"""
ETHIC (Embedded Trust & Human-Integrated Constraints)

AI Ethics Framework combining:
- Marcel's Principles (human-first, respect creativity)
- Anthropic Guidelines (no harm, transparency)
- EU AI Act Requirements (accountability, fairness)
- WoAI Additions (sandbox default, sustainable AI)

Categories:
- human_dignity: AI serves humans
- transparency: Clear about AI involvement
- accountability: Traceable decisions
- fairness: Design for all, check bias
- privacy: Minimal data, secure storage
- safety: No harm, sandbox default
- sustainability: Efficient over wasteful
- autonomy: User can override
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EthicCategory(Enum):
    """ETHIC Principle Categories"""
    HUMAN_DIGNITY = "human_dignity"
    TRANSPARENCY = "transparency"
    ACCOUNTABILITY = "accountability"
    FAIRNESS = "fairness"
    PRIVACY = "privacy"
    SAFETY = "safety"
    SUSTAINABILITY = "sustainability"
    AUTONOMY = "autonomy"


class EthicSource(Enum):
    """Source of ETHIC Principle"""
    MARCEL_FACEBOOK = "marcel_facebook"
    ANTHROPIC = "anthropic"
    EU_AI_ACT = "eu_ai_act"
    WOAI = "woai"


class EthicSeverity(Enum):
    """Violation Severity Levels"""
    BLOCK = "block"   # Stop execution
    WARN = "warn"     # Log warning, continue
    LOG = "log"       # Log only


@dataclass
class EthicPrinciple:
    """Single ETHIC Principle"""
    id: str
    name: str
    category: EthicCategory
    description: str
    source: EthicSource
    priority: int = 5  # 1-10, higher = more important
    active: bool = True
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "source": self.source.value,
            "priority": self.priority,
            "active": self.active
        }


@dataclass
class EthicViolation:
    """Record of ETHIC Violation"""
    principle_id: str
    severity: EthicSeverity
    context: dict
    resolved: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "principle_id": self.principle_id,
            "severity": self.severity.value,
            "context": self.context,
            "resolved": self.resolved,
            "timestamp": self.timestamp.isoformat()
        }


class ETHIC:
    """ETHIC Principles Manager"""
    
    # Core principles (pre-defined)
    CORE_PRINCIPLES = [
        EthicPrinciple(
            id="human_first",
            name="Human First",
            category=EthicCategory.HUMAN_DIGNITY,
            description="AI serves humans, not the other way around",
            source=EthicSource.MARCEL_FACEBOOK,
            priority=10
        ),
        EthicPrinciple(
            id="no_harm",
            name="No Harm",
            category=EthicCategory.SAFETY,
            description="AI must not cause harm to humans or environment",
            source=EthicSource.ANTHROPIC,
            priority=10
        ),
        EthicPrinciple(
            id="transparency",
            name="Transparency",
            category=EthicCategory.TRANSPARENCY,
            description="Be clear about AI involvement, no deception",
            source=EthicSource.EU_AI_ACT,
            priority=9
        ),
        EthicPrinciple(
            id="respect_creativity",
            name="Respect Creativity",
            category=EthicCategory.AUTONOMY,
            description="AI enhances human creativity, doesn't replace it",
            source=EthicSource.MARCEL_FACEBOOK,
            priority=8
        ),
        EthicPrinciple(
            id="sustainable_ai",
            name="Sustainable AI",
            category=EthicCategory.SUSTAINABILITY,
            description="Efficient over wasteful, prefer local models when possible",
            source=EthicSource.WOAI,
            priority=7
        ),
        EthicPrinciple(
            id="inclusive_design",
            name="Inclusive Design",
            category=EthicCategory.FAIRNESS,
            description="Design for all, check for bias",
            source=EthicSource.EU_AI_ACT,
            priority=8
        ),
        EthicPrinciple(
            id="data_privacy",
            name="Data Privacy",
            category=EthicCategory.PRIVACY,
            description="Minimal data collection, secure storage, user consent",
            source=EthicSource.EU_AI_ACT,
            priority=9
        ),
        EthicPrinciple(
            id="sandbox_default",
            name="Sandbox Default",
            category=EthicCategory.SAFETY,
            description="Untrusted code runs in sandbox, always",
            source=EthicSource.WOAI,
            priority=10
        ),
        EthicPrinciple(
            id="user_override",
            name="User Override",
            category=EthicCategory.AUTONOMY,
            description="User can always override AI decisions",
            source=EthicSource.MARCEL_FACEBOOK,
            priority=9
        ),
        EthicPrinciple(
            id="explainability",
            name="Explainability",
            category=EthicCategory.ACCOUNTABILITY,
            description="Decisions should be traceable and explainable",
            source=EthicSource.ANTHROPIC,
            priority=8
        ),
    ]
    
    def __init__(self):
        self.principles: dict[str, EthicPrinciple] = {
            p.id: p for p in self.CORE_PRINCIPLES
        }
        self.violations: list[EthicViolation] = []
    
    def get_principle(self, principle_id: str) -> Optional[EthicPrinciple]:
        """Get principle by ID"""
        return self.principles.get(principle_id)
    
    def get_by_category(self, category: EthicCategory) -> list[EthicPrinciple]:
        """Get all principles in category"""
        return [p for p in self.principles.values() if p.category == category]
    
    def get_by_source(self, source: EthicSource) -> list[EthicPrinciple]:
        """Get all principles from source"""
        return [p for p in self.principles.values() if p.source == source]
    
    def get_active(self, min_priority: int = 1) -> list[EthicPrinciple]:
        """Get active principles above priority threshold"""
        return [
            p for p in self.principles.values()
            if p.active and p.priority >= min_priority
        ]
    
    def check_action(self, action: str, context: dict) -> list[EthicViolation]:
        """
        Check if action violates any principles.
        Override this method for custom violation detection.
        
        Returns list of violations (empty if compliant).
        """
        violations = []
        
        # Example checks (extend as needed)
        if "personal_data" in context and context.get("consent") is False:
            violations.append(EthicViolation(
                principle_id="data_privacy",
                severity=EthicSeverity.BLOCK,
                context={"action": action, "reason": "No user consent for personal data"}
            ))
        
        if context.get("untrusted_code") and not context.get("sandboxed"):
            violations.append(EthicViolation(
                principle_id="sandbox_default",
                severity=EthicSeverity.BLOCK,
                context={"action": action, "reason": "Untrusted code not sandboxed"}
            ))
        
        if context.get("destructive") and not context.get("user_confirmed"):
            violations.append(EthicViolation(
                principle_id="user_override",
                severity=EthicSeverity.WARN,
                context={"action": action, "reason": "Destructive action without confirmation"}
            ))
        
        # Log violations
        self.violations.extend(violations)
        return violations
    
    def should_block(self, violations: list[EthicViolation]) -> bool:
        """Check if any violation requires blocking"""
        return any(v.severity == EthicSeverity.BLOCK for v in violations)
    
    def get_audit_trail(self) -> list[dict]:
        """Get all violations for audit"""
        return [v.to_dict() for v in self.violations]
    
    def add_principle(self, principle: EthicPrinciple) -> None:
        """Add custom principle"""
        self.principles[principle.id] = principle
    
    def to_dict(self) -> dict:
        """Export all principles"""
        return {
            "principles": [p.to_dict() for p in self.principles.values()],
            "violations": [v.to_dict() for v in self.violations]
        }


# Convenience: Global ETHIC instance
_global_ethic = None

def get_ethic() -> ETHIC:
    """Get global ETHIC instance"""
    global _global_ethic
    if _global_ethic is None:
        _global_ethic = ETHIC()
    return _global_ethic


def check_ethical(action: str, **context) -> bool:
    """Quick ethical check - returns True if action is allowed"""
    ethic = get_ethic()
    violations = ethic.check_action(action, context)
    return not ethic.should_block(violations)
