"""Pluggable retry strategies for compensation middleware.

This module implements the Strategy pattern for retry behavior, allowing
developers to customize how transient failures are detected and retried
before triggering rollback.

Key Features:
- Failure classification: TRANSIENT (retry) vs PERMANENT (no retry)
- Exponential backoff with jitter
- Parameter transformation between retry attempts
- Per-tool retry configuration
- Composable strategy chains
"""

import logging
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List

from langchain_core.messages import ToolMessage


class FailureType(Enum):
    """Classification of failure types for retry decisions."""

    TRANSIENT = "transient"  # Should retry (network, timeout, temporary unavailability)
    PERMANENT = "permanent"  # Should NOT retry (validation, resource doesn't exist)
    UNKNOWN = "unknown"  # Cannot determine, defer to default behavior


@dataclass
class RetryConfig:
    """Configuration for retry behavior.

    Attributes:
        max_retries: Maximum number of retry attempts (0 = no retries)
        base_delay: Base delay in seconds between retries
        max_delay: Maximum delay cap in seconds
        exponential_base: Base for exponential backoff (e.g., 2 for doubling)
        jitter: Whether to add random jitter to prevent thundering herd
    """

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True


@dataclass
class RetryContext:
    """Context passed to retry transformers and strategies.

    Attributes:
        tool_name: Name of the tool being retried
        attempt: Current attempt number (1-indexed)
        original_params: Original parameters from first attempt
        last_result: Result from the previous failed attempt
        elapsed_time: Total time spent in retries so far
        failure_history: List of (attempt, FailureType, error_snippet) tuples
    """

    tool_name: str
    attempt: int
    original_params: Dict[str, Any]
    last_result: ToolMessage
    elapsed_time: float = 0.0
    failure_history: List[tuple] = field(default_factory=list)


@dataclass
class RetryResult:
    """Result of a retry attempt.

    Attributes:
        success: Whether the retry succeeded
        attempt: Which attempt number this was (1-indexed)
        result: The ToolMessage from the final attempt
        elapsed_time: Total time spent in retries
        failure_type: Classification of the last failure
        params_used: Parameters used in the final attempt
    """

    success: bool
    attempt: int
    result: ToolMessage
    elapsed_time: float
    failure_type: FailureType = FailureType.UNKNOWN
    params_used: Dict[str, Any] = field(default_factory=dict)


class RetryStrategy(ABC):
    """Abstract base class for retry classification strategies.

    Each strategy examines a ToolMessage and determines if the failure
    is transient (should retry) or permanent (should not retry).

    Strategies can:
    - Return FailureType.TRANSIENT: Failure is temporary, retry may succeed
    - Return FailureType.PERMANENT: Failure is permanent, do not retry
    - Return FailureType.UNKNOWN: Cannot determine, defer to next strategy
    """

    @abstractmethod
    def classify_failure(
        self,
        result: ToolMessage,
        tool_name: str,
        attempt: int,
    ) -> FailureType:
        """Classify the failure type for retry decisions.

        Args:
            result: The failed ToolMessage
            tool_name: Name of the tool that failed
            attempt: Current attempt number (1-indexed)

        Returns:
            FailureType classification
        """
        pass

    @property
    def name(self) -> str:
        """Human-readable name for logging."""
        return self.__class__.__name__


class NetworkErrorStrategy(RetryStrategy):
    """Classify network-related errors as transient.

    Detects patterns like:
    - Connection refused/reset
    - Timeout errors
    - DNS failures
    - HTTP 5xx errors
    - Rate limiting
    """

    TRANSIENT_PATTERNS = [
        "connection refused",
        "connection reset",
        "timeout",
        "timed out",
        "network unreachable",
        "dns",
        "502",
        "503",
        "504",  # HTTP status codes
        "service unavailable",
        "temporarily unavailable",
        "rate limit",
        "too many requests",
        "retry later",
        "try again",
        "temporary",
        "transient",
    ]

    def classify_failure(
        self,
        result: ToolMessage,
        tool_name: str,
        attempt: int,
    ) -> FailureType:
        content = str(result.content).lower()

        for pattern in self.TRANSIENT_PATTERNS:
            if pattern in content:
                return FailureType.TRANSIENT

        return FailureType.UNKNOWN


class ValidationErrorStrategy(RetryStrategy):
    """Classify validation errors as permanent.

    Detects patterns like:
    - Invalid input/parameter
    - Missing required field
    - Type errors
    - Not found (resource doesn't exist)
    - Authorization failures
    """

    PERMANENT_PATTERNS = [
        "invalid",
        "validation error",
        "required field",
        "not found",
        "does not exist",
        "unauthorized",
        "forbidden",
        "permission denied",
        "400",  # Bad request
        "401",  # Unauthorized
        "403",  # Forbidden
        "404",  # Not found
        "422",  # Unprocessable entity
        "missing required",
        "type error",
        "typeerror",
        "valueerror",
    ]

    def classify_failure(
        self,
        result: ToolMessage,
        tool_name: str,
        attempt: int,
    ) -> FailureType:
        content = str(result.content).lower()

        for pattern in self.PERMANENT_PATTERNS:
            if pattern in content:
                return FailureType.PERMANENT

        return FailureType.UNKNOWN


class ResourceUnavailableStrategy(RetryStrategy):
    """Handle resource unavailability with configurable behavior.

    Some resources like machines/workers may be temporarily busy
    or permanently broken. This strategy allows custom pattern lists.
    """

    def __init__(
        self,
        transient_patterns: List[str] | None = None,
        permanent_patterns: List[str] | None = None,
    ):
        self.transient_patterns = transient_patterns or [
            "busy",
            "in use",
            "currently unavailable",
            "queue full",
            "capacity",
            "overloaded",
        ]
        self.permanent_patterns = permanent_patterns or [
            "broken",
            "out of service",
            "decommissioned",
            "permanently unavailable",
            "shutdown",
            "maintenance",
            "breakdown",
        ]

    def classify_failure(
        self,
        result: ToolMessage,
        tool_name: str,
        attempt: int,
    ) -> FailureType:
        content = str(result.content).lower()

        # Check permanent patterns first (higher priority)
        for pattern in self.permanent_patterns:
            if pattern in content:
                return FailureType.PERMANENT

        for pattern in self.transient_patterns:
            if pattern in content:
                return FailureType.TRANSIENT

        return FailureType.UNKNOWN


class ToolSpecificRetryStrategy(RetryStrategy):
    """Apply different retry rules per tool.

    Example:
        strategy = ToolSpecificRetryStrategy({
            "schedule_job": RetryConfig(max_retries=5),
            "book_flight": RetryConfig(max_retries=2),
            "validate_input": RetryConfig(max_retries=0),  # Never retry
        })
    """

    def __init__(
        self,
        tool_configs: Dict[str, RetryConfig | FailureType] | None = None,
    ):
        """Initialize with per-tool configurations.

        Args:
            tool_configs: Map of tool_name -> RetryConfig or FailureType.
                If FailureType, that classification is always returned.
                If RetryConfig, max_retries=0 means PERMANENT.
        """
        self.tool_configs = tool_configs or {}

    def classify_failure(
        self,
        result: ToolMessage,
        tool_name: str,
        attempt: int,
    ) -> FailureType:
        if tool_name not in self.tool_configs:
            return FailureType.UNKNOWN

        config = self.tool_configs[tool_name]

        if isinstance(config, FailureType):
            return config

        if isinstance(config, RetryConfig):
            # If max_retries is 0, it's permanently not retriable for this tool
            if config.max_retries == 0:
                return FailureType.PERMANENT
            # Otherwise, it's transient if we haven't exceeded retries
            if attempt <= config.max_retries:
                return FailureType.TRANSIENT
            return FailureType.PERMANENT

        return FailureType.UNKNOWN


class CompositeRetryStrategy(RetryStrategy):
    """Chains multiple retry strategies together.

    Strategies are evaluated in order until one returns a definitive
    classification (TRANSIENT or PERMANENT). If all return UNKNOWN,
    the default behavior is used.
    """

    def __init__(
        self,
        strategies: List[RetryStrategy] | None = None,
        default_type: FailureType = FailureType.PERMANENT,
    ):
        """Initialize composite strategy.

        Args:
            strategies: Ordered list of strategies. Defaults to:
                [NetworkError, ValidationError, ResourceUnavailable]
            default_type: What to return when all strategies return UNKNOWN.
                PERMANENT (default) means don't retry unknown failures.
        """
        self.strategies = strategies or [
            NetworkErrorStrategy(),
            ValidationErrorStrategy(),
            ResourceUnavailableStrategy(),
        ]
        self.default_type = default_type

    def classify_failure(
        self,
        result: ToolMessage,
        tool_name: str,
        attempt: int,
    ) -> FailureType:
        for strategy in self.strategies:
            classification = strategy.classify_failure(result, tool_name, attempt)
            if classification != FailureType.UNKNOWN:
                logging.debug(
                    f"Retry strategy {strategy.name} classified failure as {classification.value}"
                )
                return classification

        return self.default_type

    @property
    def name(self) -> str:
        names = [s.name for s in self.strategies]
        return f"CompositeRetryStrategy({', '.join(names)})"


class RetryTransformer(ABC):
    """Abstract base class for parameter transformation between retries.

    Transformers allow modifying tool parameters between retry attempts,
    enabling scenarios like:
    - Trying a different machine when one is broken
    - Using fallback resources
    - Adjusting request parameters
    """

    @abstractmethod
    def transform(
        self,
        params: Dict[str, Any],
        context: RetryContext,
    ) -> Dict[str, Any] | None:
        """Transform parameters for the next retry attempt.

        Args:
            params: Current parameters (may already be transformed)
            context: Retry context with attempt info and failure history

        Returns:
            Transformed parameters for next attempt, or None to skip retry
        """
        pass

    @property
    def name(self) -> str:
        """Human-readable name for logging."""
        return self.__class__.__name__


class IdentityTransformer(RetryTransformer):
    """Default transformer that returns parameters unchanged."""

    def transform(
        self,
        params: Dict[str, Any],
        context: RetryContext,
    ) -> Dict[str, Any]:
        return params


class AlternativeResourceTransformer(RetryTransformer):
    """Picks alternative resource when primary fails.

    Useful for scenarios like:
    - Machine breakdown -> try different machine
    - Server unavailable -> try different server
    - Region failure -> try different region

    Example:
        transformer = AlternativeResourceTransformer(
            resource_field="machine_id",
            alternatives_fn=lambda current, ctx: ["machine_2", "machine_3"],
        )
    """

    def __init__(
        self,
        resource_field: str,
        alternatives_fn: Callable[[Any, RetryContext], List[Any]],
        max_alternatives: int | None = None,
    ):
        """Initialize the transformer.

        Args:
            resource_field: The parameter name containing the resource ID
            alternatives_fn: Function that returns list of alternative values.
                Takes (current_value, context) and returns [alternatives].
            max_alternatives: Maximum alternatives to try before giving up.
                None means try all alternatives.
        """
        self.resource_field = resource_field
        self.alternatives_fn = alternatives_fn
        self.max_alternatives = max_alternatives
        self._tried_resources: Dict[str, set] = {}  # tool_name -> set of tried values

    def transform(
        self,
        params: Dict[str, Any],
        context: RetryContext,
    ) -> Dict[str, Any] | None:
        if self.resource_field not in params:
            logging.warning(
                f"Resource field '{self.resource_field}' not found in params, "
                f"returning unchanged"
            )
            return params

        current_value = params[self.resource_field]

        # Track tried resources per tool
        tool_key = context.tool_name
        if tool_key not in self._tried_resources:
            self._tried_resources[tool_key] = set()

        self._tried_resources[tool_key].add(current_value)

        # Get alternatives
        try:
            alternatives = self.alternatives_fn(current_value, context)
        except Exception as e:
            logging.error(f"alternatives_fn raised exception: {e}")
            return None

        # Filter out already tried resources
        untried = [a for a in alternatives if a not in self._tried_resources[tool_key]]

        # Apply max_alternatives limit
        if self.max_alternatives is not None:
            if len(self._tried_resources[tool_key]) >= self.max_alternatives:
                logging.info(
                    f"Reached max_alternatives limit ({self.max_alternatives}), "
                    f"stopping retry"
                )
                return None

        if not untried:
            logging.info(f"No untried alternatives for {self.resource_field}, stopping retry")
            return None

        # Pick first untried alternative
        next_value = untried[0]
        logging.info(
            f"Transforming {self.resource_field}: {current_value} -> {next_value} "
            f"(attempt {context.attempt})"
        )

        # Return new params with alternative resource
        new_params = params.copy()
        new_params[self.resource_field] = next_value
        return new_params

    def reset(self) -> None:
        """Reset tried resources tracking (call between transactions)."""
        self._tried_resources.clear()


class CompositeTransformer(RetryTransformer):
    """Chains multiple transformers together.

    Transformers are applied in order. If any returns None, the chain stops.
    """

    def __init__(self, transformers: List[RetryTransformer]):
        self.transformers = transformers

    def transform(
        self,
        params: Dict[str, Any],
        context: RetryContext,
    ) -> Dict[str, Any] | None:
        current_params = params

        for transformer in self.transformers:
            result = transformer.transform(current_params, context)
            if result is None:
                logging.debug(f"Transformer {transformer.name} returned None, stopping chain")
                return None
            current_params = result

        return current_params

    @property
    def name(self) -> str:
        names = [t.name for t in self.transformers]
        return f"CompositeTransformer({', '.join(names)})"


class RetryExecutor:
    """Executes retry logic with configurable backoff.

    This class handles the actual retry loop, backoff calculation,
    and tracing/logging of retry attempts.
    """

    def __init__(
        self,
        config: RetryConfig,
        classifier: RetryStrategy,
        transformer: RetryTransformer | None = None,
    ):
        self.config = config
        self.classifier = classifier
        self.transformer = transformer or IdentityTransformer()

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay before next retry with exponential backoff."""
        delay = self.config.base_delay * (self.config.exponential_base ** (attempt - 1))
        delay = min(delay, self.config.max_delay)

        if self.config.jitter:
            # Add +/- 25% jitter
            jitter_range = delay * 0.25
            delay += random.uniform(-jitter_range, jitter_range)

        return max(0, delay)

    def should_retry(
        self,
        result: ToolMessage,
        tool_name: str,
        attempt: int,
    ) -> tuple[bool, FailureType]:
        """Determine if we should retry this failure.

        Args:
            result: The failed ToolMessage
            tool_name: Name of the tool
            attempt: Current attempt (1-indexed)

        Returns:
            Tuple of (should_retry, failure_type)
        """
        if attempt > self.config.max_retries:
            return False, FailureType.PERMANENT

        failure_type = self.classifier.classify_failure(result, tool_name, attempt)
        should_retry = failure_type == FailureType.TRANSIENT

        return should_retry, failure_type

    def execute_with_retry(
        self,
        tool_name: str,
        execute_fn: Callable[[Dict[str, Any]], ToolMessage],
        is_error_fn: Callable[[ToolMessage], bool],
        initial_params: Dict[str, Any],
    ) -> RetryResult:
        """Execute a tool call with retry logic.

        Args:
            tool_name: Name of the tool being executed
            execute_fn: Function that executes the tool with params and returns ToolMessage
            is_error_fn: Function that determines if result is an error
            initial_params: Initial parameters for the tool call

        Returns:
            RetryResult with final outcome
        """
        start_time = time.time()
        attempt = 0
        last_result: ToolMessage | None = None
        last_failure_type = FailureType.UNKNOWN
        current_params = initial_params
        failure_history: List[tuple] = []

        while attempt <= self.config.max_retries:
            attempt += 1

            logging.info(
                f"Executing {tool_name} (attempt {attempt}/{self.config.max_retries + 1})"
            )

            try:
                result = execute_fn(current_params)
            except Exception as e:
                result = ToolMessage(
                    content=f"Execution exception: {str(e)}",
                    tool_call_id="retry",
                    name=tool_name,
                    status="error",
                )

            last_result = result

            # Check if successful
            if not is_error_fn(result):
                return RetryResult(
                    success=True,
                    attempt=attempt,
                    result=result,
                    elapsed_time=time.time() - start_time,
                    failure_type=FailureType.UNKNOWN,
                    params_used=current_params,
                )

            # Failed - check if we should retry
            should_retry, failure_type = self.should_retry(result, tool_name, attempt)
            last_failure_type = failure_type

            # Record failure history
            error_snippet = str(result.content)[:100] if result.content else ""
            failure_history.append((attempt, failure_type, error_snippet))

            if not should_retry:
                logging.info(
                    f"{tool_name} failed with {failure_type.value} failure, not retrying"
                )
                break

            if attempt <= self.config.max_retries:
                # Try to transform parameters for next attempt
                context = RetryContext(
                    tool_name=tool_name,
                    attempt=attempt,
                    original_params=initial_params,
                    last_result=result,
                    elapsed_time=time.time() - start_time,
                    failure_history=failure_history,
                )

                transformed = self.transformer.transform(current_params, context)

                if transformed is None:
                    logging.info(
                        f"Transformer returned None for {tool_name}, stopping retry"
                    )
                    break

                current_params = transformed

                delay = self.calculate_delay(attempt)
                logging.info(
                    f"{tool_name} failed (transient), retrying in {delay:.2f}s "
                    f"(attempt {attempt + 1}/{self.config.max_retries + 1})"
                )
                time.sleep(delay)

        return RetryResult(
            success=False,
            attempt=attempt,
            result=last_result,
            elapsed_time=time.time() - start_time,
            failure_type=last_failure_type,
            params_used=current_params,
        )


# Factory functions


def create_retry_classifier(
    strategies: List[RetryStrategy] | None = None,
    default_type: FailureType = FailureType.PERMANENT,
) -> CompositeRetryStrategy:
    """Factory function to create a configured retry classifier.

    Args:
        strategies: Custom strategy list, or None for defaults
        default_type: Fallback behavior when uncertain

    Returns:
        Configured CompositeRetryStrategy instance
    """
    return CompositeRetryStrategy(
        strategies=strategies,
        default_type=default_type,
    )


def create_retry_executor(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    classifier: RetryStrategy | None = None,
    transformer: RetryTransformer | None = None,
) -> RetryExecutor:
    """Factory function to create a configured retry executor.

    Args:
        max_retries: Maximum retry attempts
        base_delay: Initial delay between retries
        max_delay: Maximum delay cap
        exponential_base: Exponential backoff multiplier
        jitter: Whether to add random jitter
        classifier: Custom failure classifier
        transformer: Custom parameter transformer

    Returns:
        Configured RetryExecutor instance
    """
    config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
    )

    return RetryExecutor(
        config=config,
        classifier=classifier or create_retry_classifier(),
        transformer=transformer,
    )


# Default instances for convenience
DEFAULT_RETRY_STRATEGIES = [
    NetworkErrorStrategy(),
    ValidationErrorStrategy(),
    ResourceUnavailableStrategy(),
]
