"""
MCP-B (Master Client Bridge) - Connects everything, brings data flow together.

A complete agent communication protocol with:
- Workflow Engine: Self-improving workflows with templates
- MCP-B Protocol: 4-layer encoding for agent-to-agent messaging
- ETHIC: AI ethics principles (background)
- QCI: Quantum coherence tracking (background)

Quick Start:
    from mcp_b import start_workflow, current_workflow, workflow_next
    from mcp_b import Workflow, WorkflowTemplate, WorkflowEngine

CLI:
    mcp-b start "Build an API"    # Start workflow
    mcp-b select 2                # Select option
    mcp-b status                  # Show progress
"""

__version__ = "0.3.0"
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
    # ethics-model frameworks
    MoralFramework,
    ManipulationTechnique,
    FramingType,
    FrameworkAnalysis,
    ManipulationAnalysis,
    EthicsAnalysis,
    get_ethics_prompt,
    FRAMEWORK_PROMPTS,
    MANIPULATION_PROMPTS,
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

# Workflow exports
from .workflow import (
    Workflow,
    WorkflowStep,
    WorkflowTemplate,
    WorkflowEngine,
    WorkflowStatus,
    StepStatus,
    get_engine,
    start_workflow,
    current_workflow,
    workflow_next,
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
    # ethics-model frameworks
    "MoralFramework",
    "ManipulationTechnique",
    "FramingType",
    "FrameworkAnalysis",
    "ManipulationAnalysis",
    "EthicsAnalysis",
    "get_ethics_prompt",
    "FRAMEWORK_PROMPTS",
    "MANIPULATION_PROMPTS",
    # QCI
    "QCI",
    "QCIState",
    "BreathingCycle",
    "coherence_signal",
    "breathing_phase",
    "binary_from_coherence",
    # Workflow
    "Workflow",
    "WorkflowStep",
    "WorkflowTemplate",
    "WorkflowEngine",
    "WorkflowStatus",
    "StepStatus",
    "get_engine",
    "start_workflow",
    "current_workflow",
    "workflow_next",
]
