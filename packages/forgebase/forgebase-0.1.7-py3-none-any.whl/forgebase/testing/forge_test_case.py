"""
Cognitive test base class for ForgeBase.

Provides a test case class that extends unittest.TestCase with cognitive
assertions, intent validation, and observability checks. Tests written with
ForgeTestCase document not just "what" works, but "why" it should work.

Philosophy:
    Traditional tests verify behavior. Cognitive tests verify intention.
    They ask: "Does the code do what we intended?" and "Do the metrics
    reflect our expectations?" This creates a feedback loop between
    intention, implementation, and observation.

    Key principles:
    1. Tests document intention, not just behavior
    2. Side effects are explicit and validated
    3. Metrics are first-class citizens in testing
    4. Context isolation prevents test pollution

Use Cases:
    - Testing UseCases with intent validation
    - Verifying metrics collection
    - Ensuring no unintended side effects
    - Domain logic validation with business context

Example::

    from forgebase.testing.forge_test_case import ForgeTestCase

    class TestUserCreation(ForgeTestCase):
        def test_creates_user_with_valid_data(self):
            # Document intent
            intent = "Create user with valid email and store in repository"

            # Setup
            user_data = {"email": "test@example.com", "name": "Test User"}

            # Execute
            with self.assert_no_side_effects(except_mutations=['repository']):
                user = create_user_usecase.execute(user_data)

            # Validate intent
            self.assert_intent_matches(
                intent,
                actual=f"User {user.id} created and saved"
            )

            # Validate metrics
            self.assert_metrics_collected({
                'usecase.create_user.count': 1,
                'usecase.create_user.success': 1,
            })

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import copy
import difflib
import unittest
from contextlib import contextmanager
from typing import Any


class ForgeTestCase(unittest.TestCase):
    """
    Base test case with cognitive assertions and intent validation.

    Extends unittest.TestCase with ForgeBase-specific testing capabilities:
    - Intent matching and validation
    - Metrics collection verification
    - Side effect detection and control
    - Context isolation between tests

    Features:
        - **assert_intent_matches**: Validates that execution matches intention
        - **assert_metrics_collected**: Verifies expected metrics were recorded
        - **assert_no_side_effects**: Ensures function purity (or documents mutations)
        - **setup_context**: Creates isolated test context

    This class enables "cognitive testing" where tests document and validate
    not just behavior, but the reasoning behind that behavior.

    :ivar _test_context: Isolated context for this test
    :vartype _test_context: Dict[str, Any]
    :ivar _captured_metrics: Metrics captured during test execution
    :vartype _captured_metrics: Dict[str, Any]

    Example::

        class TestCalculator(ForgeTestCase):
            def setUp(self):
                super().setUp()
                self.calculator = Calculator()

            def test_addition_intent(self):
                intent = "Add two positive integers"
                result = self.calculator.add(2, 3)

                self.assertEqual(result, 5)
                self.assert_intent_matches(
                    intent,
                    actual="2 + 3 = 5"
                )
    """

    def setUp(self):
        """
        Set up test fixtures with isolated context.

        Called before each test method. Initializes test context and
        metrics capture.
        """
        super().setUp()
        self._test_context: dict[str, Any] = {}
        self._captured_metrics: dict[str, Any] = {}
        self._side_effect_baseline: dict[str, Any] = {}

    def tearDown(self):
        """
        Clean up after test execution.

        Called after each test method. Clears context and metrics.
        """
        super().tearDown()
        self._test_context.clear()
        self._captured_metrics.clear()
        self._side_effect_baseline.clear()

    def setup_context(self, **kwargs) -> None:
        """
        Configure test context with specific values.

        Provides a way to set up common test state that can be
        accessed throughout the test.

        :param kwargs: Context key-value pairs
        :type kwargs: Any

        Example::

            def setUp(self):
                super().setUp()
                self.setup_context(
                    user_id="test-user-123",
                    tenant="test-tenant",
                    correlation_id="test-corr-id"
                )

            def test_with_context(self):
                user_id = self._test_context['user_id']
                # ... use context in test
        """
        self._test_context.update(kwargs)

    def assert_intent_matches(
        self,
        expected_intent: str,
        actual: str,
        threshold: float = 0.8
    ) -> None:
        """
        Assert that actual execution matches expected intent.

        Uses similarity matching to validate that what happened aligns
        with what was intended. This creates a bridge between intention
        (documented in test) and implementation (actual execution).

        :param expected_intent: Description of what should happen
        :type expected_intent: str
        :param actual: Description of what actually happened
        :type actual: str
        :param threshold: Similarity threshold (0.0-1.0, default 0.8)
        :type threshold: float
        :raises AssertionError: If intent doesn't match actual outcome

        Example::

            # Strong match
            self.assert_intent_matches(
                expected_intent="Store user in database",
                actual="User stored in PostgreSQL database"
            )

            # Will fail - different intent
            self.assert_intent_matches(
                expected_intent="Delete user",
                actual="User created"
            )
        """
        # Calculate similarity using difflib
        similarity = difflib.SequenceMatcher(
            None,
            expected_intent.lower(),
            actual.lower()
        ).ratio()

        if similarity < threshold:
            msg = (
                f"\n"
                f"Intent mismatch (similarity: {similarity:.2%}):\n"
                f"  Expected: {expected_intent}\n"
                f"  Actual:   {actual}\n"
                f"  Threshold: {threshold:.2%}"
            )
            self.fail(msg)

    def assert_metrics_collected(
        self,
        expected_metrics: dict[str, Any],
        metrics_collector: Any | None = None
    ) -> None:
        """
        Assert that expected metrics were collected.

        Validates that the code being tested properly instrumented itself
        with metrics. This ensures observability is maintained.

        :param expected_metrics: Dict of metric name to expected value
        :type expected_metrics: Dict[str, Any]
        :param metrics_collector: Optional metrics collector to inspect
        :type metrics_collector: Optional[Any]
        :raises AssertionError: If expected metrics weren't collected

        Example::

            # After executing a UseCase
            self.assert_metrics_collected({
                'usecase.create_user.count': 1,
                'usecase.create_user.duration_ms': lambda x: x > 0,
                'usecase.create_user.success': 1,
            })

            # With specific collector
            self.assert_metrics_collected(
                {'requests.total': 5},
                metrics_collector=my_metrics
            )
        """
        # Use provided collector or internal captured metrics
        if metrics_collector:
            # Try to get metrics from collector
            if hasattr(metrics_collector, 'get_counter'):
                for metric_name, expected_value in expected_metrics.items():
                    actual_value = metrics_collector.get_counter(metric_name)
                    self._validate_metric_value(
                        metric_name,
                        expected_value,
                        actual_value
                    )
            elif hasattr(metrics_collector, 'report'):
                report = metrics_collector.report()
                for metric_name, expected_value in expected_metrics.items():
                    # Try counters, gauges, histograms
                    actual_value = (
                        report.get('counters', {}).get(metric_name) or
                        report.get('gauges', {}).get(metric_name) or
                        report.get('histograms', {}).get(metric_name)
                    )
                    self._validate_metric_value(
                        metric_name,
                        expected_value,
                        actual_value
                    )
            else:
                self.fail(
                    f"Metrics collector {type(metrics_collector).__name__} "
                    f"doesn't support inspection"
                )
        else:
            # Use captured metrics
            for metric_name, expected_value in expected_metrics.items():
                actual_value = self._captured_metrics.get(metric_name)
                self._validate_metric_value(
                    metric_name,
                    expected_value,
                    actual_value
                )

    def _validate_metric_value(
        self,
        metric_name: str,
        expected: Any,
        actual: Any
    ) -> None:
        """
        Validate a single metric value.

        :param metric_name: Name of the metric
        :type metric_name: str
        :param expected: Expected value (or callable validator)
        :type expected: Any
        :param actual: Actual collected value
        :type actual: Any
        :raises AssertionError: If validation fails
        """
        if actual is None:
            self.fail(f"Metric '{metric_name}' was not collected")

        # If expected is callable, use it as validator
        if callable(expected):
            if not expected(actual):
                self.fail(
                    f"Metric '{metric_name}' validation failed: "
                    f"validator returned False for value {actual}"
                )
        else:
            # Direct comparison
            if actual != expected:
                self.fail(
                    f"Metric '{metric_name}' mismatch: "
                    f"expected {expected}, got {actual}"
                )

    @contextmanager
    def assert_no_side_effects(
        self,
        obj: Any | None = None,
        except_mutations: list[str] | None = None
    ):
        """
        Context manager to assert function has no side effects.

        Validates function purity by checking that no state was mutated
        during execution. Useful for testing domain logic and pure functions.

        :param obj: Object to monitor for mutations (optional)
        :type obj: Optional[Any]
        :param except_mutations: List of allowed mutation paths
        :type except_mutations: Optional[List[str]]
        :yields: None
        :raises AssertionError: If unexpected mutations detected

        Example::

            # Assert complete purity
            with self.assert_no_side_effects():
                result = calculate_price(cart)

            # Allow specific mutations
            with self.assert_no_side_effects(
                obj=self.repository,
                except_mutations=['_storage']
            ):
                user = usecase.execute(data)
                # Repository can mutate _storage, nothing else
        """
        except_mutations = except_mutations or []

        # Take baseline snapshot
        baseline = self._capture_state(obj) if obj else None

        try:
            yield
        finally:
            # Check for mutations
            if obj:
                current = self._capture_state(obj)
                mutations = self._find_mutations(
                    baseline,
                    current,
                    except_mutations
                )

                if mutations:
                    msg = (
                        "\nUnexpected side effects detected:\n"
                        + "\n".join(f"  - {m}" for m in mutations)
                    )
                    self.fail(msg)

    def _capture_state(self, obj: Any) -> dict[str, Any]:
        """
        Capture current state of an object.

        :param obj: Object to capture
        :type obj: Any
        :return: State snapshot
        :rtype: Dict[str, Any]
        """
        state = {}

        # Capture attributes
        if hasattr(obj, '__dict__'):
            for key, value in obj.__dict__.items():
                if not key.startswith('_test_') and not callable(value):
                    try:
                        state[key] = copy.deepcopy(value)
                    except Exception:
                        # Can't deepcopy, store reference
                        state[key] = id(value)

        return state

    def _find_mutations(
        self,
        baseline: dict[str, Any],
        current: dict[str, Any],
        exceptions: list[str]
    ) -> list[str]:
        """
        Find mutations between baseline and current state.

        :param baseline: Initial state
        :type baseline: Dict[str, Any]
        :param current: Current state
        :type current: Dict[str, Any]
        :param exceptions: Allowed mutation paths
        :type exceptions: List[str]
        :return: List of mutation descriptions
        :rtype: List[str]
        """
        mutations = []

        # Check for changed values
        for key in baseline:
            if key in exceptions:
                continue

            if key not in current:
                mutations.append(f"Attribute '{key}' was removed")
            elif baseline[key] != current[key]:
                mutations.append(
                    f"Attribute '{key}' was mutated: "
                    f"{baseline[key]} → {current[key]}"
                )

        # Check for new attributes
        for key in current:
            if key not in baseline and key not in exceptions:
                mutations.append(f"Attribute '{key}' was added")

        return mutations

    def capture_metric(self, name: str, value: Any) -> None:
        """
        Manually capture a metric for testing.

        Useful when testing code that emits metrics but you want to
        validate them later.

        :param name: Metric name
        :type name: str
        :param value: Metric value
        :type value: Any

        Example::

            def test_metrics_emission(self):
                self.capture_metric('test.counter', 1)
                self.capture_metric('test.gauge', 42.5)

                self.assert_metrics_collected({
                    'test.counter': 1,
                    'test.gauge': 42.5
                })
        """
        self._captured_metrics[name] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Get value from test context.

        :param key: Context key
        :type key: str
        :param default: Default value if key not found
        :type default: Any
        :return: Context value
        :rtype: Any
        """
        return self._test_context.get(key, default)

    def __repr__(self) -> str:
        """String representation."""
        return f"<ForgeTestCase {self._testMethodName}>"
