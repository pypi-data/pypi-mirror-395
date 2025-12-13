"""
AMUM (AI ↔ Mensch Understanding Matrix)

Progressive Alignment System: 3 → 6 → 9 Workflow

Phase 1 (divergent_3):  3 broad options
Phase 2 (expand_6):     6 variations of selected option
Phase 3 (converge_9):   9 detailed choices, final selection

The flow enables human-AI alignment through progressive refinement.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class AMUMPhase(Enum):
    """AMUM Alignment Phases"""
    DIVERGENT_3 = "divergent_3"   # 3 broad options
    EXPAND_6 = "expand_6"         # 6 variations
    CONVERGE_9 = "converge_9"     # 9 details
    COMPLETE = "complete"         # Alignment achieved


@dataclass
class AMUMOption:
    """Single option in AMUM selection"""
    index: int
    label: str
    description: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class AMUMSession:
    """AMUM Alignment Session"""
    session_id: str = field(default_factory=lambda: f"AMUM-{uuid.uuid4().hex[:8]}")
    user_id: str = ""
    phase: AMUMPhase = AMUMPhase.DIVERGENT_3
    intent: str = ""
    options: list[AMUMOption] = field(default_factory=list)
    selected: Optional[int] = None
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def present_options(self) -> str:
        """Format options for display"""
        lines = [f"Phase: {self.phase.value}", f"Intent: {self.intent}", ""]
        for opt in self.options:
            marker = "→" if opt.index == self.selected else " "
            lines.append(f"  {marker} [{opt.index}] {opt.label}")
            if opt.description:
                lines.append(f"       {opt.description}")
        return "\n".join(lines)
    
    def select(self, index: int) -> bool:
        """Select an option by index"""
        if 0 <= index < len(self.options):
            self.selected = index
            self.history.append({
                "phase": self.phase.value,
                "selected": index,
                "option": self.options[index].label,
                "timestamp": datetime.now().isoformat()
            })
            return True
        return False
    
    def advance_phase(self) -> bool:
        """Advance to next phase"""
        if self.selected is None:
            return False
        
        selected_option = self.options[self.selected]
        
        if self.phase == AMUMPhase.DIVERGENT_3:
            self.phase = AMUMPhase.EXPAND_6
            self.intent = selected_option.label
            self.options = []
            self.selected = None
            return True
        elif self.phase == AMUMPhase.EXPAND_6:
            self.phase = AMUMPhase.CONVERGE_9
            self.intent = selected_option.label
            self.options = []
            self.selected = None
            return True
        elif self.phase == AMUMPhase.CONVERGE_9:
            self.phase = AMUMPhase.COMPLETE
            self.intent = selected_option.label
            return True
        return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "phase": self.phase.value,
            "intent": self.intent,
            "options": [
                {"index": o.index, "label": o.label, "description": o.description}
                for o in self.options
            ],
            "selected": self.selected,
            "history": self.history,
            "created_at": self.created_at.isoformat()
        }


class AMUM:
    """AMUM Progressive Alignment Manager"""
    
    def __init__(self):
        self.sessions: dict[str, AMUMSession] = {}
    
    def create_session(self, user_id: str, intent: str) -> AMUMSession:
        """Create new AMUM alignment session"""
        session = AMUMSession(user_id=user_id, intent=intent)
        self.sessions[session.session_id] = session
        return session
    
    def set_divergent_options(self, session_id: str, options: list[str]) -> bool:
        """Set 3 divergent options for phase 1"""
        session = self.sessions.get(session_id)
        if not session or session.phase != AMUMPhase.DIVERGENT_3:
            return False
        if len(options) != 3:
            return False
        
        session.options = [
            AMUMOption(index=i, label=opt) for i, opt in enumerate(options)
        ]
        return True
    
    def set_expand_options(self, session_id: str, options: list[str]) -> bool:
        """Set 6 expansion options for phase 2"""
        session = self.sessions.get(session_id)
        if not session or session.phase != AMUMPhase.EXPAND_6:
            return False
        if len(options) != 6:
            return False
        
        session.options = [
            AMUMOption(index=i, label=opt) for i, opt in enumerate(options)
        ]
        return True
    
    def set_converge_options(self, session_id: str, options: list[str]) -> bool:
        """Set 9 convergence options for phase 3"""
        session = self.sessions.get(session_id)
        if not session or session.phase != AMUMPhase.CONVERGE_9:
            return False
        if len(options) != 9:
            return False
        
        session.options = [
            AMUMOption(index=i, label=opt) for i, opt in enumerate(options)
        ]
        return True
    
    def select_and_advance(self, session_id: str, selection: int) -> Optional[AMUMSession]:
        """Select option and advance to next phase"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        if session.select(selection):
            session.advance_phase()
            return session
        return None
    
    def get_final_selection(self, session_id: str) -> Optional[dict]:
        """Get final selection after complete alignment"""
        session = self.sessions.get(session_id)
        if not session or session.phase != AMUMPhase.COMPLETE:
            return None
        
        return {
            "session_id": session.session_id,
            "final_intent": session.intent,
            "alignment_path": session.history,
            "completed_at": datetime.now().isoformat()
        }


# Convenience function for quick 3→6→9 flow
def quick_alignment(
    intent: str,
    divergent_3: list[str],
    select_1: int,
    expand_6: list[str],
    select_2: int,
    converge_9: list[str],
    select_3: int
) -> dict:
    """Run complete 3→6→9 alignment in one call"""
    amum = AMUM()
    session = amum.create_session("quick", intent)
    
    amum.set_divergent_options(session.session_id, divergent_3)
    amum.select_and_advance(session.session_id, select_1)
    
    amum.set_expand_options(session.session_id, expand_6)
    amum.select_and_advance(session.session_id, select_2)
    
    amum.set_converge_options(session.session_id, converge_9)
    amum.select_and_advance(session.session_id, select_3)
    
    return amum.get_final_selection(session.session_id)
