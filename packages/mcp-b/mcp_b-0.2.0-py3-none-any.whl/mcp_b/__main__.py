#!/usr/bin/env python3
"""
MCP-B (Master Client Bridge) CLI - Connects everything, brings data flow together.

Usage:
    uvx mcp-b demo                   # Run demo
    uvx mcp-b encode <msg>           # Encode message
    uvx mcp-b decode <msg>           # Decode message
    uvx mcp-b ethic check            # Check ethical principles
    uvx mcp-b ethic frameworks       # List moral frameworks
    uvx mcp-b qci status             # QCI network status
    uvx mcp-b bridge status          # Database bridge status
"""

import argparse
import asyncio
import json

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


def cmd_demo(args):
    """Run the full demo"""
    print(f"\n{'='*60}")
    print(f"MCP-B (Master Client Bridge) v{__version__} - DEMO")
    print(f"{'='*60}")

    # Protocol Demo
    print("\n[MCP-B PROTOCOL]")
    claude = MCBAgent(agent_id="7C1", name="Claude", capabilities=["chat", "code"])
    hacka = MCBAgent(agent_id="5510", name="HACKA-DEV-BJOERN", capabilities=["orchestrate"])
    protocol = MCBProtocol(hacka)
    init_msg = protocol.init_connection(claude)
    print(f"  INIT: {init_msg.encode()}")

    # QCI Demo
    print("\n[QCI COHERENCE]")
    qci = QCI()
    qci.register_agent("7C1", initial_coherence=0.8)
    qci.register_agent("5510", initial_coherence=1.0)
    network_coh = qci.calculate_network_coherence()
    print(f"  Network Coherence: {network_coh:.2f}")

    # ETHIC Demo
    print("\n[ETHIC PRINCIPLES]")
    ethic = ETHIC()
    print(f"  Total Principles: {len(ethic.principles)}")
    print(f"  Safety: {len(ethic.get_by_category(EthicCategory.SAFETY))}")

    print(f"\n{'='*60}")
    print("DEMO COMPLETE")
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
        print(f"QCI Network Status")
        print(f"  Registered Agents: {len(qci.states)}")
        if qci.states:
            coh = qci.calculate_network_coherence()
            print(f"  Network Coherence: {coh:.2f}")

    elif args.qci_cmd == "register":
        state = qci.register_agent(args.agent_id, initial_coherence=float(args.coherence or 1.0))
        print(f"Registered: {args.agent_id} (coherence={state.coherence_level})")


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


def main():
    parser = argparse.ArgumentParser(
        prog="mcp-b",
        description="MCP-B (Master Client Bridge) - Connects everything, brings data flow together",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcp-b demo                    Run the demo
  mcp-b encode "Hello World"    Encode a message
  mcp-b decode "<mcb_string>"   Decode a message
  mcp-b ethic list              List ethical principles
  mcp-b ethic frameworks        List moral frameworks (ethics-model)
  mcp-b ethic manipulation      List manipulation techniques
  mcp-b qci status              Show QCI network status
  mcp-b bridge status           Show database bridge status
  mcp-b bridge sync             Sync DuckDB <-> SurrealDB
        """
    )
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

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
