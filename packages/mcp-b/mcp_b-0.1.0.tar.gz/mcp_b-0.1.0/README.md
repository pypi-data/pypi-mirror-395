# MCB - Master Client Bridge

**Connects everything, brings data flow together.**

A complete agent communication framework combining:
- **MCB Protocol**: 4-layer encoding for agent-to-agent messaging
- **AMUM**: Progressive 3→6→9 human-AI alignment workflow
- **QCI**: Quantum coherence state tracking
- **ETHIC**: AI ethics principles enforcement

## Installation

```bash
# Via pip
pip install mcp-b

# Via uv
uvx mcp-b demo
# or after install:
mcb demo

# With SurrealDB support
pip install mcp-b[surrealdb]

# Full installation
pip install mcp-b[full]
```

## CLI Usage

```bash
mcb demo                              # Run demo
mcb encode "Hello" -s 5510 -d 7C1     # Encode message
mcb decode "5510 7C1 ..."             # Decode message
mcb ethic list                        # List ethical principles
mcb qci status                        # QCI network status
mcb version                           # Show version
```

## Quick Start

### MCB Protocol - Agent Communication

```python
from mcb import MCBAgent, MCBProtocol, encode_mcb, decode_mcb

# Create agents
claude = MCBAgent(agent_id="7C1", name="Claude")
hacka = MCBAgent(agent_id="5510", name="HACKA")

# Initialize protocol
protocol = MCBProtocol(hacka)

# Send messages (INQC commands)
init_msg = protocol.init_connection(claude)      # I = Init
node_msg = protocol.register_node(["chat"])      # N = Node
query_msg = protocol.query("7C1", {"status": 1}) # Q = Query
connect_msg = protocol.connect(claude)           # C = Connect

# Encode/Decode
encoded = encode_mcb("5510", "7C1", 0b1011101010111111, "Q", {"ping": True})
decoded = decode_mcb("5510 7C1 1011101010111111 • {\"ping\": true} • Q")
```

### AMUM - Progressive Alignment (3→6→9)

```python
from mcb import AMUM, quick_alignment

# Quick one-liner alignment
result = quick_alignment(
    intent="Create AI agent",
    divergent_3=["Minimal", "Balanced", "Full"],
    select_1=1,
    expand_6=["Text", "Image", "Voice", "Multi", "Pro", "Suite"],
    select_2=4,
    converge_9=["GPT-4", "Claude", "Gemini", "Ollama", "Hybrid",
                "Edge", "ElevenLabs", "OpenAI", "Local"],
    select_3=6
)
print(result["final_intent"])  # "ElevenLabs"
```

### QCI - Coherence States

```python
from mcb import QCI, BreathingCycle

qci = QCI()

# Register agents with coherence
state = qci.register_agent("7C1", initial_coherence=0.95)
state.calculate_rov_q(resonance=12860.65, quality=1.0)
state.calculate_signal(base=4414.94)

# Sync breathing across agents
qci.sync_breathing(["7C1", "5510"], BreathingCycle.INHALE)

# Check network coherence
print(qci.calculate_network_coherence())
```

### ETHIC - Principles Enforcement

```python
from mcb import ETHIC, check_ethical, EthicCategory

ethic = ETHIC()

# Check if action is ethical
if check_ethical("collect_data", personal_data=True, consent=False):
    print("Allowed")
else:
    print("Blocked - no consent")

# Get principles by category
for p in ethic.get_by_category(EthicCategory.SAFETY):
    print(f"[{p.priority}] {p.name}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MCB - MASTER CLIENT BRIDGE                               │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐                  │
│  │  AMUM   │───▶│   MCB   │───▶│   QCI   │───▶│  ETHIC  │                  │
│  │ 3→6→9   │    │ INQC    │    │Coherence│    │Principles│                  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘                  │
│       │              │              │              │                        │
│       ▼              ▼              ▼              ▼                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DUAL DATABASE LAYER                              │   │
│  │  ┌─────────────────────┐    ┌─────────────────────┐                 │   │
│  │  │      DuckDB         │    │     SurrealDB       │                 │   │
│  │  │  (Analytics/SQL)    │    │  (Graph/Relations)  │                 │   │
│  │  └─────────────────────┘    └─────────────────────┘                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## MCB Protocol Layers

| Layer | Purpose | Example |
|-------|---------|---------|
| **Layer 1** | HEX/DECIMAL Routing | `7C1 5510` (source → dest) |
| **Layer 2** | BINARY State Vectors | `1011101010111111` (16 flags) |
| **Layer 3** | DOT-SEPARATED Tokens | `• payload • command` |
| **Layer 4** | INQC Commands | `I`/`N`/`Q`/`C` |

### INQC Commands

- **I** (INIT): Initialize connection
- **N** (NODE): Node registration/discovery
- **Q** (QUERY): Request data/state
- **C** (CONNECT): Establish persistent link

### Binary State Flags (16-bit)

| Bit | Flag | Description |
|-----|------|-------------|
| 0 | CONNECTED | Connection active |
| 1 | AUTHENTICATED | Auth verified |
| 2 | ENCRYPTED | Encryption enabled |
| 3 | COMPRESSED | Compression enabled |
| 4 | STREAMING | Streaming mode |
| 5 | BIDIRECTIONAL | Two-way comm |
| 6 | PERSISTENT | Persistent connection |
| 7 | PRIORITY | High priority |
| 8-15 | RESERVED | Custom flags |

## ETHIC Principles

| Principle | Category | Source | Priority |
|-----------|----------|--------|----------|
| Human First | human_dignity | Marcel | 10 |
| No Harm | safety | Anthropic | 10 |
| Sandbox Default | safety | WoAI | 10 |
| User Override | autonomy | Marcel | 9 |
| Data Privacy | privacy | EU AI Act | 9 |
| Transparency | transparency | EU AI Act | 9 |

## Database Integration

### DuckDB (Analytics)

```sql
-- Load schema
.read sql/duckdb.sql

-- Use macros
SELECT mcb_encode('5510', '7C1', '1011101010111111', '{"ping":true}', 'Q');
SELECT * FROM agent_network;
SELECT * FROM ethic_compliance;
```

### SurrealDB (Graph)

```sql
-- Load schema
IMPORT FILE schemas/surrealdb.surql;

-- Query relationships
SELECT
    name,
    ->has_qci->qci_states.coherence_level AS coherence,
    ->follows_ethic->ethic_principles.name AS principles
FROM mcb_agents;
```

## File Structure

```
mcb/
├── src/mcb/
│   ├── __init__.py      # Package exports
│   ├── __main__.py      # CLI entry point
│   ├── protocol.py      # MCB Protocol (INQC)
│   ├── amum.py          # AMUM Alignment
│   ├── qci.py           # QCI Coherence
│   └── ethic.py         # ETHIC Principles
├── schemas/
│   └── surrealdb.surql  # SurrealDB schema
├── sql/
│   └── duckdb.sql       # DuckDB schema + macros
├── examples/
│   └── demo.py          # Usage examples
├── pyproject.toml
└── README.md
```

## MCB vs MCP

| | MCB | MCP |
|---|-----|-----|
| **Full Name** | Master Client Bridge | Model Context Protocol |
| **Purpose** | Internal agent-to-agent | Bridge to community |
| **Binary** | 0 = not connected, 1 = ALL CONNECTED | N/A |
| **Encoding** | 4-layer (hex/binary/dot/INQC) | JSON-RPC |

## License

MIT License - Björn Bethge

## Links

- [GitHub](https://github.com/bjoernbethge/mcb)
- [PyPI](https://pypi.org/project/mcp-b/)
