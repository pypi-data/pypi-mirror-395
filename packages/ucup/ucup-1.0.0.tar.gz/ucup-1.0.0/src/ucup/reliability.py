"""
Reliability and recovery systems for UCUP Framework.

This module provides comprehensive tools for detecting failures, recovering
automatically, checkpointing state, and degrading gracefully when perfect
performance isn't possible.
"""

import asyncio
import inspect
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set, Type, Union
from collections import defaultdict
import traceback

import numpy as np


@dataclass
class FailureIndicator:
    """Indicator of a potential failure in agent execution."""
    failure_type: str
    severity: str  # "low", "medium", "high", "critical"
    description: str
    evidence: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    agent_id: Optional[str] = None
    recoverable: bool = True
    confidence: float = 0.8

    def to_dict(self) -> Dict[str, Any]:
        return {
            "failure_type": self.failure_type,
            "severity": self.severity,
            "description": self.description,
            "evidence": self.evidence,
            "timestamp": self.timestamp.isoformat(),
            "agent_id": self.agent_id,
            "recoverable": self.recoverable,
            "confidence": self.confidence
        }


@dataclass
class FailurePattern:
    """Pattern for detecting specific types of failures."""
    pattern_name: str
    detection_function: Callable
    severity: str = "medium"
    description: str = ""
    required_evidence: List[str] = field(default_factory=list)

    def matches(self, context: Dict[str, Any]) -> Optional[FailureIndicator]:
        """Check if this failure pattern matches the given context."""
        try:
            return self.detection_function(context)
        except Exception as e:
            logging.warning(f"Failure pattern {self.pattern_name} failed: {e}")
            return None


@dataclass
class AgentCheckpoint:
    """Checkpoint of agent state for rollback purposes."""
    checkpoint_id: str
    agent_state: Dict[str, Any]
    decision_point: str
    alternatives_considered: List[Dict[str, Any]]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "decision_point": self.decision_point,
            "alternatives_considered": self.alternatives_considered,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class RecoveryAttempt:
    """Record of a recovery attempt."""
    attempt_id: str
    failure_indicator: FailureIndicator
    recovery_strategy: str
    result: str  # "success", "partial_success", "failed"
    timestamp: datetime = field(default_factory=datetime.now)
    duration: float = 0.0
    new_state: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class FailureDetector:
    """
    Multi-layer failure detection system.

    Monitors agent execution for various types of failures:
    - Reasoning failures (circular thinking, contradictions)
    - Execution failures (timeouts, exceptions)
    - Progress failures (stalled execution)
    - Behavioral anomalies (unexpected agent behavior)
    """

    def __init__(self):
        self.failure_patterns: List[FailurePattern] = []
        self.register_default_patterns()
        self.detection_history: List[FailureIndicator] = []
        self.logger = logging.getLogger(__name__)

    def register_default_patterns(self):
        """Register the default set of failure detection patterns."""

        self.failure_patterns = [
            FailurePattern(
                pattern_name="circular_reasoning",
                detection_function=self._detect_circular_reasoning,
                severity="high",
                description="Agent is stuck in circular reasoning loops",
                required_evidence=["recent_decisions", "decision_history"]
            ),
            FailurePattern(
                pattern_name="contradiction_detector",
                detection_function=self._detect_contradictions,
                severity="high",
                description="Agent has made contradictory statements",
                required_evidence=["reasoning_trace"]
            ),
            FailurePattern(
                pattern_name="confidence_collapse",
                detection_function=self._detect_confidence_collapse,
                severity="medium",
                description="Agent confidence dropping rapidly",
                required_evidence=["confidence_history"]
            ),
            FailurePattern(
                pattern_name="hallucination_detector",
                detection_function=self._detect_hallucinations,
                severity="critical",
                description="Agent may be generating false information",
                required_evidence=["fact_checker", "response_content"]
            ),
            FailurePattern(
                pattern_name="timeout_failure",
                detection_function=self._detect_timeout,
                severity="medium",
                description="Agent execution timed out",
                required_evidence=["execution_time", "timeout_limit"]
            ),
            FailurePattern(
                pattern_name="progress_stall",
                detection_function=self._detect_progress_stall,
                severity="medium",
                description="Agent appears to be making no progress",
                required_evidence=["recent_activity", "last_progress_timestamp"]
            )
        ]

    async def detect_failures(self, agent_session: Dict[str, Any]) -> List[FailureIndicator]:
        """
        Detect all applicable failures in the given agent session.

        Args:
            agent_session: Dictionary containing agent state, history, and context

        Returns:
            List of detected failure indicators
        """

        failures = []

        for pattern in self.failure_patterns:
            # Check if all required evidence is available
            if self._has_required_evidence(agent_session, pattern):
                failure = pattern.matches(agent_session)
                if failure:
                    failures.append(failure)
                    self.detection_history.append(failure)

        # Also check for domain-specific failures if context provides
        domain_failures = await self._detect_domain_specific_failures(agent_session)
        failures.extend(domain_failures)

        return failures

    def _has_required_evidence(
        self,
        agent_session: Dict[str, Any],
        pattern: FailurePattern
    ) -> bool:
        """Check if agent session has the required evidence for pattern detection."""

        for evidence_key in pattern.required_evidence:
            if evidence_key not in agent_session:
                return False
        return True

    def _detect_circular_reasoning(self, context: Dict[str, Any]) -> Optional[FailureIndicator]:
        """Detect circular reasoning patterns."""

        decisions = context.get("recent_decisions", [])
        decision_history = context.get("decision_history", [])

        if len(decisions) < 3:
            return None

        # Look for repeating decision patterns in last few steps
        recent_decisions = [d.get("chosen_action") for d in decisions[-10:] if d.get("chosen_action")]

        # Check for cycles
        for cycle_length in range(2, min(6, len(recent_decisions) // 2 + 1)):
            for i in range(len(recent_decisions) - 2 * cycle_length + 1):
                if (recent_decisions[i:i + cycle_length] ==
                    recent_decisions[i + cycle_length:i + 2 * cycle_length]):
                    return FailureIndicator(
                        failure_type="circular_reasoning",
                        severity="high",
                        description=f"Detected {cycle_length}-step circular reasoning",
                        evidence={
                            "cycle_length": cycle_length,
                            "cycle_actions": recent_decisions[i:i + cycle_length],
                            "total_recent_decisions": len(recent_decisions)
                        },
                        agent_id=context.get("agent_id"),
                        confidence=0.9
                    )

        return None

    def _detect_contradictions(self, context: Dict[str, Any]) -> Optional[FailureIndicator]:
        """Detect contradictory statements in reasoning."""

        reasoning_trace = context.get("reasoning_trace", [])

        if not reasoning_trace:
            return None

        # Simple contradiction detection - would need NLP in real implementation
        statements = []
        for trace in reasoning_trace:
            if isinstance(trace, dict) and "statement" in trace:
                statements.append(trace["statement"])
            elif isinstance(trace, str):
                statements.append(trace)

        # Look for obvious contradictions
        contradictions = []
        for i, stmt1 in enumerate(statements):
            for stmt2 in statements[i+1:]:
                if self._are_contradictory(stmt1, stmt2):
                    contradictions.append((stmt1, stmt2))

        if contradictions:
            return FailureIndicator(
                failure_type="contradictory_statements",
                severity="high",
                description=f"Found {len(contradictions)} contradictory statements",
                evidence={
                    "contradictions": contradictions[:5],  # Limit for readability
                    "total_contradictions": len(contradictions)
                },
                confidence=0.85
            )

        return None

    def _are_contradictory(self, stmt1: str, stmt2: str) -> bool:
        """Check if two statements are contradictory. Simplified implementation."""

        stmt1_lower = stmt1.lower()
        stmt2_lower = stmt2.lower()

        # Simple contradiction patterns (would need NLP for real implementation)
        contradiction_pairs = [
            ("yes", "no"),
            ("true", "false"),
            ("correct", "incorrect"),
            ("valid", "invalid"),
            ("should", "should not"),
            ("will", "will not")
        ]

        for pos, neg in contradiction_pairs:
            if (pos in stmt1_lower and neg in stmt2_lower) or \
               (neg in stmt1_lower and pos in stmt2_lower):
                return True

        return False

    def _detect_confidence_collapse(self, context: Dict[str, Any]) -> Optional[FailureIndicator]:
        """Detect rapid confidence decreases."""

        confidence_history = context.get("confidence_history", [])

        if len(confidence_history) < 3:
            return None

        recent_confidences = confidence_history[-5:]  # Last 5 confidence scores
        avg_recent = np.mean(recent_confidences)
        avg_earlier = np.mean(confidence_history[:-5]) if len(confidence_history) > 5 else avg_recent

        drop_threshold = 0.3  # 30% drop
        relative_drop = (avg_earlier - avg_recent) / avg_earlier if avg_earlier > 0 else 0

        if relative_drop > drop_threshold:
            return FailureIndicator(
                failure_type="confidence_collapse",
                severity="medium",
                description=f"Confidence dropped by {relative_drop:.1%} in recent steps",
                evidence={
                    "average_recent_confidence": avg_recent,
                    "average_earlier_confidence": avg_earlier,
                    "relative_drop": relative_drop,
                    "recent_confidences": recent_confidences
                },
                confidence=0.8
            )

        return None

    def _detect_hallucinations(self, context: Dict[str, Any]) -> Optional[FailureIndicator]:
        """Detect potential hallucinations using fact checking."""

        fact_checker = context.get("fact_checker")
        response_content = context.get("response_content", "")

        if not fact_checker or not response_content:
            return None

        # This would integrate with actual fact-checking service
        # For demonstration, mock hallucination detection
        mock_hallucination_score = np.random.random()

        if mock_hallucination_score > 0.8:
            return FailureIndicator(
                failure_type="hallucination_detected",
                severity="critical",
                description="High probability of hallucinated content",
                evidence={
                    "hallucination_score": mock_hallucination_score,
                    "checked_content_keywords": ["potentially_false_info"],
                    "fact_check_results": {"verified": False}
                },
                confidence=mock_hallucination_score
            )

        return None

    def _detect_timeout(self, context: Dict[str, Any]) -> Optional[FailureIndicator]:
        """Detect timeout failures."""

        execution_time = context.get("execution_time", 0)
        timeout_limit = context.get("timeout_limit", 30)

        if execution_time > timeout_limit:
            return FailureIndicator(
                failure_type="execution_timeout",
                severity="medium",
                description=f"Execution exceeded timeout limit of {timeout_limit}s",
                evidence={
                    "execution_time": execution_time,
                    "timeout_limit": timeout_limit,
                    "overrun": execution_time - timeout_limit
                },
                confidence=0.95
            )

        return None

    def _detect_progress_stall(self, context: Dict[str, Any]) -> Optional[FailureIndicator]:
        """Detect when agent appears to be making no progress."""

        recent_activity = context.get("recent_activity", [])
        last_progress = context.get("last_progress_timestamp")

        if not recent_activity and last_progress:
            time_since_progress = (datetime.now() - last_progress).total_seconds()
            stall_threshold = 300  # 5 minutes

            if time_since_progress > stall_threshold:
                return FailureIndicator(
                    failure_type="progress_stalled",
                    severity="medium",
                    description=f"No progress for {time_since_progress/60:.1f} minutes",
                    evidence={
                        "time_since_progress": time_since_progress,
                        "stall_threshold": stall_threshold,
                        "last_progress": last_progress.isoformat()
                    },
                    confidence=0.75
                )

        return None

    async def _detect_domain_specific_failures(self, context: Dict[str, Any]) -> List[FailureIndicator]:
        """Detect domain-specific failures based on context."""

        failures = []
        domain = context.get("domain", "")

        if domain == "legal":
            # Legal domain specific failures
            legal_failures = await self._detect_legal_failures(context)
            failures.extend(legal_failures)

        elif domain == "medical":
            # Medical domain specific failures
            medical_failures = await self._detect_medical_failures(context)
            failures.extend(medical_failures)

        return failures

    async def _detect_legal_failures(self, context: Dict[str, Any]) -> List[FailureIndicator]:
        """Detect legal domain-specific failures."""

        # Mock legal failure detection
        response_content = context.get("response_content", "").lower()

        legal_keywords = ["lawsuit", "contract", "liability", "regulation"]
        has_legal_content = any(keyword in response_content for keyword in legal_keywords)

        if has_legal_content:
            confidence = context.get("confidence", 0.5)

            if confidence < 0.7:
                return [FailureIndicator(
                    failure_type="low_confidence_legal_advice",
                    severity="high",
                    description="Low confidence in legal domain response",
                    evidence={"confidence": confidence, "domain": "legal"},
                    confidence=0.8
                )]

        return []

    async def _detect_medical_failures(self, context: Dict[str, Any]) -> List[FailureIndicator]:
        """Detect medical domain-specific failures."""

        # Mock medical failure detection
        response_content = context.get("response_content", "").lower()

        medical_keywords = ["diagnosis", "treatment", "medication", "symptoms"]
        has_medical_content = any(keyword in response_content for keyword in medical_keywords)

        if has_medical_content:
            sources_cited = context.get("sources_cited", [])
            if len(sources_cited) < 2:
                return [FailureIndicator(
                    failure_type="insufficient_medical_sources",
                    severity="high",
                    description="Medical advice given without sufficient authoritative sources",
                    evidence={"sources_cited": sources_cited, "domain": "medical"},
                    confidence=0.9
                )]

        return []


@dataclass
class RecoveryStrategy:
    """Definition of a recovery strategy."""
    name: str
    trigger_condition: Callable[[FailureIndicator], bool]
    action: Callable
    priority: int = 0
    max_attempts: int = 3
    cooldown_seconds: int = 10

    def can_handle(self, failure: FailureIndicator) -> bool:
        """Check if this strategy can handle the given failure."""
        return self.trigger_condition(failure)


class AutomatedRecoveryPipeline:
    """
    Hierarchical automated recovery system.

    Implements multiple recovery strategies of increasing invasiveness:
    1. Retry with clarification
    2. Switch reasoning approach
    3. Escalate to human
    4. Transfer to specialist
    """

    def __init__(self):
        self.recovery_strategies: List[RecoveryStrategy] = []
        self.register_default_strategies()
        self.attempt_history: Dict[str, List[RecoveryAttempt]] = defaultdict(list)
        self.logger = logging.getLogger(__name__)

    def register_default_strategies(self):
        """Register the default recovery strategies."""

        self.recovery_strategies = [
            RecoveryStrategy(
                name="retry_with_clarification",
                trigger_condition=lambda f: f.failure_type in ["low_confidence", "confidence_collapse"],
                action=self._retry_with_clarification,
                priority=1,
                max_attempts=2
            ),
            RecoveryStrategy(
                name="switch_reasoning_approach",
                trigger_condition=lambda f: f.failure_type in ["circular_reasoning", "contradictory_statements"],
                action=self._switch_reasoning_strategy,
                priority=2,
                max_attempts=3
            ),
            RecoveryStrategy(
                name="escalate_to_human",
                trigger_condition=lambda f: f.severity == "critical" or self._is_multiple_attempts(f, 3),
                action=self._escalate_to_human,
                priority=3,
                max_attempts=1
            ),
            RecoveryStrategy(
                name="transfer_to_specialist",
                trigger_condition=lambda f: f.failure_type == "domain_specific_failure",
                action=self._transfer_to_specialist,
                priority=2,
                max_attempts=2
            )
        ]

    async def execute_recovery(
        self,
        failure: FailureIndicator,
        agent_session: Dict[str, Any]
    ) -> Optional[RecoveryAttempt]:
        """
        Execute appropriate recovery strategy for the given failure.

        Returns recovery attempt record or None if no strategy could be applied.
        """

        # Check attempt history to avoid repeated attempts
        agent_id = failure.agent_id or "unknown"
        recent_attempts = self.attempt_history[agent_id]
        recent_attempts = [a for a in recent_attempts if
                          (datetime.now() - a.timestamp).total_seconds() < 3600]  # Last hour

        if len(recent_attempts) >= 5:  # Max attempts per hour
            self.logger.warning(f"Too many recovery attempts for agent {agent_id}")
            return None

        # Find applicable strategies (highest priority first)
        applicable_strategies = [
            s for s in self.recovery_strategies
            if s.can_handle(failure)
        ]
        applicable_strategies.sort(key=lambda s: s.priority)

        if not applicable_strategies:
            self.logger.warning(f"No recovery strategy for failure type: {failure.failure_type}")
            return None

        # Try each strategy until one succeeds
        for strategy in applicable_strategies:
            attempt_id = f"{strategy.name}_{datetime.now().timestamp()}"

            # Check if strategy is on cooldown
            if self._is_on_cooldown(strategy, agent_id):
                continue

            start_time = datetime.now()
            try:
                result = await strategy.action(failure, agent_session)
                duration = (datetime.now() - start_time).total_seconds()

                attempt = RecoveryAttempt(
                    attempt_id=attempt_id,
                    failure_indicator=failure,
                    recovery_strategy=strategy.name,
                    result=result,
                    duration=duration,
                    metadata={"agent_session": agent_session}
                )

                self.attempt_history[agent_id].append(attempt)
                self.logger.info(f"Recovery attempt {attempt_id}: {result}")

                return attempt

            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()

                attempt = RecoveryAttempt(
                    attempt_id=attempt_id,
                    failure_indicator=failure,
                    recovery_strategy=strategy.name,
                    result="exception",
                    duration=duration,
                    metadata={"error": str(e), "agent_session": agent_session}
                )

                self.attempt_history[agent_id].append(attempt)
                self.logger.error(f"Recovery attempt {attempt_id} failed: {e}")

        return None

    def _is_on_cooldown(self, strategy: RecoveryStrategy, agent_id: str) -> bool:
        """Check if strategy is currently on cooldown for this agent."""

        recent_attempts = [
            a for a in self.attempt_history[agent_id]
            if a.recovery_strategy == strategy.name
        ]

        if not recent_attempts:
            return False

        latest_attempt = max(recent_attempts, key=lambda a: a.timestamp)
        time_since_attempt = (datetime.now() - latest_attempt.timestamp).total_seconds()

        return time_since_attempt < strategy.cooldown_seconds

    def _is_multiple_attempts(self, failure: FailureIndicator, threshold: int) -> bool:
        """Check if there have been multiple recent failures of this type."""

        agent_id = failure.agent_id or "unknown"
        recent_failures = [
            a for a in self.attempt_history[agent_id]
            if (datetime.now() - a.timestamp).total_seconds() < 3600  # Last hour
        ]

        return len(recent_failures) >= threshold

    async def _retry_with_clarification(
        self,
        failure: FailureIndicator,
        agent_session: Dict[str, Any]
    ) -> str:
        """Retry with additional clarification."""

        # This would typically modify the task with clarification requests
        # For demonstration, return success
        await asyncio.sleep(0.1)  # Simulate processing
        return "success"

    async def _switch_reasoning_strategy(
        self,
        failure: FailureIndicator,
        agent_session: Dict[str, Any]
    ) -> str:
        """Switch to a different reasoning strategy."""

        # This would modify the agent's reasoning approach
        await asyncio.sleep(0.1)  # Simulate processing
        return "partial_success"

    async def _escalate_to_human(
        self,
        failure: FailureIndicator,
        agent_session: Dict[str, Any]
    ) -> str:
        """Escalate the issue to human intervention."""

        # This would create a human workflow ticket
        await asyncio.sleep(0.2)  # Simulate processing
        return "escalated"

    async def _transfer_to_specialist(
        self,
        failure: FailureIndicator,
        agent_session: Dict[str, Any]
    ) -> str:
        """Transfer to a domain specialist agent."""

        # This would handover to a specialist agent
        await asyncio.sleep(0.15)  # Simulate processing
        return "transferred"


class StateCheckpointer:
    """
    Automatic state checkpointing and rollback system.

    Saves agent state at critical decision points and enables rollback
    when failures occur, allowing recovery to stable states.
    """

    def __init__(self, max_checkpoints: int = 10):
        self.checkpoints: Dict[str, List[AgentCheckpoint]] = defaultdict(list)
        self.max_checkpoints = max_checkpoints
        self.logger = logging.getLogger(__name__)

    def create_checkpoint(
        self,
        agent_session_id: str,
        agent_state: Dict[str, Any],
        decision_point: str,
        alternatives_considered: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentCheckpoint:
        """Create a checkpoint of the current agent state."""

        checkpoint_id = f"{agent_session_id}_checkpoint_{len(self.checkpoints[agent_session_id])}"

        checkpoint = AgentCheckpoint(
            checkpoint_id=checkpoint_id,
            agent_state=dict(agent_state),  # Deep copy
            decision_point=decision_point,
            alternatives_considered=list(alternatives_considered),
            metadata=metadata or {}
        )

        self.checkpoints[agent_session_id].append(checkpoint)

        # Enforce max checkpoints limit
        if len(self.checkpoints[agent_session_id]) > self.max_checkpoints:
            removed = self.checkpoints[agent_session_id].pop(0)
            self.logger.debug(f"Removed old checkpoint: {removed.checkpoint_id}")

        self.logger.debug(f"Created checkpoint: {checkpoint_id}")
        return checkpoint

    def rollback_to_checkpoint(
        self,
        checkpoint_id: str,
        new_strategy: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Rollback to a specific checkpoint.

        Returns the agent state from the checkpoint, optionally modified
        with a new strategy.
        """

        checkpoint_id_parts = checkpoint_id.split('_checkpoint_')
        if len(checkpoint_id_parts) != 2:
            self.logger.error(f"Invalid checkpoint ID format: {checkpoint_id}")
            return None

        session_id = checkpoint_id_parts[0]
        checkpoint_number = int(checkpoint_id_parts[1])

        if session_id not in self.checkpoints:
            self.logger.error(f"No checkpoints found for session: {session_id}")
            return None

        checkpoints = self.checkpoints[session_id]
        if checkpoint_number >= len(checkpoints):
            self.logger.error(f"Checkpoint {checkpoint_number} not found for session {session_id}")
            return None

        target_checkpoint = checkpoints[checkpoint_number]

        # Restore state
        restored_state = dict(target_checkpoint.agent_state)

        # Optionally modify with new strategy
        if new_strategy:
            restored_state["reasoning_strategy"] = new_strategy
            restored_state["rollback_new_strategy"] = new_strategy

        self.logger.info(f"Rolled back to checkpoint: {checkpoint_id}")
        return restored_state

    def get_recent_checkpoints(self, session_id: str, limit: int = 5) -> List[AgentCheckpoint]:
        """Get recent checkpoints for a session."""

        if session_id not in self.checkpoints:
            return []

        checkpoints = self.checkpoints[session_id]
        return checkpoints[-limit:]  # Most recent

    def cleanup_old_checkpoints(self, session_id: str, max_age_hours: int = 24):
        """Clean up checkpoints older than specified hours."""

        if session_id not in self.checkpoints:
            return

        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

        original_count = len(self.checkpoints[session_id])
        self.checkpoints[session_id] = [
            cp for cp in self.checkpoints[session_id]
            if cp.timestamp > cutoff_time
        ]

        removed_count = original_count - len(self.checkpoints[session_id])
        if removed_count > 0:
            self.logger.debug(f"Cleaned up {removed_count} old checkpoints for {session_id}")

    def suggest_rollback_checkpoint(
        self,
        session_id: str,
        current_failure: FailureIndicator
    ) -> Optional[str]:
        """Suggest the best checkpoint to rollback to based on failure type."""

        if session_id not in self.checkpoints:
            return None

        checkpoints = self.checkpoints[session_id]

        if not checkpoints:
            return None

        # For reasoning failures, go back to before the problematic decision
        if current_failure.failure_type in ["circular_reasoning", "contradictory_statements"]:
            # Look for a checkpoint with fewer alternatives (simpler state)
            best_checkpoint = min(
                checkpoints,
                key=lambda cp: len(cp.alternatives_considered)
            )
            return best_checkpoint.checkpoint_id

        # For any failure, go back to most recent stable checkpoint
        return checkpoints[-1].checkpoint_id


class PartialSuccessResult:
    """Result when agent achieves partial success."""

    def __init__(
        self,
        achieved_subgoals: List[str],
        partial_outputs: List[Any],
        missing_components: List[str],
        next_steps_recommendation: str
    ):
        self.achieved_subgoals = achieved_subgoals
        self.partial_outputs = partial_outputs
        self.missing_components = missing_components
        self.next_steps_recommendation = next_steps_recommendation
        self.completion_percentage = len(achieved_subgoals) / max(1, len(achieved_subgoals) + len(missing_components))


class ClearFailureMessage:
    """Message explaining a clear failure."""

    def __init__(
        self,
        what_went_wrong: Dict[str, Any],
        what_was_tried: List[str],
        suggested_alternatives: List[str]
    ):
        self.what_went_wrong = what_went_wrong
        self.what_was_tried = what_was_tried
        self.suggested_alternatives = suggested_alternatives


class GracefulDegradationManager:
    """
    Manages graceful degradation when perfect performance isn't possible.

    Rather than complete failure, provides the best possible outcome given
    current constraints and capabilities.
    """

    def __init__(self):
        self.degradation_strategies: Dict[str, Callable] = {}
        self.register_default_strategies()
        self.degradation_history: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)

    def register_default_strategies(self):
        """Register default graceful degradation strategies."""

        self.degradation_strategies = {
            "partial_results": self._provide_partial_results,
            "fallback_responses": self._provide_fallback_response,
            "simplified_output": self._simplify_output,
            "human_handover": self._prepare_human_handover
        }

    async def handle_partial_failure(
        self,
        agent_session: Dict[str, Any]
    ) -> Union[PartialSuccessResult, ClearFailureMessage]:
        """
        Handle a partial failure by providing graceful degradation.
        """

        # Assess what was achieved vs what was attempted
        achieved = agent_session.get("achieved_subgoals", [])
        attempted = agent_session.get("attempted_subgoals", [])
        failed = agent_session.get("failed_subgoals", [])

        # Calculate degradation level
        degradation_level = self._calculate_degradation_level(achieved, failed)

        # Choose appropriate strategy
        strategy_name = self._select_degradation_strategy(degradation_level)

        strategy = self.degradation_strategies.get(strategy_name)
        if not strategy:
            # Default to clear failure message
            return ClearFailureMessage(
                what_went_wrong={"general_failure": "Unable to process request"},
                what_was_tried=["standard_processing"],
                suggested_alternatives=["Try again later", "Contact support"]
            )

        try:
            result = await strategy(agent_session)

            # Log degradation
            self.degradation_history.append({
                "strategy": strategy_name,
                "degradation_level": degradation_level,
                "timestamp": datetime.now(),
                "session": agent_session.get("session_id")
            })

            return result

        except Exception as e:
            self.logger.error(f"Degradation strategy {strategy_name} failed: {e}")

            # Final fallback
            return ClearFailureMessage(
                what_went_wrong={"degradation_failure": str(e)},
                what_was_tried=["graceful_degradation"],
                suggested_alternatives=["Contact support"]
            )

    def _calculate_degradation_level(self, achieved: List[Any], failed: List[Any]) -> float:
        """Calculate how severe the degradation should be."""

        total_tasks = len(achieved) + len(failed)
        if total_tasks == 0:
            return 0.0

        failure_rate = len(failed) / total_tasks

        # Adjust based on criticality of failed tasks
        critical_failed = sum(1 for f in failed if getattr(f, 'critical', False))
        critical_failure_rate = critical_failed / max(1, len(failed))

        degradation = failure_rate * (0.5 + 0.5 * critical_failure_rate)
        return min(degradation, 1.0)

    def _select_degradation_strategy(self, degradation_level: float) -> str:
        """Select appropriate degradation strategy based on severity."""

        if degradation_level < 0.3:
            return "partial_results"
        elif degradation_level < 0.6:
            return "fallback_responses"
        elif degradation_level < 0.9:
            return "simplified_output"
        else:
            return "human_handover"

    async def _provide_partial_results(self, agent_session: Dict[str, Any]) -> PartialSuccessResult:
        """Provide partial results when some subtasks succeeded."""

        achieved = agent_session.get("achieved_subgoals", [])
        partial_outputs = agent_session.get("partial_outputs", [])
        failed = agent_session.get("failed_subgoals", [])

        # Generate next steps recommendation
        next_steps = self._generate_next_steps_recommendation(failed)

        return PartialSuccessResult(
            achieved_subgoals=[str(a) for a in achieved],
            partial_outputs=partial_outputs,
            missing_components=[str(f) for f in failed],
            next_steps_recommendation=next_steps
        )

    async def _provide_fallback_response(self, agent_session: Dict[str, Any]) -> PartialSuccessResult:
        """Provide fallback responses for failed components."""

        task = agent_session.get("original_task", "")
        failed = agent_session.get("failed_subgoals", [])

        # Generate simple fallback responses
        fallback_outputs = []
        for failed_item in failed:
            fallback = f"Fallback response for: {failed_item}"
            fallback_outputs.append(fallback)

        return PartialSuccessResult(
            achieved_subgoals=["basic_processing_completed"],
            partial_outputs=fallback_outputs,
            missing_components=[str(f) for f in failed],
            next_steps_recommendation="Consider manual verification of fallback responses"
        )

    async def _simplify_output(self, agent_session: Dict[str, Any]) -> PartialSuccessResult:
        """Provide simplified version of the output."""

        original_task = agent_session.get("original_task", "")

        simplified_output = f"Simplified result for: {original_task[:50]}..."

        return PartialSuccessResult(
            achieved_subgoals=["simplification_completed"],
            partial_outputs=[simplified_output],
            missing_components=["detailed_analysis"],
            next_steps_recommendation="Request full analysis from human operator if needed"
        )

    async def _prepare_human_handover(self, agent_session: Dict[str, Any]) -> ClearFailureMessage:
        """Prepare for human handover when degradation is too severe."""

        what_went_wrong = {
            "severe_degradation": "Unable to provide meaningful automated response",
            "session_details": agent_session
        }

        what_was_tried = agent_session.get("attempted_strategies", ["standard_processing"])

        suggested_alternatives = [
            "Contact human support specialist",
            "Schedule follow-up consultation",
            "Review system capabilities for this type of request"
        ]

        return ClearFailureMessage(
            what_went_wrong=what_went_wrong,
            what_was_tried=what_was_tried,
            suggested_alternatives=suggested_alternatives
        )

    def _generate_next_steps_recommendation(self, failed_components: List[Any]) -> str:
        """Generate recommendation for next steps."""

        if not failed_components:
            return "All components completed successfully"

        if len(failed_components) == 1:
            return f"Manually complete the remaining component: {failed_components[0]}"
        else:
            return f"Manually complete {len(failed_components)} remaining components, starting with the most critical"

    def get_degradation_statistics(self) -> Dict[str, Any]:
        """Get statistics on degradation usage."""

        if not self.degradation_history:
            return {"no_degradation_events": True}

        strategies_used = defaultdict(int)
        degradation_levels = []

        for event in self.degradation_history:
            strategies_used[event["strategy"]] += 1
            degradation_levels.append(event["degradation_level"])

        return {
            "total_degradation_events": len(self.degradation_history),
            "strategies_used": dict(strategies_used),
            "average_degradation_level": np.mean(degradation_levels),
            "max_degradation_level": max(degradation_levels),
            "most_used_strategy": max(strategies_used.items(), key=lambda x: x[1])[0]
        }
