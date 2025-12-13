"""
Intent Tracking & Validation for Cognitive Coherence.

Tracks the relationship between ForgeProcess intentions and ForgeBase execution,
enabling validation of cognitive coherence and learning from execution patterns.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import difflib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CoherenceLevel(Enum):
    """Coherence level between intent and execution."""

    PERFECT = "perfect"  # 100% match
    HIGH = "high"  # 80-99% match
    MEDIUM = "medium"  # 60-79% match
    LOW = "low"  # 40-59% match
    DIVERGENT = "divergent"  # < 40% match


@dataclass
class IntentRecord:
    """
    Record of captured intention.

    :ivar id: Unique intent identifier
    :vartype id: str
    :ivar description: Intent description
    :vartype description: str
    :ivar expected_outcome: What should happen
    :vartype expected_outcome: str
    :ivar timestamp: When intent was captured
    :vartype timestamp: float
    :ivar context: Additional context
    :vartype context: Dict[str, Any]
    :ivar source: Source of intent (user, ai, system)
    :vartype source: str
    """

    id: str
    description: str
    expected_outcome: str
    timestamp: float = field(default_factory=time.time)
    context: dict[str, Any] = field(default_factory=dict)
    source: str = "system"


@dataclass
class ExecutionRecord:
    """
    Record of actual execution.

    :ivar intent_id: Associated intent ID
    :vartype intent_id: str
    :ivar actual_outcome: What actually happened
    :vartype actual_outcome: str
    :ivar success: Whether execution succeeded
    :vartype success: bool
    :ivar timestamp: When execution occurred
    :vartype timestamp: float
    :ivar duration_ms: Execution duration
    :vartype duration_ms: float
    :ivar artifacts: Artifacts produced
    :vartype artifacts: Dict[str, Any]
    """

    intent_id: str
    actual_outcome: str
    success: bool
    timestamp: float = field(default_factory=time.time)
    duration_ms: float = 0.0
    artifacts: dict[str, Any] = field(default_factory=dict)


@dataclass
class CoherenceReport:
    """
    Report on cognitive coherence.

    :ivar intent_id: Intent identifier
    :vartype intent_id: str
    :ivar coherence_level: Level of coherence
    :vartype coherence_level: CoherenceLevel
    :ivar similarity_score: Similarity score (0-1)
    :vartype similarity_score: float
    :ivar matches: What matched
    :vartype matches: List[str]
    :ivar divergences: What diverged
    :vartype divergences: List[str]
    :ivar recommendations: Recommendations for improvement
    :vartype recommendations: List[str]
    """

    intent_id: str
    coherence_level: CoherenceLevel
    similarity_score: float
    matches: list[str] = field(default_factory=list)
    divergences: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


class IntentTracker:
    """
    Tracks and validates cognitive coherence between intent and execution.

    Enables ForgeProcess to understand how well its intentions are being
    executed by ForgeBase, creating a feedback loop for continuous improvement.

    Features:
        - Intent capture and storage
        - Execution tracking
        - Similarity analysis (intent vs execution)
        - Coherence validation
        - Learning data export
        - Pattern detection

    Example::

        tracker = IntentTracker()

        # Capture intent
        intent_id = tracker.capture_intent(
            description="Create user with email validation",
            expected_outcome="User created with validated email",
            source="forgeprocess"
        )

        # Execute
        start = time.time()
        try:
            user = create_user_with_validation(email="test@example.com")
            outcome = f"User {user.id} created successfully"
            success = True
        except Exception as e:
            outcome = f"Failed: {e}"
            success = False

        duration = (time.time() - start) * 1000

        # Record execution
        tracker.record_execution(
            intent_id=intent_id,
            actual_outcome=outcome,
            success=success,
            duration_ms=duration
        )

        # Validate coherence
        report = tracker.validate_coherence(intent_id)
        print(f"Coherence: {report.coherence_level.value}")
        print(f"Similarity: {report.similarity_score:.2%}")

        if report.divergences:
            print("Divergences:")
            for div in report.divergences:
                print(f"  - {div}")

    :ivar _intents: Stored intent records
    :vartype _intents: Dict[str, IntentRecord]
    :ivar _executions: Stored execution records
    :vartype _executions: Dict[str, ExecutionRecord]
    """

    def __init__(self):
        """Initialize intent tracker."""
        self._intents: dict[str, IntentRecord] = {}
        self._executions: dict[str, ExecutionRecord] = {}

    def capture_intent(
        self,
        description: str,
        expected_outcome: str,
        source: str = "system",
        **context: Any
    ) -> str:
        """
        Capture an intention before execution.

        :param description: What is intended
        :type description: str
        :param expected_outcome: What should happen
        :type expected_outcome: str
        :param source: Source of intent
        :type source: str
        :param context: Additional context
        :type context: Any
        :return: Intent identifier
        :rtype: str

        Example::

            intent_id = tracker.capture_intent(
                description="Validate email format and save user",
                expected_outcome="User saved with valid email",
                source="forgeprocess",
                operation="create_user",
                actor="api_client"
            )
        """
        import uuid
        intent_id = str(uuid.uuid4())

        intent = IntentRecord(
            id=intent_id,
            description=description,
            expected_outcome=expected_outcome,
            source=source,
            context=context
        )

        self._intents[intent_id] = intent
        return intent_id

    def record_execution(
        self,
        intent_id: str,
        actual_outcome: str,
        success: bool,
        duration_ms: float = 0.0,
        **artifacts: Any
    ) -> None:
        """
        Record actual execution results.

        :param intent_id: Associated intent ID
        :type intent_id: str
        :param actual_outcome: What actually happened
        :type actual_outcome: str
        :param success: Whether execution succeeded
        :type success: bool
        :param duration_ms: Execution duration in milliseconds
        :type duration_ms: float
        :param artifacts: Execution artifacts (IDs, data, etc.)
        :type artifacts: Any

        Example::

            tracker.record_execution(
                intent_id=intent_id,
                actual_outcome="User abc123 created successfully",
                success=True,
                duration_ms=45.2,
                user_id="abc123",
                email="test@example.com"
            )
        """
        if intent_id not in self._intents:
            raise ValueError(f"Intent {intent_id} not found")

        execution = ExecutionRecord(
            intent_id=intent_id,
            actual_outcome=actual_outcome,
            success=success,
            duration_ms=duration_ms,
            artifacts=artifacts
        )

        self._executions[intent_id] = execution

    def validate_coherence(
        self,
        intent_id: str,
        threshold: float = 0.6
    ) -> CoherenceReport:
        """
        Validate cognitive coherence between intent and execution.

        :param intent_id: Intent to validate
        :type intent_id: str
        :param threshold: Minimum similarity threshold
        :type threshold: float
        :return: Coherence report
        :rtype: CoherenceReport

        Example::

            report = tracker.validate_coherence(intent_id)

            if report.coherence_level == CoherenceLevel.DIVERGENT:
                print("WARNING: Intent and execution diverged!")
                for div in report.divergences:
                    print(f"  - {div}")
        """
        if intent_id not in self._intents:
            raise ValueError(f"Intent {intent_id} not found")

        if intent_id not in self._executions:
            raise ValueError(f"Execution for intent {intent_id} not found")

        intent = self._intents[intent_id]
        execution = self._executions[intent_id]

        # Calculate similarity
        similarity = self._calculate_similarity(
            intent.expected_outcome,
            execution.actual_outcome
        )

        # Determine coherence level
        if similarity >= 0.95:
            level = CoherenceLevel.PERFECT
        elif similarity >= 0.80:
            level = CoherenceLevel.HIGH
        elif similarity >= 0.60:
            level = CoherenceLevel.MEDIUM
        elif similarity >= 0.40:
            level = CoherenceLevel.LOW
        else:
            level = CoherenceLevel.DIVERGENT

        # Analyze matches and divergences
        matches, divergences = self._analyze_differences(
            intent.expected_outcome,
            execution.actual_outcome
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            intent,
            execution,
            level,
            similarity
        )

        return CoherenceReport(
            intent_id=intent_id,
            coherence_level=level,
            similarity_score=similarity,
            matches=matches,
            divergences=divergences,
            recommendations=recommendations
        )

    def _calculate_similarity(self, expected: str, actual: str) -> float:
        """
        Calculate similarity between expected and actual outcomes.

        Uses sequence matching to determine how similar the outcomes are.

        :param expected: Expected outcome
        :type expected: str
        :param actual: Actual outcome
        :type actual: str
        :return: Similarity score (0-1)
        :rtype: float
        """
        return difflib.SequenceMatcher(
            None,
            expected.lower(),
            actual.lower()
        ).ratio()

    def _analyze_differences(
        self,
        expected: str,
        actual: str
    ) -> tuple[list[str], list[str]]:
        """
        Analyze differences between expected and actual.

        :param expected: Expected outcome
        :type expected: str
        :param actual: Actual outcome
        :type actual: str
        :return: (matches, divergences)
        :rtype: Tuple[List[str], List[str]]
        """
        # Simple word-based analysis
        expected_words = set(expected.lower().split())
        actual_words = set(actual.lower().split())

        common = expected_words & actual_words
        missing = expected_words - actual_words
        unexpected = actual_words - expected_words

        matches = [f"Common terms: {', '.join(common)}"] if common else []

        divergences = []
        if missing:
            divergences.append(f"Missing from execution: {', '.join(missing)}")
        if unexpected:
            divergences.append(f"Unexpected in execution: {', '.join(unexpected)}")

        return matches, divergences

    def _generate_recommendations(
        self,
        intent: IntentRecord,
        execution: ExecutionRecord,
        level: CoherenceLevel,
        similarity: float
    ) -> list[str]:
        """
        Generate recommendations for improving coherence.

        :param intent: Intent record
        :type intent: IntentRecord
        :param execution: Execution record
        :type execution: ExecutionRecord
        :param level: Coherence level
        :type level: CoherenceLevel
        :param similarity: Similarity score
        :type similarity: float
        :return: List of recommendations
        :rtype: List[str]
        """
        recommendations = []

        if level == CoherenceLevel.DIVERGENT:
            recommendations.append(
                "HIGH PRIORITY: Significant divergence detected. "
                "Review implementation against intent."
            )

        if level in (CoherenceLevel.LOW, CoherenceLevel.MEDIUM):
            recommendations.append(
                "Review and align implementation with intent description."
            )

        if not execution.success:
            recommendations.append(
                "Execution failed. Review error handling and validation."
            )

        if execution.duration_ms > 1000:
            recommendations.append(
                f"Execution took {execution.duration_ms:.0f}ms. "
                "Consider performance optimization."
            )

        if similarity < 0.8 and execution.success:
            recommendations.append(
                "Update outcome messages to better reflect intent."
            )

        return recommendations

    def get_intent(self, intent_id: str) -> IntentRecord:
        """
        Get intent record.

        :param intent_id: Intent identifier
        :type intent_id: str
        :return: Intent record
        :rtype: IntentRecord
        """
        if intent_id not in self._intents:
            raise ValueError(f"Intent {intent_id} not found")
        return self._intents[intent_id]

    def get_execution(self, intent_id: str) -> ExecutionRecord:
        """
        Get execution record.

        :param intent_id: Intent identifier
        :type intent_id: str
        :return: Execution record
        :rtype: ExecutionRecord
        """
        if intent_id not in self._executions:
            raise ValueError(f"Execution for intent {intent_id} not found")
        return self._executions[intent_id]

    def get_all_intents(self) -> list[IntentRecord]:
        """
        Get all intent records.

        :return: List of intent records
        :rtype: List[IntentRecord]
        """
        return list(self._intents.values())

    def get_coherence_stats(self) -> dict[str, Any]:
        """
        Get overall coherence statistics.

        :return: Statistics dictionary
        :rtype: Dict[str, Any]

        Example::

            stats = tracker.get_coherence_stats()
            print(f"Total intents: {stats['total_intents']}")
            print(f"Average coherence: {stats['avg_similarity']:.2%}")
            print(f"Success rate: {stats['success_rate']:.2%}")
        """
        if not self._intents:
            return {
                'total_intents': 0,
                'total_executions': 0,
                'avg_similarity': 0.0,
                'success_rate': 0.0,
                'coherence_distribution': {}
            }

        # Calculate statistics
        total_intents = len(self._intents)
        total_executions = len(self._executions)

        similarities = []
        successes = []
        coherence_counts = {level: 0 for level in CoherenceLevel}

        for intent_id in self._executions:
            report = self.validate_coherence(intent_id)
            similarities.append(report.similarity_score)
            coherence_counts[report.coherence_level] += 1

            execution = self._executions[intent_id]
            successes.append(execution.success)

        avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0
        success_rate = sum(successes) / len(successes) if successes else 0.0

        return {
            'total_intents': total_intents,
            'total_executions': total_executions,
            'avg_similarity': avg_similarity,
            'success_rate': success_rate,
            'coherence_distribution': {
                level.value: count
                for level, count in coherence_counts.items()
            }
        }

    def export_learning_data(self) -> list[dict[str, Any]]:
        """
        Export data for machine learning / analysis.

        :return: List of learning examples
        :rtype: List[Dict[str, Any]]

        Example::

            data = tracker.export_learning_data()

            # Save to JSON for analysis
            import json
            with open("learning_data.json", "w") as f:
                json.dump(data, f, indent=2)
        """
        learning_data = []

        for intent_id, execution in self._executions.items():
            intent = self._intents[intent_id]
            report = self.validate_coherence(intent_id)

            learning_data.append({
                'intent': {
                    'description': intent.description,
                    'expected_outcome': intent.expected_outcome,
                    'source': intent.source,
                    'context': intent.context
                },
                'execution': {
                    'actual_outcome': execution.actual_outcome,
                    'success': execution.success,
                    'duration_ms': execution.duration_ms,
                    'artifacts': execution.artifacts
                },
                'coherence': {
                    'level': report.coherence_level.value,
                    'similarity_score': report.similarity_score,
                    'matches': report.matches,
                    'divergences': report.divergences
                }
            })

        return learning_data

    def clear(self) -> None:
        """Clear all tracked data."""
        self._intents.clear()
        self._executions.clear()
