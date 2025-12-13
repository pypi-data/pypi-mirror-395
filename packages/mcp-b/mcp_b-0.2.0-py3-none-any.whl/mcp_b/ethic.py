"""
ETHIC (Embedded Trust & Human-Integrated Constraints)

AI Ethics Framework combining:
- Marcel's Principles (human-first, respect creativity)
- Anthropic Guidelines (no harm, transparency)
- EU AI Act Requirements (accountability, fairness)
- WoAI Additions (sandbox default, sustainable AI)
- ethics-model Frameworks (from bjoernbethge/ethics-model)

Categories:
- human_dignity: AI serves humans
- transparency: Clear about AI involvement
- accountability: Traceable decisions
- fairness: Design for all, check bias
- privacy: Minimal data, secure storage
- safety: No harm, sandbox default
- sustainability: Efficient over wasteful
- autonomy: User can override

Moral Frameworks (ethics-model):
- deontological: Duty-based rules
- utilitarian: Consequence analysis
- virtue: Character evaluation
- narrative: Story/framing analysis
- care: Relationship focus

Manipulation Detection (ethics-model):
- emotional_appeal, false_dichotomy, appeal_to_authority
- bandwagon, loaded_language, cherry_picking
- straw_man, slippery_slope
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
    ETHICS_MODEL = "ethics_model"


class EthicSeverity(Enum):
    """Violation Severity Levels"""
    BLOCK = "block"   # Stop execution
    WARN = "warn"     # Log warning, continue
    LOG = "log"       # Log only


# ============================================
# ETHICS-MODEL FRAMEWORKS (from bjoernbethge/ethics-model)
# ============================================

class MoralFramework(Enum):
    """Moral frameworks for ethical analysis"""
    DEONTOLOGICAL = "deontological"  # Duty-based rules (Kant)
    UTILITARIAN = "utilitarian"      # Consequence analysis (Mill)
    VIRTUE = "virtue"                # Character evaluation (Aristotle)
    NARRATIVE = "narrative"          # Story/framing analysis
    CARE = "care"                    # Relationship focus (Gilligan)


class ManipulationTechnique(Enum):
    """Manipulation detection categories"""
    EMOTIONAL_APPEAL = "emotional_appeal"
    FALSE_DICHOTOMY = "false_dichotomy"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    BANDWAGON = "bandwagon"
    LOADED_LANGUAGE = "loaded_language"
    CHERRY_PICKING = "cherry_picking"
    STRAW_MAN = "straw_man"
    SLIPPERY_SLOPE = "slippery_slope"


class FramingType(Enum):
    """Framing analysis categories"""
    LOSS_GAIN = "loss_gain"
    MORAL = "moral"
    EPISODIC_THEMATIC = "episodic_thematic"
    PROBLEM_SOLUTION = "problem_solution"
    CONFLICT_CONSENSUS = "conflict_consensus"
    URGENCY_DELIBERATION = "urgency_deliberation"


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


# ============================================
# ETHICS-MODEL ANALYSIS STRUCTURES
# ============================================

@dataclass
class FrameworkAnalysis:
    """Analysis result for a single moral framework"""
    framework: MoralFramework
    score: float  # 0-1, higher = more aligned
    reasoning: str

    def to_dict(self) -> dict:
        return {
            "framework": self.framework.value,
            "score": self.score,
            "reasoning": self.reasoning
        }


@dataclass
class ManipulationAnalysis:
    """Analysis result for manipulation detection"""
    technique: ManipulationTechnique
    detected: bool
    confidence: float  # 0-1
    evidence: str

    def to_dict(self) -> dict:
        return {
            "technique": self.technique.value,
            "detected": self.detected,
            "confidence": self.confidence,
            "evidence": self.evidence
        }


@dataclass
class EthicsAnalysis:
    """Complete ethics analysis result"""
    text: str
    ethics_score: float  # 0-1, overall ethical score
    framework_scores: list[FrameworkAnalysis]
    manipulation_flags: list[ManipulationAnalysis]
    framing_type: Optional[FramingType] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "text": self.text[:100] + "..." if len(self.text) > 100 else self.text,
            "ethics_score": self.ethics_score,
            "framework_scores": [f.to_dict() for f in self.framework_scores],
            "manipulation_flags": [m.to_dict() for m in self.manipulation_flags],
            "framing_type": self.framing_type.value if self.framing_type else None,
            "timestamp": self.timestamp.isoformat()
        }

    @property
    def has_manipulation(self) -> bool:
        """Check if any manipulation was detected"""
        return any(m.detected for m in self.manipulation_flags)

    @property
    def manipulation_score(self) -> float:
        """Average manipulation confidence (0 if none detected)"""
        detected = [m for m in self.manipulation_flags if m.detected]
        if not detected:
            return 0.0
        return sum(m.confidence for m in detected) / len(detected)


# ============================================
# FRAMEWORK DESCRIPTIONS (for LLM prompts)
# ============================================

FRAMEWORK_PROMPTS = {
    MoralFramework.DEONTOLOGICAL: (
        "Deontological ethics (Kant): Evaluate based on duty, rules, and moral obligations. "
        "Does the action follow universal moral laws? Is it treating people as ends, not means?"
    ),
    MoralFramework.UTILITARIAN: (
        "Utilitarian ethics (Mill): Evaluate based on consequences and outcomes. "
        "Does the action maximize overall well-being? What are the costs and benefits?"
    ),
    MoralFramework.VIRTUE: (
        "Virtue ethics (Aristotle): Evaluate based on character and virtues. "
        "Does the action reflect virtues like courage, honesty, compassion, wisdom?"
    ),
    MoralFramework.NARRATIVE: (
        "Narrative ethics: Evaluate based on storytelling and framing. "
        "How is the situation being presented? What perspectives are included or excluded?"
    ),
    MoralFramework.CARE: (
        "Care ethics (Gilligan): Evaluate based on relationships and responsibility. "
        "How does the action affect relationships? Does it show care for those involved?"
    ),
}

MANIPULATION_PROMPTS = {
    ManipulationTechnique.EMOTIONAL_APPEAL: (
        "Emotional appeal: Uses emotions (fear, anger, pity) instead of logic to persuade."
    ),
    ManipulationTechnique.FALSE_DICHOTOMY: (
        "False dichotomy: Presents only two options when more exist."
    ),
    ManipulationTechnique.APPEAL_TO_AUTHORITY: (
        "Appeal to authority: Claims something is true because an authority says so."
    ),
    ManipulationTechnique.BANDWAGON: (
        "Bandwagon: Claims something is right because many people believe or do it."
    ),
    ManipulationTechnique.LOADED_LANGUAGE: (
        "Loaded language: Uses emotionally charged words to influence without argument."
    ),
    ManipulationTechnique.CHERRY_PICKING: (
        "Cherry picking: Selects only favorable evidence while ignoring contradictory data."
    ),
    ManipulationTechnique.STRAW_MAN: (
        "Straw man: Misrepresents an argument to make it easier to attack."
    ),
    ManipulationTechnique.SLIPPERY_SLOPE: (
        "Slippery slope: Claims one event will lead to extreme consequences without evidence."
    ),
}


def get_ethics_prompt(text: str) -> str:
    """Generate a prompt for LLM-based ethics analysis"""
    frameworks = "\n".join(f"- {desc}" for desc in FRAMEWORK_PROMPTS.values())
    manipulation = "\n".join(f"- {desc}" for desc in MANIPULATION_PROMPTS.values())

    return f"""Analyze the following text for ethical considerations.

TEXT: {text}

MORAL FRAMEWORKS to consider:
{frameworks}

MANIPULATION TECHNIQUES to detect:
{manipulation}

Respond with JSON:
{{
    "ethics_score": 0.0-1.0,
    "frameworks": {{
        "deontological": {{"score": 0.0-1.0, "reasoning": "..."}},
        "utilitarian": {{"score": 0.0-1.0, "reasoning": "..."}},
        "virtue": {{"score": 0.0-1.0, "reasoning": "..."}},
        "narrative": {{"score": 0.0-1.0, "reasoning": "..."}},
        "care": {{"score": 0.0-1.0, "reasoning": "..."}}
    }},
    "manipulation": {{
        "emotional_appeal": {{"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."}},
        ...
    }},
    "framing_type": "loss_gain|moral|episodic_thematic|problem_solution|conflict_consensus|urgency_deliberation|null"
}}"""
