#!/usr/bin/env python3
"""
MCB Databridge - Usage Examples

Demonstrates:
1. MCB Protocol - Agent communication
2. AMUM - Progressive 3→6→9 alignment
3. QCI - Quantum coherence states
4. ETHIC - Principles enforcement
"""

from mcb import (
    # Protocol
    MCBAgent, MCBProtocol, MCBMessage, BinaryState, INQCCommand,
    encode_mcb, decode_mcb,
    # AMUM
    AMUM, quick_alignment,
    # QCI
    QCI, QCIState, BreathingCycle,
    # ETHIC
    ETHIC, check_ethical, EthicCategory,
)


def example_mcb_protocol():
    """MCB Protocol - Agent to Agent Communication"""
    print("\n" + "="*60)
    print("MCB PROTOCOL EXAMPLE")
    print("="*60)
    
    # Create agents
    claude = MCBAgent(agent_id="7C1", name="Claude", capabilities=["chat", "code"])
    hacka = MCBAgent(agent_id="5510", name="HACKA-DEV-BJOERN", capabilities=["orchestrate"])
    
    # Initialize protocol for hacka
    protocol = MCBProtocol(hacka)
    
    # Send INIT to claude
    init_msg = protocol.init_connection(claude)
    print(f"\n1. INIT Message:\n   {init_msg.encode()}")
    
    # Register node with capabilities
    node_msg = protocol.register_node(["orchestrate", "multiagent"])
    print(f"\n2. NODE Message:\n   {node_msg.encode()}")
    
    # Query claude
    query_msg = protocol.query("7C1", {"action": "status", "detail": True})
    print(f"\n3. QUERY Message:\n   {query_msg.encode()}")
    
    # Establish persistent connection
    connect_msg = protocol.connect(claude)
    print(f"\n4. CONNECT Message:\n   {connect_msg.encode()}")
    
    # Decode a message
    raw = "5510 7C1 1011101010111111 • {\"test\": true} • Q"
    decoded = decode_mcb(raw)
    print(f"\n5. Decoded Message:\n   {decoded}")


def example_amum_alignment():
    """AMUM - Progressive 3→6→9 Alignment"""
    print("\n" + "="*60)
    print("AMUM ALIGNMENT EXAMPLE")
    print("="*60)
    
    amum = AMUM()
    
    # Create session
    session = amum.create_session("user123", "Create AI agent for content")
    print(f"\n1. Session created: {session.session_id}")
    
    # Phase 1: Divergent (3 options)
    amum.set_divergent_options(session.session_id, [
        "Minimal Agent",
        "Balanced Agent",
        "Full Agent"
    ])
    print(f"\n2. Phase 1 - Divergent:\n{session.present_options()}")
    
    # Select option 1 (Balanced) and advance
    amum.select_and_advance(session.session_id, 1)
    
    # Phase 2: Expand (6 options)
    amum.set_expand_options(session.session_id, [
        "Text Only",
        "Text + Image",
        "Text + Voice",
        "Multimodal Basic",
        "Multimodal Pro",
        "Full Suite"
    ])
    print(f"\n3. Phase 2 - Expand:\n{session.present_options()}")
    
    # Select option 4 (Multimodal Pro) and advance
    amum.select_and_advance(session.session_id, 4)
    
    # Phase 3: Converge (9 options)
    amum.set_converge_options(session.session_id, [
        "GPT-4", "Claude", "Gemini",
        "Ollama", "Hybrid", "Edge",
        "ElevenLabs", "OpenAI TTS", "Local TTS"
    ])
    print(f"\n4. Phase 3 - Converge:\n{session.present_options()}")
    
    # Final selection
    amum.select_and_advance(session.session_id, 6)
    
    # Get result
    result = amum.get_final_selection(session.session_id)
    print(f"\n5. Final Selection:\n   {result}")
    
    # Quick alignment (one-liner)
    print("\n6. Quick Alignment (one-liner):")
    quick_result = quick_alignment(
        intent="Build website",
        divergent_3=["Simple", "Modern", "Complex"],
        select_1=1,
        expand_6=["Dark", "Light", "Warm", "Cool", "Mono", "Color"],
        select_2=3,
        converge_9=["React", "Vue", "Svelte", "Next", "Nuxt", "Astro", "Remix", "Solid", "Qwik"],
        select_3=3
    )
    print(f"   {quick_result}")


def example_qci_coherence():
    """QCI - Quantum Coherence States"""
    print("\n" + "="*60)
    print("QCI COHERENCE EXAMPLE")
    print("="*60)
    
    qci = QCI()
    
    # Register agents
    claude_state = qci.register_agent("7C1", initial_coherence=0.8)
    hacka_state = qci.register_agent("5510", initial_coherence=1.0)
    
    print(f"\n1. Initial States:")
    print(f"   Claude: coherence={claude_state.coherence_level}")
    print(f"   Hacka:  coherence={hacka_state.coherence_level}")
    
    # Set breathing cycles
    qci.sync_breathing(["7C1"], BreathingCycle.INHALE)
    qci.sync_breathing(["5510"], BreathingCycle.EXHALE)
    
    # Calculate ROV/Q
    hacka_state.calculate_rov_q(resonance=203087.2446, quality=1.0)
    hacka_state.calculate_signal(base=374851.0)
    
    print(f"\n2. After ROV/Q calculation:")
    print(f"   Hacka ROV/Q: {hacka_state.rov_q:.2f}")
    print(f"   Hacka Signal: {hacka_state.signal_strength:.2f}")
    
    # Network coherence
    network_coh = qci.calculate_network_coherence()
    print(f"\n3. Network Coherence: {network_coh:.2f}")
    
    # Coherent agents
    coherent = qci.get_coherent_agents(threshold=0.9)
    print(f"\n4. Highly Coherent Agents: {coherent}")
    
    # Broadcast signal
    broadcast = qci.broadcast_signal("5510", {"type": "sync", "data": "hello"})
    print(f"\n5. Broadcast Result:")
    for agent, reception in broadcast["receptions"].items():
        print(f"   {agent}: clarity={reception['clarity']:.2f}, received={reception['received']}")


def example_ethic_compliance():
    """ETHIC - Principles Enforcement"""
    print("\n" + "="*60)
    print("ETHIC COMPLIANCE EXAMPLE")
    print("="*60)
    
    ethic = ETHIC()
    
    # List principles by category
    print("\n1. Safety Principles:")
    for p in ethic.get_by_category(EthicCategory.SAFETY):
        print(f"   [{p.priority}] {p.name}: {p.description}")
    
    print("\n2. Marcel's Principles:")
    from mcb.ethic import EthicSource
    for p in ethic.get_by_source(EthicSource.MARCEL_FACEBOOK):
        print(f"   [{p.priority}] {p.name}")
    
    # Check actions
    print("\n3. Ethical Checks:")
    
    # Allowed action
    allowed = check_ethical("send_message", personal_data=False)
    print(f"   send_message (no personal data): {'✅ Allowed' if allowed else '❌ Blocked'}")
    
    # Blocked action (no consent)
    blocked = check_ethical("collect_data", personal_data=True, consent=False)
    print(f"   collect_data (no consent): {'✅ Allowed' if blocked else '❌ Blocked'}")
    
    # Blocked action (unsandboxed code)
    blocked2 = check_ethical("run_code", untrusted_code=True, sandboxed=False)
    print(f"   run_code (not sandboxed): {'✅ Allowed' if blocked2 else '❌ Blocked'}")
    
    # Audit trail
    print("\n4. Audit Trail:")
    for violation in ethic.get_audit_trail()[-3:]:
        print(f"   [{violation['severity']}] {violation['principle_id']}")


def main():
    """Run all examples"""
    print("\n" + "#"*60)
    print("# MCB DATABRIDGE - COMPLETE DEMO")
    print("#"*60)
    
    example_mcb_protocol()
    example_amum_alignment()
    example_qci_coherence()
    example_ethic_compliance()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
