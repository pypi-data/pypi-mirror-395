"""
Feedback loop management system for cognitive coherence.

Manages feedback loops between ForgeProcess (intent) and ForgeBase (execution),
enabling cognitive systems to learn from execution patterns and validate
intention-execution alignment.

Philosophy:
    Cognitive systems must maintain coherence between what they intend to do
    and what actually happens. This requires:

    1. **Intent Capture**: Recording what the system meant to accomplish
    2. **Execution Tracking**: Recording what actually happened
    3. **Mapping**: Linking intention to execution
    4. **Learning**: Extracting patterns for improvement
    5. **Validation**: Checking cognitive coherence

    This feedback loop enables self-reflection and continuous improvement,
    distinguishing cognitive systems from mere automation.

Use Cases:
    - AI agent learning from execution patterns
    - Debugging intent-execution mismatches
    - Training data collection for system improvement
    - Cognitive coherence validation
    - ForgeProcess ↔ ForgeBase synchronization

Example::

    feedback = FeedbackManager()

    # Capture intent
    intent_id = feedback.capture_intent(
        intent="Create new user with email validation",
        context={"operation": "user_creation", "actor": "api"}
    )

    # Track execution
    with feedback.track_execution(intent_id):
        try:
            user = create_user(email="test@example.com")
            feedback.record_success(intent_id, user_id=user.id)
        except Exception as e:
            feedback.record_failure(intent_id, error=str(e))

    # Analyze feedback
    coherence = feedback.check_coherence(intent_id)
    if not coherence.aligned:
        print(f"Misalignment detected: {coherence.reason}")

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ExecutionStatus(Enum):
    """Execution status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


@dataclass
class Intent:
    """
    Represents a captured intention.

    An intent describes what the system intends to accomplish, captured
    before execution begins.

    :ivar id: Unique intent identifier
    :vartype id: str
    :ivar description: Human-readable intent description
    :vartype description: str
    :ivar timestamp: When intent was captured
    :vartype timestamp: float
    :ivar context: Additional context about the intent
    :vartype context: Dict[str, Any]
    :ivar expected_outcomes: Expected outcomes
    :vartype expected_outcomes: List[str]
    """

    id: str
    description: str
    timestamp: float = field(default_factory=time.time)
    context: dict[str, Any] = field(default_factory=dict)
    expected_outcomes: list[str] = field(default_factory=list)


@dataclass
class Execution:
    """
    Represents an execution trace.

    Tracks what actually happened during execution of an intent.

    :ivar intent_id: Associated intent identifier
    :vartype intent_id: str
    :ivar status: Execution status
    :vartype status: ExecutionStatus
    :ivar start_time: Execution start time
    :vartype start_time: float
    :ivar end_time: Execution end time
    :vartype end_time: Optional[float]
    :ivar outcomes: Actual outcomes
    :vartype outcomes: List[str]
    :ivar metrics: Execution metrics
    :vartype metrics: Dict[str, Any]
    :ivar errors: Errors encountered
    :vartype errors: List[str]
    :ivar trace: Detailed execution trace
    :vartype trace: List[Dict[str, Any]]
    """

    intent_id: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    outcomes: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)

    def duration_ms(self) -> float:
        """Get execution duration in milliseconds."""
        if self.end_time is None:
            return (time.time() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000


@dataclass
class CoherenceCheck:
    """
    Result of cognitive coherence validation.

    Compares intent against execution to determine alignment.

    :ivar aligned: Whether intent and execution are aligned
    :vartype aligned: bool
    :ivar confidence: Confidence score (0-1)
    :vartype confidence: float
    :ivar reason: Explanation of alignment/misalignment
    :vartype reason: str
    :ivar differences: Specific differences detected
    :vartype differences: List[str]
    """

    aligned: bool
    confidence: float
    reason: str
    differences: list[str] = field(default_factory=list)


class FeedbackManager:
    """
    Manages feedback loops between intent and execution.

    Tracks the relationship between what a cognitive system intends to do
    and what actually happens, enabling learning and coherence validation.

    Features:
        - Intent capture and storage
        - Execution tracking with detailed traces
        - Intent-execution mapping
        - Cognitive coherence validation
        - Learning data export
        - Pattern analysis

    :ivar _intents: Stored intents
    :vartype _intents: Dict[str, Intent]
    :ivar _executions: Stored executions
    :vartype _executions: Dict[str, List[Execution]]
    :ivar _current_execution: Currently active execution
    :vartype _current_execution: Optional[Execution]

    Example::

        feedback = FeedbackManager()

        # Capture intent
        intent_id = feedback.capture_intent(
            "Validate user email and send confirmation",
            expected_outcomes=["email_validated", "confirmation_sent"]
        )

        # Track execution
        with feedback.track_execution(intent_id) as execution:
            validate_email()
            execution.add_outcome("email_validated")

            send_confirmation()
            execution.add_outcome("confirmation_sent")

        # Check coherence
        check = feedback.check_coherence(intent_id)
        assert check.aligned, f"Intent-execution mismatch: {check.reason}"
    """

    def __init__(self):
        """Initialize feedback manager."""
        self._intents: dict[str, Intent] = {}
        self._executions: dict[str, list[Execution]] = {}
        self._current_execution: Execution | None = None

    def capture_intent(
        self,
        description: str,
        expected_outcomes: list[str] | None = None,
        **context: Any
    ) -> str:
        """
        Capture an intention before execution.

        :param description: Human-readable intent description
        :type description: str
        :param expected_outcomes: Expected outcomes
        :type expected_outcomes: Optional[List[str]]
        :param context: Additional context
        :type context: Any
        :return: Intent identifier
        :rtype: str

        Example::

            intent_id = feedback.capture_intent(
                "Create user account with admin privileges",
                expected_outcomes=["user_created", "admin_role_assigned"],
                requested_by="admin_user_123",
                priority="high"
            )
        """
        intent_id = str(uuid.uuid4())

        intent = Intent(
            id=intent_id,
            description=description,
            context=context,
            expected_outcomes=expected_outcomes or []
        )

        self._intents[intent_id] = intent
        return intent_id

    def start_execution(self, intent_id: str) -> Execution:
        """
        Start tracking execution for an intent.

        :param intent_id: Intent identifier
        :type intent_id: str
        :return: Execution tracker
        :rtype: Execution

        Example::

            intent_id = feedback.capture_intent("Process payment")
            execution = feedback.start_execution(intent_id)
        """
        execution = Execution(
            intent_id=intent_id,
            status=ExecutionStatus.IN_PROGRESS
        )

        if intent_id not in self._executions:
            self._executions[intent_id] = []

        self._executions[intent_id].append(execution)
        self._current_execution = execution

        return execution

    def record_success(self, intent_id: str, **outcomes: Any) -> None:
        """
        Record successful execution.

        :param intent_id: Intent identifier
        :type intent_id: str
        :param outcomes: Outcomes achieved
        :type outcomes: Any

        Example::

            feedback.record_success(
                intent_id,
                user_id="user-123",
                email_sent=True
            )
        """
        executions = self._executions.get(intent_id, [])
        if executions:
            execution = executions[-1]
            execution.status = ExecutionStatus.SUCCESS
            execution.end_time = time.time()
            execution.metrics.update(outcomes)
            execution.outcomes.extend(outcomes.keys())

    def record_failure(self, intent_id: str, error: str, **context: Any) -> None:
        """
        Record failed execution.

        :param intent_id: Intent identifier
        :type intent_id: str
        :param error: Error description
        :type error: str
        :param context: Additional error context
        :type context: Any

        Example::

            feedback.record_failure(
                intent_id,
                error="Database connection timeout",
                retry_count=3,
                last_error_code=500
            )
        """
        executions = self._executions.get(intent_id, [])
        if executions:
            execution = executions[-1]
            execution.status = ExecutionStatus.FAILURE
            execution.end_time = time.time()
            execution.errors.append(error)
            execution.metrics.update(context)

    def add_trace_point(self, intent_id: str, operation: str, **data: Any) -> None:
        """
        Add trace point to current execution.

        :param intent_id: Intent identifier
        :type intent_id: str
        :param operation: Operation name
        :type operation: str
        :param data: Operation data
        :type data: Any

        Example::

            feedback.add_trace_point(
                intent_id,
                "database_query",
                query="SELECT * FROM users",
                duration_ms=45
            )
        """
        executions = self._executions.get(intent_id, [])
        if executions:
            execution = executions[-1]
            trace_point = {
                'timestamp': time.time(),
                'operation': operation,
                'data': data
            }
            execution.trace.append(trace_point)

    def check_coherence(self, intent_id: str) -> CoherenceCheck:
        """
        Check cognitive coherence between intent and execution.

        Validates that what was intended aligns with what happened.

        :param intent_id: Intent identifier
        :type intent_id: str
        :return: Coherence check result
        :rtype: CoherenceCheck

        Example::

            check = feedback.check_coherence(intent_id)
            if not check.aligned:
                logger.warning(f"Coherence issue: {check.reason}")
                for diff in check.differences:
                    logger.warning(f"  - {diff}")
        """
        intent = self._intents.get(intent_id)
        executions = self._executions.get(intent_id, [])

        if not intent:
            return CoherenceCheck(
                aligned=False,
                confidence=0.0,
                reason="Intent not found"
            )

        if not executions:
            return CoherenceCheck(
                aligned=False,
                confidence=0.0,
                reason="No execution recorded"
            )

        execution = executions[-1]  # Check most recent execution

        # Check if execution completed
        if execution.status == ExecutionStatus.PENDING:
            return CoherenceCheck(
                aligned=False,
                confidence=0.0,
                reason="Execution not completed"
            )

        # Check expected outcomes
        differences = []
        expected = set(intent.expected_outcomes)
        actual = set(execution.outcomes)

        missing = expected - actual
        unexpected = actual - expected

        if missing:
            differences.append(f"Missing expected outcomes: {', '.join(missing)}")

        if unexpected:
            differences.append(f"Unexpected outcomes: {', '.join(unexpected)}")

        # Check for failures
        if execution.status == ExecutionStatus.FAILURE:
            differences.append(f"Execution failed: {execution.errors}")

        # Calculate alignment
        if not differences:
            return CoherenceCheck(
                aligned=True,
                confidence=1.0,
                reason="Intent and execution fully aligned"
            )

        # Partial alignment
        if expected and actual:
            overlap = len(expected & actual)
            total = len(expected | actual)
            confidence = overlap / total
        else:
            confidence = 0.0

        return CoherenceCheck(
            aligned=False,
            confidence=confidence,
            reason="Intent-execution misalignment detected",
            differences=differences
        )

    def get_learning_data(self, intent_id: str) -> dict[str, Any]:
        """
        Export learning data for analysis.

        :param intent_id: Intent identifier
        :type intent_id: str
        :return: Learning data package
        :rtype: Dict[str, Any]

        Example::

            data = feedback.get_learning_data(intent_id)
            # Send to ML training pipeline
            training_service.ingest(data)
        """
        intent = self._intents.get(intent_id)
        executions = self._executions.get(intent_id, [])

        if not intent:
            return {}

        return {
            'intent': {
                'id': intent.id,
                'description': intent.description,
                'expected_outcomes': intent.expected_outcomes,
                'context': intent.context
            },
            'executions': [
                {
                    'status': ex.status.value,
                    'duration_ms': ex.duration_ms(),
                    'outcomes': ex.outcomes,
                    'errors': ex.errors,
                    'metrics': ex.metrics,
                    'trace': ex.trace
                }
                for ex in executions
            ],
            'coherence': self.check_coherence(intent_id).__dict__
        }

    def get_all_intents(self) -> list[Intent]:
        """
        Get all captured intents.

        :return: List of intents
        :rtype: List[Intent]
        """
        return list(self._intents.values())

    def get_statistics(self) -> dict[str, Any]:
        """
        Get feedback system statistics.

        :return: Statistics dictionary
        :rtype: Dict[str, Any]
        """
        total_intents = len(self._intents)
        total_executions = sum(len(exs) for exs in self._executions.values())

        successful = 0
        failed = 0
        aligned = 0

        for intent_id in self._intents:
            executions = self._executions.get(intent_id, [])
            if executions:
                if executions[-1].status == ExecutionStatus.SUCCESS:
                    successful += 1
                elif executions[-1].status == ExecutionStatus.FAILURE:
                    failed += 1

                coherence = self.check_coherence(intent_id)
                if coherence.aligned:
                    aligned += 1

        return {
            'total_intents': total_intents,
            'total_executions': total_executions,
            'successful_executions': successful,
            'failed_executions': failed,
            'aligned_intents': aligned,
            'alignment_rate': aligned / total_intents if total_intents > 0 else 0.0
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"<FeedbackManager intents={len(self._intents)} executions={sum(len(e) for e in self._executions.values())}>"
