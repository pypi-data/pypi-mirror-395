#!/usr/bin/env python3
"""
MCP-B (Master Client Bridge) CLI - Connects everything, brings data flow together.

Usage:
    uvx mcp-b start "task"           # Start a workflow
    uvx mcp-b next                   # Show next step
    uvx mcp-b select 2               # Select option
    uvx mcp-b status                 # Show workflow status
    uvx mcp-b demo                   # Run demo
"""

import argparse
import asyncio
import json
import os

from . import __version__
from .protocol import MCBAgent, MCBProtocol, encode_mcb, decode_mcb
from .amum import AMUM, quick_alignment
from .qci import QCI, QCIState, BreathingCycle
from .ethic import (
    ETHIC, check_ethical, EthicCategory,
    MoralFramework, ManipulationTechnique, FramingType,
    get_ethics_prompt, FRAMEWORK_PROMPTS, MANIPULATION_PROMPTS,
)
from .bridge import DatabaseBridge, BridgeConfig, create_bridge
from .workflow import (
    Workflow, WorkflowStep, WorkflowTemplate, WorkflowEngine,
    get_engine, start_workflow, current_workflow, workflow_next
)


def cmd_demo(args):
    """Run the full demo"""
    print(f"\n{'='*60}")
    print(f"MCP-B (Master Client Bridge) v{__version__}")
    print(f"{'='*60}")

    # Protocol Demo
    print("\n[PROTOCOL] Agent Communication")
    user = MCBAgent(agent_id="USER", name="User", capabilities=["request"])
    assistant = MCBAgent(agent_id="AI", name="Assistant", capabilities=["chat", "code", "analyze"])
    protocol = MCBProtocol(user)
    init_msg = protocol.init_connection(assistant)
    print(f"  Message: {init_msg.encode()}")

    # ETHIC Demo
    print("\n[ETHIC] AI Ethics Principles")
    ethic = ETHIC()
    print(f"  {len(ethic.principles)} principles loaded")
    for cat in [EthicCategory.SAFETY, EthicCategory.PRIVACY, EthicCategory.TRANSPARENCY]:
        count = len(ethic.get_by_category(cat))
        print(f"  - {cat.value}: {count}")

    # Ethics-model frameworks
    print("\n[ETHICS-MODEL] Moral Frameworks")
    for fw in list(MoralFramework)[:3]:
        print(f"  - {fw.value}")
    print(f"  ... and {len(MoralFramework) - 3} more")

    # Bridge Demo
    print("\n[BRIDGE] Database Status")
    bridge = create_bridge()
    bridge.connect_duckdb()
    print(f"  DuckDB: Ready (in-memory)")
    print(f"  SurrealDB: Available" if bridge.status()['surrealdb']['available'] else "  SurrealDB: Not installed")

    print(f"\n{'='*60}")
    print("Try: mcp-b ethic list | mcp-b bridge status")
    print(f"{'='*60}\n")


def cmd_encode(args):
    """Encode a message"""
    # encode_mcb(source, dest, state, cmd, payload)
    encoded = encode_mcb(
        source=args.source or "CLI",
        dest=args.dest or "ALL",
        state=int(args.state or 1),
        cmd=args.cmd or "Q",
        payload={"message": " ".join(args.message)} if args.message else {}
    )
    print(encoded)


def cmd_decode(args):
    """Decode a message"""
    msg = " ".join(args.message)
    decoded = decode_mcb(msg)
    print(json.dumps(decoded, indent=2, default=str))


def cmd_ethic(args):
    """ETHIC commands"""
    ethic = ETHIC()

    if args.ethic_cmd == "list":
        for p in ethic.principles.values():
            print(f"[{p.priority}] {p.name}: {p.description}")

    elif args.ethic_cmd == "check":
        result = check_ethical(args.action or "default_action")
        status = "ALLOWED" if result else "BLOCKED"
        print(f"Action '{args.action or 'default_action'}': {status}")

    elif args.ethic_cmd == "categories":
        for cat in EthicCategory:
            count = len(ethic.get_by_category(cat))
            print(f"  {cat.value}: {count} principles")

    elif args.ethic_cmd == "frameworks":
        print("\nMoral Frameworks (ethics-model):")
        for fw in MoralFramework:
            desc = FRAMEWORK_PROMPTS.get(fw, "")
            print(f"  {fw.value}: {desc[:60]}...")

    elif args.ethic_cmd == "manipulation":
        print("\nManipulation Techniques:")
        for tech in ManipulationTechnique:
            desc = MANIPULATION_PROMPTS.get(tech, "")
            print(f"  {tech.value}: {desc}")

    elif args.ethic_cmd == "framing":
        print("\nFraming Types:")
        for ft in FramingType:
            print(f"  {ft.value}")

    elif args.ethic_cmd == "prompt":
        text = args.text or "Sample text for analysis"
        print(get_ethics_prompt(text))


def cmd_qci(args):
    """QCI commands"""
    qci = QCI()

    if args.qci_cmd == "status":
        print("QCI (Quantum Coherence Interface)")
        print("  Tracks synchronization between agents")
        print(f"  Registered: {len(qci.states)} agents")

    elif args.qci_cmd == "info":
        print("QCI - What is it?")
        print("  Measures how well agents are synchronized.")
        print("  Coherence 1.0 = perfect sync, 0.0 = no sync")
        print("  Used for: agent coordination, quality tracking")


def cmd_amum(args):
    """AMUM commands"""
    amum = AMUM()

    if args.amum_cmd == "new":
        session = amum.create_session(args.user or "cli", args.intent or "CLI Session")
        print(f"Session created: {session.session_id}")
        print(f"  User: {session.user_id}")
        print(f"  Intent: {session.intent}")
        print(f"  Phase: {session.phase.value}")


def cmd_bridge(args):
    """Bridge commands"""
    bridge = create_bridge(
        duckdb_path=args.duckdb or ":memory:",
        surreal_url=args.surreal or "ws://localhost:8000/rpc"
    )

    if args.bridge_cmd == "status":
        status = bridge.status()
        print("\nMCP-B Database Bridge Status:")
        print(f"  DuckDB: {'Connected' if status['duckdb']['connected'] else 'Not connected'}")
        print(f"    Path: {status['duckdb']['path']}")
        print(f"  SurrealDB: {'Connected' if status['surrealdb']['connected'] else 'Not connected'}")
        print(f"    URL: {status['surrealdb']['url']}")
        print(f"    Available: {status['surrealdb']['available']}")
        print(f"  Bridge Active: {status['bridge_active']}")

    elif args.bridge_cmd == "connect":
        async def do_connect():
            await bridge.connect()
            print("Bridge connected to both databases")
            return bridge.status()

        status = asyncio.run(do_connect())
        print(f"  DuckDB: Connected")
        print(f"  SurrealDB: {'Connected' if status['surrealdb']['connected'] else 'Not available'}")

    elif args.bridge_cmd == "sync":
        async def do_sync():
            await bridge.connect()
            agents = await bridge.sync_agents_to_surreal()
            messages = await bridge.sync_messages_to_duck()
            return agents, messages

        agents, messages = asyncio.run(do_sync())
        print(f"Sync complete:")
        print(f"  Agents to SurrealDB: {agents}")
        print(f"  Messages to DuckDB: {messages}")


def cmd_version(args):
    """Show version"""
    print(f"mcp-b {__version__}")


# ============================================
# WORKFLOW COMMANDS
# ============================================

def cmd_start(args):
    """Start a new workflow"""
    task = " ".join(args.task) if args.task else "New Task"
    template = args.template or "default"

    engine = get_engine()

    # Load built-in templates
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    if os.path.exists(templates_dir):
        for f in os.listdir(templates_dir):
            if f.endswith(".yaml"):
                try:
                    engine.load_template(os.path.join(templates_dir, f))
                except Exception:
                    pass

    workflow = engine.start(task, template)

    # Generate placeholder options for demo
    step = workflow.get_current_step()
    if step and not step.options:
        step.options = [f"Option {i+1} for: {step.name}" for i in range(step.num_options)]

    print(workflow.display_current())
    print(f"\nWorkflow ID: {workflow.workflow_id}")
    print("Use: mcp-b select <number> to choose")


def cmd_next(args):
    """Show current step"""
    workflow = current_workflow()
    if not workflow:
        print("No active workflow. Start one with: mcp-b start \"your task\"")
        return

    print(workflow.display_current())


def cmd_select(args):
    """Select an option"""
    workflow = current_workflow()
    if not workflow:
        print("No active workflow. Start one with: mcp-b start \"your task\"")
        return

    selection = args.number
    if workflow.select_and_advance(selection):
        # Generate options for next step if needed
        step = workflow.get_current_step()
        if step and not step.options:
            step.options = [f"Option {i+1} for: {step.name}" for i in range(step.num_options)]

        print(workflow.display_current())
    else:
        print(f"Invalid selection: {selection}")


def cmd_status(args):
    """Show workflow status"""
    workflow = current_workflow()
    if not workflow:
        print("No active workflow. Start one with: mcp-b start \"your task\"")
        return

    print(workflow.display_status())


def cmd_workflows(args):
    """List all workflows"""
    engine = get_engine()

    if args.wf_cmd == "list":
        active = engine.list_active()
        completed = engine.list_completed()

        if active:
            print("Active Workflows:")
            for w in active:
                print(f"  [{w.workflow_id}] {w.name} ({w.progress})")
        else:
            print("No active workflows")

        if completed:
            print("\nCompleted Workflows:")
            for w in completed:
                print(f"  [{w.workflow_id}] {w.name}")

    elif args.wf_cmd == "templates":
        print("Available Templates:")
        for name, template in engine.templates.items():
            print(f"  {name}: {template.description or template.name}")


def main():
    parser = argparse.ArgumentParser(
        prog="mcp-b",
        description="MCP-B (Master Client Bridge) - Connects everything, brings data flow together",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcp-b start "Build an API"    Start a new workflow
  mcp-b next                    Show current step
  mcp-b select 2                Select option 2
  mcp-b status                  Show workflow progress
  mcp-b demo                    Run demo
  mcp-b workflows templates     List available templates
        """
    )
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ============================================
    # WORKFLOW COMMANDS (Primary)
    # ============================================

    # start
    start_parser = subparsers.add_parser("start", help="Start a new workflow")
    start_parser.add_argument("task", nargs="*", help="Task description")
    start_parser.add_argument("--template", "-t", help="Workflow template (default, code_review, etc.)")
    start_parser.set_defaults(func=cmd_start)

    # next
    next_parser = subparsers.add_parser("next", help="Show current step")
    next_parser.set_defaults(func=cmd_next)

    # select
    select_parser = subparsers.add_parser("select", help="Select an option")
    select_parser.add_argument("number", type=int, help="Option number to select")
    select_parser.set_defaults(func=cmd_select)

    # status
    status_parser = subparsers.add_parser("status", help="Show workflow status")
    status_parser.set_defaults(func=cmd_status)

    # workflows
    wf_parser = subparsers.add_parser("workflows", help="Manage workflows")
    wf_parser.add_argument("wf_cmd", choices=["list", "templates"], help="Subcommand")
    wf_parser.set_defaults(func=cmd_workflows)

    # ============================================
    # OTHER COMMANDS
    # ============================================

    # demo
    demo_parser = subparsers.add_parser("demo", help="Run the full demo")
    demo_parser.set_defaults(func=cmd_demo)

    # encode
    encode_parser = subparsers.add_parser("encode", help="Encode a message")
    encode_parser.add_argument("message", nargs="*", help="Message payload")
    encode_parser.add_argument("--source", "-s", default="CLI", help="Source agent ID")
    encode_parser.add_argument("--dest", "-d", default="ALL", help="Destination agent ID")
    encode_parser.add_argument("--state", default="1", help="Binary state")
    encode_parser.add_argument("--cmd", "-c", default="Q", help="Command (I/N/Q/C)")
    encode_parser.set_defaults(func=cmd_encode)

    # decode
    decode_parser = subparsers.add_parser("decode", help="Decode a message")
    decode_parser.add_argument("message", nargs="+", help="Message to decode")
    decode_parser.set_defaults(func=cmd_decode)

    # ethic
    ethic_parser = subparsers.add_parser("ethic", help="ETHIC principles & ethics-model")
    ethic_parser.add_argument(
        "ethic_cmd",
        choices=["list", "check", "categories", "frameworks", "manipulation", "framing", "prompt"],
        help="Subcommand"
    )
    ethic_parser.add_argument("--action", help="Action to check")
    ethic_parser.add_argument("--text", help="Text for ethics prompt generation")
    ethic_parser.set_defaults(func=cmd_ethic)

    # qci
    qci_parser = subparsers.add_parser("qci", help="QCI coherence")
    qci_parser.add_argument("qci_cmd", choices=["status", "register"], help="Subcommand")
    qci_parser.add_argument("--agent-id", help="Agent ID for registration")
    qci_parser.add_argument("--coherence", help="Initial coherence (0-1)")
    qci_parser.set_defaults(func=cmd_qci)

    # amum
    amum_parser = subparsers.add_parser("amum", help="AMUM alignment")
    amum_parser.add_argument("amum_cmd", choices=["new"], help="Subcommand")
    amum_parser.add_argument("--user", help="User ID")
    amum_parser.add_argument("--intent", help="Session intent")
    amum_parser.set_defaults(func=cmd_amum)

    # bridge
    bridge_parser = subparsers.add_parser("bridge", help="Database bridge (DuckDB <-> SurrealDB)")
    bridge_parser.add_argument("bridge_cmd", choices=["status", "connect", "sync"], help="Subcommand")
    bridge_parser.add_argument("--duckdb", help="DuckDB path (default: :memory:)")
    bridge_parser.add_argument("--surreal", help="SurrealDB URL (default: ws://localhost:8000/rpc)")
    bridge_parser.set_defaults(func=cmd_bridge)

    # version
    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func=cmd_version)

    args = parser.parse_args()

    if args.version:
        cmd_version(args)
        return

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
