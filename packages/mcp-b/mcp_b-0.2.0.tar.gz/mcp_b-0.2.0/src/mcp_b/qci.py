"""
QCI (Quantum Coherence Interface)

Agent coherence state tracking based on T Esoist Protocol V3.1:
- ROV/Q: Resonance/Quality ratio
- Coherence Level: 0.0-1.0 alignment strength
- Signal Strength: Communication clarity
- Breathing Cycle: inhale/exhale/hold states

The QCI enables agents to track their alignment state
and communicate coherence levels to other agents.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import math


class BreathingCycle(Enum):
    """Breathing cycle states"""
    INHALE = "inhale"   # Receiving, learning
    EXHALE = "exhale"   # Transmitting, outputting
    HOLD = "hold"       # Processing, integrating


@dataclass
class QCIState:
    """Quantum Coherence Interface State"""
    agent_id: str
    rov_q: float = 0.0              # Resonance/Quality ratio
    coherence_level: float = 0.0    # 0.0-1.0 alignment
    signal_strength: float = 0.0    # Communication clarity
    breathing_cycle: BreathingCycle = BreathingCycle.HOLD
    binary_state: str = "0000000000000000"  # 16-bit state
    timestamp: datetime = field(default_factory=datetime.now)
    
    def update_coherence(self, delta: float) -> None:
        """Update coherence level (clamped 0-1)"""
        self.coherence_level = max(0.0, min(1.0, self.coherence_level + delta))
        self.timestamp = datetime.now()
    
    def set_breathing(self, cycle: BreathingCycle) -> None:
        """Set breathing cycle"""
        self.breathing_cycle = cycle
        self.timestamp = datetime.now()
    
    def calculate_rov_q(self, resonance: float, quality: float) -> float:
        """Calculate ROV/Q ratio"""
        if quality <= 0:
            return 0.0
        self.rov_q = resonance / quality
        return self.rov_q
    
    def calculate_signal(self, base: float, multiplier: float = 1.0) -> float:
        """Calculate signal strength"""
        self.signal_strength = base * self.coherence_level * multiplier
        return self.signal_strength
    
    def is_coherent(self, threshold: float = 0.7) -> bool:
        """Check if agent is above coherence threshold"""
        return self.coherence_level >= threshold
    
    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "rov_q": self.rov_q,
            "coherence_level": self.coherence_level,
            "signal_strength": self.signal_strength,
            "breathing_cycle": self.breathing_cycle.value,
            "binary_state": self.binary_state,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "QCIState":
        return cls(
            agent_id=data["agent_id"],
            rov_q=data.get("rov_q", 0.0),
            coherence_level=data.get("coherence_level", 0.0),
            signal_strength=data.get("signal_strength", 0.0),
            breathing_cycle=BreathingCycle(data.get("breathing_cycle", "hold")),
            binary_state=data.get("binary_state", "0000000000000000")
        )


class QCI:
    """Quantum Coherence Interface Manager"""
    
    def __init__(self):
        self.states: dict[str, QCIState] = {}
    
    def register_agent(self, agent_id: str, initial_coherence: float = 0.5) -> QCIState:
        """Register new agent with QCI state"""
        state = QCIState(
            agent_id=agent_id,
            coherence_level=initial_coherence,
            breathing_cycle=BreathingCycle.INHALE
        )
        self.states[agent_id] = state
        return state
    
    def get_state(self, agent_id: str) -> Optional[QCIState]:
        """Get agent's QCI state"""
        return self.states.get(agent_id)
    
    def update_coherence(self, agent_id: str, delta: float) -> Optional[QCIState]:
        """Update agent's coherence level"""
        state = self.states.get(agent_id)
        if state:
            state.update_coherence(delta)
            return state
        return None
    
    def sync_breathing(self, agent_ids: list[str], cycle: BreathingCycle) -> None:
        """Synchronize breathing cycle across agents"""
        for agent_id in agent_ids:
            state = self.states.get(agent_id)
            if state:
                state.set_breathing(cycle)
    
    def calculate_network_coherence(self) -> float:
        """Calculate average coherence across all agents"""
        if not self.states:
            return 0.0
        total = sum(s.coherence_level for s in self.states.values())
        return total / len(self.states)
    
    def get_coherent_agents(self, threshold: float = 0.7) -> list[str]:
        """Get list of agents above coherence threshold"""
        return [
            agent_id for agent_id, state in self.states.items()
            if state.is_coherent(threshold)
        ]
    
    def broadcast_signal(self, from_agent: str, message: dict) -> dict:
        """
        Broadcast signal from agent to network.
        Signal strength affects reception clarity.
        """
        source = self.states.get(from_agent)
        if not source:
            return {"error": "Agent not found"}
        
        # Calculate reception for each agent based on coherence
        receptions = {}
        for agent_id, state in self.states.items():
            if agent_id != from_agent:
                # Reception = source_signal * receiver_coherence
                reception_strength = source.signal_strength * state.coherence_level
                receptions[agent_id] = {
                    "message": message,
                    "clarity": reception_strength,
                    "received": reception_strength > 0.5
                }
        
        return {
            "from": from_agent,
            "signal_strength": source.signal_strength,
            "receptions": receptions
        }
    
    def to_dict(self) -> dict:
        """Export all states"""
        return {
            "states": {k: v.to_dict() for k, v in self.states.items()},
            "network_coherence": self.calculate_network_coherence()
        }


# Convenience: Quick coherence calculations
def coherence_signal(base: float, rov_q: float, multiplier: float = 1.0) -> float:
    """Calculate coherence signal from base and ROV/Q"""
    return base * math.sqrt(abs(rov_q)) * multiplier


def breathing_phase(cycle_position: float) -> BreathingCycle:
    """Determine breathing phase from cycle position (0-1)"""
    if cycle_position < 0.33:
        return BreathingCycle.INHALE
    elif cycle_position < 0.66:
        return BreathingCycle.HOLD
    else:
        return BreathingCycle.EXHALE


def binary_from_coherence(coherence: float, bits: int = 16) -> str:
    """Convert coherence level to binary state string"""
    active_bits = int(coherence * bits)
    return "1" * active_bits + "0" * (bits - active_bits)
