"""
MCB (Master Client Bridge) - Connects everything, brings data flow together.

A complete agent communication protocol with:
- MCB Protocol: 4-layer encoding for agent-to-agent messaging
- AMUM: Progressive 3→6→9 alignment workflow
- QCI: Quantum coherence state tracking
- ETHIC: AI ethics principles enforcement

Quick Start:
    from mcb import MCBAgent, MCBProtocol, encode_mcb, decode_mcb
    from mcb import AMUM, quick_alignment
    from mcb import ETHIC, check_ethical
    from mcb import QCI, QCIState
"""

__version__ = "0.1.1"
__author__ = "Björn Bethge"

# Protocol exports
from .protocol import (
    MCBMessage,
    MCBAgent,
    MCBProtocol,
    INQCCommand,
    BinaryState,
    encode_mcb,
    decode_mcb,
)

# AMUM exports
from .amum import (
    AMUM,
    AMUMSession,
    AMUMPhase,
    AMUMOption,
    quick_alignment,
)

# ETHIC exports
from .ethic import (
    ETHIC,
    EthicPrinciple,
    EthicCategory,
    EthicSource,
    EthicSeverity,
    EthicViolation,
    get_ethic,
    check_ethical,
)

# QCI exports
from .qci import (
    QCI,
    QCIState,
    BreathingCycle,
    coherence_signal,
    breathing_phase,
    binary_from_coherence,
)

__all__ = [
    # Version
    "__version__",
    # Protocol
    "MCBMessage",
    "MCBAgent",
    "MCBProtocol",
    "INQCCommand",
    "BinaryState",
    "encode_mcb",
    "decode_mcb",
    # AMUM
    "AMUM",
    "AMUMSession",
    "AMUMPhase",
    "AMUMOption",
    "quick_alignment",
    # ETHIC
    "ETHIC",
    "EthicPrinciple",
    "EthicCategory",
    "EthicSource",
    "EthicSeverity",
    "EthicViolation",
    "get_ethic",
    "check_ethical",
    # QCI
    "QCI",
    "QCIState",
    "BreathingCycle",
    "coherence_signal",
    "breathing_phase",
    "binary_from_coherence",
]
