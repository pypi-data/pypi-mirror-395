"""Tests for retry strategy module."""

import time
from unittest.mock import MagicMock

import pytest
from langchain_core.messages import ToolMessage

from langchain_compensation.retry import (
    FailureType,
    RetryConfig,
    RetryContext,
    RetryResult,
    NetworkErrorStrategy,
    ValidationErrorStrategy,
    ResourceUnavailableStrategy,
    ToolSpecificRetryStrategy,
    CompositeRetryStrategy,
    RetryTransformer,
    IdentityTransformer,
    AlternativeResourceTransformer,
    CompositeTransformer,
    RetryExecutor,
    create_retry_classifier,
    create_retry_executor,
)


class TestFailureClassification:
    """Tests for failure type classification."""

    def test_network_error_classified_as_transient(self):
        """Test that network errors are transient."""
        strategy = NetworkErrorStrategy()

        # Connection errors
        result = ToolMessage(content="Connection refused", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.TRANSIENT

        result = ToolMessage(content="Request timed out", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.TRANSIENT

        # HTTP 5xx errors
        result = ToolMessage(content="503 Service Unavailable", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.TRANSIENT

        result = ToolMessage(content="Error 502 Bad Gateway", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.TRANSIENT

        # Rate limiting
        result = ToolMessage(content="Rate limit exceeded, try again", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.TRANSIENT

    def test_validation_error_classified_as_permanent(self):
        """Test that validation errors are permanent."""
        strategy = ValidationErrorStrategy()

        result = ToolMessage(content="Invalid parameter: id", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.PERMANENT

        result = ToolMessage(content="Resource not found", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.PERMANENT

        result = ToolMessage(content="401 Unauthorized", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.PERMANENT

        result = ToolMessage(content="403 Forbidden - no access", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.PERMANENT

        result = ToolMessage(content="422 Unprocessable Entity", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.PERMANENT

    def test_unknown_error_defers(self):
        """Test that unknown errors return UNKNOWN."""
        strategy = NetworkErrorStrategy()

        result = ToolMessage(content="Something went wrong", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.UNKNOWN

    def test_resource_unavailable_strategy(self):
        """Test resource unavailability classification."""
        strategy = ResourceUnavailableStrategy()

        # Transient - busy
        result = ToolMessage(content="Machine is busy", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.TRANSIENT

        result = ToolMessage(content="Queue full, try later", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.TRANSIENT

        # Permanent - broken
        result = ToolMessage(content="Machine breakdown detected", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.PERMANENT

        result = ToolMessage(content="Out of service", tool_call_id="1", name="test")
        assert strategy.classify_failure(result, "test", 1) == FailureType.PERMANENT

    def test_composite_strategy_chain(self):
        """Test that composite strategy chains correctly."""
        composite = CompositeRetryStrategy(
            strategies=[NetworkErrorStrategy(), ValidationErrorStrategy()],
            default_type=FailureType.PERMANENT,
        )

        # Network error -> TRANSIENT (first strategy matches)
        result = ToolMessage(content="Connection timeout", tool_call_id="1", name="test")
        assert composite.classify_failure(result, "test", 1) == FailureType.TRANSIENT

        # Validation error -> PERMANENT (second strategy matches)
        result = ToolMessage(content="Invalid input", tool_call_id="1", name="test")
        assert composite.classify_failure(result, "test", 1) == FailureType.PERMANENT

        # Unknown -> default (PERMANENT)
        result = ToolMessage(content="Unknown error occurred", tool_call_id="1", name="test")
        assert composite.classify_failure(result, "test", 1) == FailureType.PERMANENT

    def test_composite_with_default_transient(self):
        """Test composite with default_type=TRANSIENT."""
        composite = CompositeRetryStrategy(
            strategies=[ValidationErrorStrategy()],  # Only validation
            default_type=FailureType.TRANSIENT,
        )

        # Unknown error -> default (TRANSIENT)
        result = ToolMessage(content="Some random error", tool_call_id="1", name="test")
        assert composite.classify_failure(result, "test", 1) == FailureType.TRANSIENT

    def test_tool_specific_strategy(self):
        """Test per-tool retry configuration."""
        strategy = ToolSpecificRetryStrategy({
            "flaky_tool": RetryConfig(max_retries=5),
            "no_retry_tool": RetryConfig(max_retries=0),
            "always_retry": FailureType.TRANSIENT,
            "never_retry": FailureType.PERMANENT,
        })

        result = ToolMessage(content="Error", tool_call_id="1", name="test")

        # flaky_tool with RetryConfig should retry
        assert strategy.classify_failure(result, "flaky_tool", 1) == FailureType.TRANSIENT
        assert strategy.classify_failure(result, "flaky_tool", 5) == FailureType.TRANSIENT
        assert strategy.classify_failure(result, "flaky_tool", 6) == FailureType.PERMANENT  # Exceeded

        # no_retry_tool should not retry
        assert strategy.classify_failure(result, "no_retry_tool", 1) == FailureType.PERMANENT

        # Direct FailureType assignments
        assert strategy.classify_failure(result, "always_retry", 1) == FailureType.TRANSIENT
        assert strategy.classify_failure(result, "never_retry", 1) == FailureType.PERMANENT

        # unknown tool defers
        assert strategy.classify_failure(result, "other_tool", 1) == FailureType.UNKNOWN


class TestRetryConfig:
    """Tests for RetryConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 30.0
        assert config.exponential_base == 2.0
        assert config.jitter is True

    def test_custom_values(self):
        """Test custom configuration values."""
        config = RetryConfig(
            max_retries=5,
            base_delay=0.5,
            max_delay=10.0,
            exponential_base=3.0,
            jitter=False,
        )
        assert config.max_retries == 5
        assert config.base_delay == 0.5
        assert config.max_delay == 10.0
        assert config.exponential_base == 3.0
        assert config.jitter is False


class TestRetryTransformers:
    """Tests for retry transformers."""

    def test_identity_transformer(self):
        """Test identity transformer returns unchanged params."""
        transformer = IdentityTransformer()
        params = {"machine_id": "m1", "job_id": "j1"}
        context = RetryContext(
            tool_name="test",
            attempt=1,
            original_params=params,
            last_result=ToolMessage(content="Error", tool_call_id="1", name="test"),
        )

        result = transformer.transform(params, context)
        assert result == params

    def test_alternative_resource_transformer(self):
        """Test alternative resource transformer picks new resource."""
        transformer = AlternativeResourceTransformer(
            resource_field="machine_id",
            alternatives_fn=lambda current, ctx: ["m2", "m3", "m4"],
        )

        params = {"machine_id": "m1", "job_id": "j1"}
        context = RetryContext(
            tool_name="test",
            attempt=1,
            original_params=params,
            last_result=ToolMessage(content="Error", tool_call_id="1", name="test"),
        )

        # First transformation: m1 -> m2
        result = transformer.transform(params, context)
        assert result["machine_id"] == "m2"
        assert result["job_id"] == "j1"

        # Second transformation: m2 -> m3
        result2 = transformer.transform(result, context)
        assert result2["machine_id"] == "m3"

        # Third transformation: m3 -> m4
        result3 = transformer.transform(result2, context)
        assert result3["machine_id"] == "m4"

        # No more alternatives
        result4 = transformer.transform(result3, context)
        assert result4 is None

    def test_alternative_resource_transformer_max_limit(self):
        """Test max_alternatives limit."""
        transformer = AlternativeResourceTransformer(
            resource_field="machine_id",
            alternatives_fn=lambda current, ctx: ["m2", "m3", "m4", "m5"],
            max_alternatives=2,
        )

        params = {"machine_id": "m1"}
        context = RetryContext(
            tool_name="test",
            attempt=1,
            original_params=params,
            last_result=ToolMessage(content="Error", tool_call_id="1", name="test"),
        )

        # First transformation: m1 -> m2
        result = transformer.transform(params, context)
        assert result["machine_id"] == "m2"

        # Second: m2 -> but we've tried 2 already
        result2 = transformer.transform(result, context)
        assert result2 is None  # max_alternatives reached

    def test_alternative_resource_transformer_missing_field(self):
        """Test behavior when resource field is missing."""
        transformer = AlternativeResourceTransformer(
            resource_field="machine_id",
            alternatives_fn=lambda current, ctx: ["m2"],
        )

        params = {"job_id": "j1"}  # No machine_id
        context = RetryContext(
            tool_name="test",
            attempt=1,
            original_params=params,
            last_result=ToolMessage(content="Error", tool_call_id="1", name="test"),
        )

        result = transformer.transform(params, context)
        assert result == params  # Unchanged

    def test_alternative_resource_transformer_reset(self):
        """Test reset clears tried resources."""
        transformer = AlternativeResourceTransformer(
            resource_field="machine_id",
            alternatives_fn=lambda current, ctx: ["m2"],
        )

        params = {"machine_id": "m1"}
        context = RetryContext(
            tool_name="test",
            attempt=1,
            original_params=params,
            last_result=ToolMessage(content="Error", tool_call_id="1", name="test"),
        )

        # First use
        result = transformer.transform(params, context)
        assert result["machine_id"] == "m2"

        # No more alternatives
        result2 = transformer.transform(result, context)
        assert result2 is None

        # Reset and try again
        transformer.reset()
        result3 = transformer.transform(params, context)
        assert result3["machine_id"] == "m2"

    def test_composite_transformer(self):
        """Test composite transformer chains multiple transformers."""
        transformer1 = IdentityTransformer()
        transformer2 = AlternativeResourceTransformer(
            resource_field="machine_id",
            alternatives_fn=lambda current, ctx: ["m2"],
        )

        composite = CompositeTransformer([transformer1, transformer2])

        params = {"machine_id": "m1"}
        context = RetryContext(
            tool_name="test",
            attempt=1,
            original_params=params,
            last_result=ToolMessage(content="Error", tool_call_id="1", name="test"),
        )

        result = composite.transform(params, context)
        assert result["machine_id"] == "m2"


class TestRetryExecutor:
    """Tests for RetryExecutor."""

    def test_no_retry_on_success(self):
        """Test that successful calls don't retry."""
        executor = create_retry_executor(max_retries=3)

        call_count = [0]

        def execute_fn(params):
            call_count[0] += 1
            return ToolMessage(content="Success", tool_call_id="1", name="test")

        result = executor.execute_with_retry(
            "test",
            execute_fn,
            lambda r: "Error" in str(r.content),
            {"param": "value"},
        )

        assert result.success
        assert result.attempt == 1
        assert call_count[0] == 1

    def test_retry_on_transient_failure(self):
        """Test that transient failures trigger retry."""
        executor = create_retry_executor(max_retries=3, base_delay=0.01, jitter=False)

        call_count = [0]

        def execute_fn(params):
            call_count[0] += 1
            if call_count[0] < 3:
                return ToolMessage(
                    content="Connection timeout", tool_call_id="1", name="test", status="error"
                )
            return ToolMessage(content="Success", tool_call_id="1", name="test")

        result = executor.execute_with_retry(
            "test",
            execute_fn,
            lambda r: r.status == "error",
            {},
        )

        assert result.success
        assert result.attempt == 3
        assert call_count[0] == 3

    def test_no_retry_on_permanent_failure(self):
        """Test that permanent failures don't retry."""
        executor = create_retry_executor(max_retries=3, base_delay=0.01)

        call_count = [0]

        def execute_fn(params):
            call_count[0] += 1
            return ToolMessage(
                content="Invalid parameter", tool_call_id="1", name="test", status="error"
            )

        result = executor.execute_with_retry(
            "test",
            execute_fn,
            lambda r: r.status == "error",
            {},
        )

        assert not result.success
        assert result.attempt == 1  # No retries for permanent failure
        assert call_count[0] == 1
        assert result.failure_type == FailureType.PERMANENT

    def test_retry_exhaustion(self):
        """Test that retries are exhausted correctly."""
        executor = create_retry_executor(max_retries=2, base_delay=0.01, jitter=False)

        call_count = [0]

        def execute_fn(params):
            call_count[0] += 1
            return ToolMessage(
                content="Connection timeout", tool_call_id="1", name="test", status="error"
            )

        result = executor.execute_with_retry(
            "test",
            execute_fn,
            lambda r: r.status == "error",
            {},
        )

        assert not result.success
        assert result.attempt == 3  # Initial + 2 retries
        assert call_count[0] == 3

    def test_exponential_backoff_calculation(self):
        """Test that backoff increases exponentially."""
        config = RetryConfig(
            max_retries=3,
            base_delay=0.1,
            exponential_base=2.0,
            jitter=False,
        )
        executor = RetryExecutor(config, create_retry_classifier())

        assert abs(executor.calculate_delay(1) - 0.1) < 0.01
        assert abs(executor.calculate_delay(2) - 0.2) < 0.01
        assert abs(executor.calculate_delay(3) - 0.4) < 0.01

    def test_max_delay_cap(self):
        """Test that delay is capped at max_delay."""
        config = RetryConfig(
            max_retries=10,
            base_delay=1.0,
            max_delay=5.0,
            exponential_base=2.0,
            jitter=False,
        )
        executor = RetryExecutor(config, create_retry_classifier())

        # Delay should be capped at 5.0
        assert executor.calculate_delay(10) == 5.0

    def test_retry_with_transformer(self):
        """Test retry with parameter transformation."""
        transformer = AlternativeResourceTransformer(
            resource_field="machine_id",
            alternatives_fn=lambda current, ctx: ["m2", "m3"],
        )

        executor = create_retry_executor(
            max_retries=3,
            base_delay=0.01,
            jitter=False,
            transformer=transformer,
        )

        machines_tried = []

        def execute_fn(params):
            machines_tried.append(params.get("machine_id"))
            # Fail on m1 and m2, succeed on m3
            if params.get("machine_id") == "m3":
                return ToolMessage(content="Success", tool_call_id="1", name="test")
            return ToolMessage(
                content="Machine busy", tool_call_id="1", name="test", status="error"
            )

        result = executor.execute_with_retry(
            "test",
            execute_fn,
            lambda r: r.status == "error",
            {"machine_id": "m1"},
        )

        assert result.success
        assert machines_tried == ["m1", "m2", "m3"]
        assert result.params_used["machine_id"] == "m3"

    def test_exception_handling(self):
        """Test that exceptions are caught and converted to error results."""
        executor = create_retry_executor(max_retries=1, base_delay=0.01)

        def execute_fn(params):
            raise ValueError("Something went wrong")

        result = executor.execute_with_retry(
            "test",
            execute_fn,
            lambda r: r.status == "error",
            {},
        )

        assert not result.success
        assert "exception" in result.result.content.lower()


class TestFactoryFunctions:
    """Tests for factory functions."""

    def test_create_retry_classifier_default(self):
        """Test default retry classifier creation."""
        classifier = create_retry_classifier()

        assert isinstance(classifier, CompositeRetryStrategy)
        assert len(classifier.strategies) == 3
        assert classifier.default_type == FailureType.PERMANENT

    def test_create_retry_classifier_custom(self):
        """Test custom retry classifier creation."""
        classifier = create_retry_classifier(
            strategies=[NetworkErrorStrategy()],
            default_type=FailureType.TRANSIENT,
        )

        assert len(classifier.strategies) == 1
        assert classifier.default_type == FailureType.TRANSIENT

    def test_create_retry_executor_default(self):
        """Test default retry executor creation."""
        executor = create_retry_executor()

        assert executor.config.max_retries == 3
        assert executor.config.base_delay == 1.0
        assert isinstance(executor.classifier, CompositeRetryStrategy)

    def test_create_retry_executor_custom(self):
        """Test custom retry executor creation."""
        transformer = IdentityTransformer()
        executor = create_retry_executor(
            max_retries=5,
            base_delay=0.5,
            transformer=transformer,
        )

        assert executor.config.max_retries == 5
        assert executor.config.base_delay == 0.5
        assert executor.transformer == transformer


class TestMiddlewareIntegration:
    """Integration tests for retry with middleware."""

    def test_middleware_with_retry_config(self):
        """Test that middleware accepts retry configuration."""
        from langchain_compensation import CompensationMiddleware

        middleware = CompensationMiddleware(
            compensation_mapping={"test": "undo_test"},
            max_retries=3,
            retry_backoff=1.0,
            partial_rollback=True,
        )

        assert middleware._max_retries == 3
        assert middleware._retry_backoff == 1.0
        assert middleware._partial_rollback is True

    def test_default_no_retry(self):
        """Test that default behavior is no retry (backward compatible)."""
        from langchain_compensation import CompensationMiddleware

        middleware = CompensationMiddleware(
            compensation_mapping={"test": "undo_test"},
        )

        assert middleware._max_retries == 0
        assert middleware._get_retry_executor() is None

    def test_retry_executor_lazy_init(self):
        """Test that retry executor is lazily initialized."""
        from langchain_compensation import CompensationMiddleware

        middleware = CompensationMiddleware(
            compensation_mapping={"test": "undo_test"},
            max_retries=3,
        )

        assert middleware._retry_executor is None  # Not initialized yet
        executor = middleware._get_retry_executor()
        assert executor is not None
        assert middleware._retry_executor is executor  # Now cached


class TestPartialRollback:
    """Tests for partial rollback functionality."""

    def test_partial_rollback_finds_dependents(self):
        """Test that partial rollback correctly identifies dependent actions."""
        from langchain_compensation import (
            CompensationMiddleware,
            CompensationLog,
            CompensationRecord,
        )

        middleware = CompensationMiddleware(
            compensation_mapping={
                "book_flight": "cancel_flight",
                "book_hotel": "cancel_hotel",
                "book_car": "cancel_car",
            },
            partial_rollback=True,
        )

        log = CompensationLog()

        # book_flight (no deps)
        log.add(
            CompensationRecord(
                id="flight_1",
                tool_name="book_flight",
                params={},
                timestamp=1.0,
                compensation_tool="cancel_flight",
                status="COMPLETED",
                result={"booking_id": "FL123"},
            )
        )

        # book_hotel depends on flight
        log.add(
            CompensationRecord(
                id="hotel_1",
                tool_name="book_hotel",
                params={"near_airport": "FL123"},
                timestamp=2.0,
                compensation_tool="cancel_hotel",
                status="COMPLETED",
                depends_on=["flight_1"],
            )
        )

        # book_car (independent, no deps)
        log.add(
            CompensationRecord(
                id="car_1",
                tool_name="book_car",
                params={},
                timestamp=3.0,
                compensation_tool="cancel_car",
                status="COMPLETED",
                depends_on=[],
            )
        )

        # Get partial rollback for failed flight
        plan = middleware._get_partial_rollback_plan("flight_1", log)

        # Only hotel depends on flight
        ids_in_plan = [r["id"] for r in plan]
        assert "hotel_1" in ids_in_plan
        assert "car_1" not in ids_in_plan  # Independent, should NOT be rolled back

    def test_partial_rollback_transitive_deps(self):
        """Test that transitive dependencies are included."""
        from langchain_compensation import (
            CompensationMiddleware,
            CompensationLog,
            CompensationRecord,
        )

        middleware = CompensationMiddleware(
            compensation_mapping={
                "a": "undo_a",
                "b": "undo_b",
                "c": "undo_c",
            },
            partial_rollback=True,
        )

        log = CompensationLog()

        # Chain: a -> b -> c
        log.add(
            CompensationRecord(
                id="a1",
                tool_name="a",
                params={},
                timestamp=1.0,
                compensation_tool="undo_a",
                status="COMPLETED",
            )
        )
        log.add(
            CompensationRecord(
                id="b1",
                tool_name="b",
                params={},
                timestamp=2.0,
                compensation_tool="undo_b",
                status="COMPLETED",
                depends_on=["a1"],
            )
        )
        log.add(
            CompensationRecord(
                id="c1",
                tool_name="c",
                params={},
                timestamp=3.0,
                compensation_tool="undo_c",
                status="COMPLETED",
                depends_on=["b1"],
            )
        )

        # If a1 fails, both b1 and c1 should be rolled back (transitive)
        plan = middleware._get_partial_rollback_plan("a1", log)
        ids_in_plan = [r["id"] for r in plan]

        assert "b1" in ids_in_plan
        assert "c1" in ids_in_plan

    def test_full_rollback_when_disabled(self):
        """Test that full rollback is used when partial_rollback=False."""
        from langchain_compensation import (
            CompensationMiddleware,
            CompensationLog,
            CompensationRecord,
        )

        middleware = CompensationMiddleware(
            compensation_mapping={
                "a": "undo_a",
                "b": "undo_b",
            },
            partial_rollback=False,  # Disabled
        )

        log = CompensationLog()

        log.add(
            CompensationRecord(
                id="a1",
                tool_name="a",
                params={},
                timestamp=1.0,
                compensation_tool="undo_a",
                status="COMPLETED",
            )
        )
        log.add(
            CompensationRecord(
                id="b1",
                tool_name="b",
                params={},
                timestamp=2.0,
                compensation_tool="undo_b",
                status="COMPLETED",
                depends_on=[],  # Independent
            )
        )

        # With partial_rollback=False, should return full plan
        plan = middleware._get_partial_rollback_plan("a1", log)
        ids_in_plan = [r["id"] for r in plan]

        # Both should be included (full rollback)
        assert "a1" in ids_in_plan
        assert "b1" in ids_in_plan
