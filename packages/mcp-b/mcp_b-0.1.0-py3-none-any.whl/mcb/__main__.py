#!/usr/bin/env python3
"""
MCB (Master Client Bridge) CLI - Connects everything, brings data flow together.

Usage:
    uvx mcb demo                     # Run demo
    uvx mcb encode <msg>             # Encode message
    uvx mcb decode <msg>             # Decode message
    uvx mcb ethic check              # Check ethical principles
    uvx mcb qci status               # QCI network status
"""

import argparse
import sys
import json

from . import __version__
from .protocol import MCBAgent, MCBProtocol, encode_mcb, decode_mcb
from .amum import AMUM, quick_alignment
from .qci import QCI, QCIState, BreathingCycle
from .ethic import ETHIC, check_ethical, EthicCategory


def cmd_demo(args):
    """Run the full demo"""
    print(f"\n{'='*60}")
    print(f"MCB (Master Client Bridge) v{__version__} - DEMO")
    print(f"{'='*60}")

    # Protocol Demo
    print("\n[MCB PROTOCOL]")
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
        status = "✅ ALLOWED" if result else "❌ BLOCKED"
        print(f"Action '{args.action or 'default_action'}': {status}")

    elif args.ethic_cmd == "categories":
        for cat in EthicCategory:
            count = len(ethic.get_by_category(cat))
            print(f"  {cat.value}: {count} principles")


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


def cmd_version(args):
    """Show version"""
    print(f"mcb {__version__}")


def main():
    parser = argparse.ArgumentParser(
        prog="mcb",
        description="MCB (Master Client Bridge) - Connects everything, brings data flow together",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcb demo                    Run the demo
  mcb encode "Hello World"    Encode a message
  mcb decode "<mcb_string>"   Decode a message
  mcb ethic list              List ethical principles
  mcb qci status              Show QCI network status
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
    ethic_parser = subparsers.add_parser("ethic", help="ETHIC principles")
    ethic_parser.add_argument("ethic_cmd", choices=["list", "check", "categories"], help="Subcommand")
    ethic_parser.add_argument("--action", help="Action to check")
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
