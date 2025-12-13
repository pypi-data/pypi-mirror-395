"""
MCP-B Workflow Engine - Self-Improving Workflows

Transforms AMUM's 3→6→9 pattern into flexible, template-based workflows.
QCI + ETHIC run in background for coherence tracking and ethical validation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid
import json
import yaml


class StepStatus(Enum):
    """Workflow step status"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class WorkflowStatus(Enum):
    """Workflow status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStep:
    """Single step in a workflow"""
    step_index: int
    name: str
    prompt: str
    num_options: int = 3
    options: list[str] = field(default_factory=list)
    selected: Optional[int] = None
    output: str = ""
    status: StepStatus = StepStatus.PENDING

    def to_dict(self) -> dict:
        return {
            "step_index": self.step_index,
            "name": self.name,
            "prompt": self.prompt,
            "num_options": self.num_options,
            "options": self.options,
            "selected": self.selected,
            "output": self.output,
            "status": self.status.value
        }

    def display(self) -> str:
        """Format step for display"""
        lines = [f"Step {self.step_index + 1}: {self.name}", ""]
        if self.prompt:
            lines.append(self.prompt)
            lines.append("")
        for i, opt in enumerate(self.options):
            marker = ">" if i == self.selected else " "
            lines.append(f"  {marker} [{i + 1}] {opt}")
        return "\n".join(lines)


@dataclass
class WorkflowTemplate:
    """Template defining workflow structure"""
    name: str
    description: str = ""
    steps: list[dict] = field(default_factory=list)
    output_template: str = ""

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "WorkflowTemplate":
        """Load template from YAML string"""
        data = yaml.safe_load(yaml_str)
        return cls(
            name=data.get("name", "Unnamed"),
            description=data.get("description", ""),
            steps=data.get("steps", []),
            output_template=data.get("output_template", "")
        )

    @classmethod
    def from_file(cls, path: str) -> "WorkflowTemplate":
        """Load template from YAML file"""
        with open(path, 'r') as f:
            return cls.from_yaml(f.read())

    @classmethod
    def default(cls) -> "WorkflowTemplate":
        """Default 3-step workflow"""
        return cls(
            name="Quick Task",
            description="Simple 3-step workflow",
            steps=[
                {"name": "Approach", "prompt": "How would you approach this?", "options": 3},
                {"name": "Details", "prompt": "What details are important?", "options": 3},
                {"name": "Execute", "prompt": "Final decision?", "options": 3},
            ]
        )


@dataclass
class Workflow:
    """Self-Improving Workflow"""
    workflow_id: str = field(default_factory=lambda: f"WF-{uuid.uuid4().hex[:8]}")
    name: str = ""
    template_name: str = ""
    steps: list[WorkflowStep] = field(default_factory=list)
    current_step: int = 0
    status: WorkflowStatus = WorkflowStatus.ACTIVE
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    @classmethod
    def from_template(cls, template: WorkflowTemplate, task_name: str = "") -> "Workflow":
        """Create workflow from template"""
        steps = [
            WorkflowStep(
                step_index=i,
                name=s.get("name", f"Step {i+1}"),
                prompt=s.get("prompt", ""),
                num_options=s.get("options", 3)
            )
            for i, s in enumerate(template.steps)
        ]
        if steps:
            steps[0].status = StepStatus.ACTIVE

        return cls(
            name=task_name or template.name,
            template_name=template.name,
            steps=steps
        )

    def get_current_step(self) -> Optional[WorkflowStep]:
        """Get current active step"""
        if 0 <= self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None

    def set_options(self, options: list[str]) -> bool:
        """Set options for current step"""
        step = self.get_current_step()
        if not step or step.status != StepStatus.ACTIVE:
            return False
        step.options = options
        return True

    def select(self, selection: int) -> bool:
        """Select an option (1-indexed for user convenience)"""
        step = self.get_current_step()
        if not step or step.status != StepStatus.ACTIVE:
            return False

        index = selection - 1  # Convert to 0-indexed
        if not (0 <= index < len(step.options)):
            return False

        step.selected = index
        step.output = step.options[index]
        step.status = StepStatus.COMPLETED

        # Log to history
        self.history.append({
            "action": "select",
            "step": self.current_step,
            "selection": selection,
            "option": step.options[index],
            "timestamp": datetime.now().isoformat()
        })

        return True

    def advance(self) -> bool:
        """Advance to next step"""
        step = self.get_current_step()
        if not step or step.status != StepStatus.COMPLETED:
            return False

        self.current_step += 1

        if self.current_step >= len(self.steps):
            # Workflow complete
            self.status = WorkflowStatus.COMPLETED
            self.completed_at = datetime.now()
            self.history.append({
                "action": "complete",
                "timestamp": datetime.now().isoformat()
            })
            return True

        # Activate next step
        self.steps[self.current_step].status = StepStatus.ACTIVE
        return True

    def select_and_advance(self, selection: int) -> bool:
        """Select option and advance in one call"""
        if self.select(selection):
            return self.advance()
        return False

    @property
    def is_complete(self) -> bool:
        return self.status == WorkflowStatus.COMPLETED

    @property
    def progress(self) -> str:
        """Progress string like '2/5'"""
        completed = sum(1 for s in self.steps if s.status == StepStatus.COMPLETED)
        return f"{completed}/{len(self.steps)}"

    def display_status(self) -> str:
        """Format workflow status for display"""
        lines = [
            f"Workflow: {self.name}",
            f"Status: {self.status.value} ({self.progress})",
            ""
        ]

        for step in self.steps:
            if step.status == StepStatus.COMPLETED:
                lines.append(f"  [x] {step.name}: {step.output}")
            elif step.status == StepStatus.ACTIVE:
                lines.append(f"  [>] {step.name} (current)")
            else:
                lines.append(f"  [ ] {step.name}")

        return "\n".join(lines)

    def display_current(self) -> str:
        """Display current step"""
        if self.is_complete:
            return self.display_result()

        step = self.get_current_step()
        if not step:
            return "No active step"

        return f"Workflow: {self.name}\n{step.display()}"

    def display_result(self) -> str:
        """Display final result"""
        if not self.is_complete:
            return self.display_status()

        lines = [
            f"Workflow Complete: {self.name}",
            f"=" * 40,
            ""
        ]

        for step in self.steps:
            lines.append(f"{step.name}: {step.output}")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "template_name": self.template_name,
            "steps": [s.to_dict() for s in self.steps],
            "current_step": self.current_step,
            "status": self.status.value,
            "history": self.history,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class WorkflowEngine:
    """Manages workflows with optional LLM integration"""

    def __init__(self):
        self.workflows: dict[str, Workflow] = {}
        self.templates: dict[str, WorkflowTemplate] = {
            "default": WorkflowTemplate.default()
        }
        self._active_workflow_id: Optional[str] = None

    def register_template(self, template: WorkflowTemplate) -> None:
        """Register a workflow template"""
        self.templates[template.name.lower().replace(" ", "_")] = template

    def load_template(self, path: str) -> WorkflowTemplate:
        """Load and register template from file"""
        template = WorkflowTemplate.from_file(path)
        self.register_template(template)
        return template

    def start(self, task: str, template_name: str = "default") -> Workflow:
        """Start a new workflow"""
        template = self.templates.get(template_name, WorkflowTemplate.default())
        workflow = Workflow.from_template(template, task)
        self.workflows[workflow.workflow_id] = workflow
        self._active_workflow_id = workflow.workflow_id
        return workflow

    def get_active(self) -> Optional[Workflow]:
        """Get currently active workflow"""
        if self._active_workflow_id:
            return self.workflows.get(self._active_workflow_id)
        return None

    def get(self, workflow_id: str) -> Optional[Workflow]:
        """Get workflow by ID"""
        return self.workflows.get(workflow_id)

    def set_active(self, workflow_id: str) -> bool:
        """Set active workflow"""
        if workflow_id in self.workflows:
            self._active_workflow_id = workflow_id
            return True
        return False

    def list_active(self) -> list[Workflow]:
        """List all active workflows"""
        return [w for w in self.workflows.values() if w.status == WorkflowStatus.ACTIVE]

    def list_completed(self) -> list[Workflow]:
        """List completed workflows"""
        return [w for w in self.workflows.values() if w.status == WorkflowStatus.COMPLETED]


# Global engine instance
_engine: Optional[WorkflowEngine] = None


def get_engine() -> WorkflowEngine:
    """Get global workflow engine"""
    global _engine
    if _engine is None:
        _engine = WorkflowEngine()
    return _engine


# Convenience functions
def start_workflow(task: str, template: str = "default") -> Workflow:
    """Start a new workflow"""
    return get_engine().start(task, template)


def current_workflow() -> Optional[Workflow]:
    """Get current workflow"""
    return get_engine().get_active()


def workflow_next(selection: int) -> bool:
    """Select and advance current workflow"""
    wf = current_workflow()
    if wf:
        return wf.select_and_advance(selection)
    return False
