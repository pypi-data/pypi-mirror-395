"""
MCB (Multiconnection Binary Databridge) Protocol

4-Layer Encoding System for Agent-to-Agent Communication:
- Layer 1: HEX/DECIMAL ROUTING (Agent IDs, routing addresses)
- Layer 2: BINARY STATE VECTORS (Connection states, feature flags)
- Layer 3: DOT-SEPARATED TOKENS (Message boundaries)
- Layer 4: PROTOCOL COMMANDS (INQC: Init/Node/Query/Connect)

MCB vs MCP:
- MCP = Model Context Protocol (bridge TO community)
- MCB = Multiconnection Binary Databridge (internal protocol)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntFlag
from typing import Any
import json
import re


class INQCCommand(Enum):
    """INQC Protocol Commands"""
    INIT = "I"      # Initialize connection
    NODE = "N"      # Node registration/discovery
    QUERY = "Q"     # Request data/state
    CONNECT = "C"   # Establish persistent link


class BinaryState(IntFlag):
    """16-bit Binary State Flags"""
    CONNECTED = 1 << 0      # Bit 0: Connection active
    AUTHENTICATED = 1 << 1  # Bit 1: Auth verified
    ENCRYPTED = 1 << 2      # Bit 2: Encryption enabled
    COMPRESSED = 1 << 3     # Bit 3: Compression enabled
    STREAMING = 1 << 4      # Bit 4: Streaming mode
    BIDIRECTIONAL = 1 << 5  # Bit 5: Two-way communication
    PERSISTENT = 1 << 6     # Bit 6: Persistent connection
    PRIORITY = 1 << 7       # Bit 7: High priority
    # Bits 8-15: Reserved for custom flags
    
    @classmethod
    def from_string(cls, binary_str: str) -> "BinaryState":
        """Parse binary string to BinaryState"""
        return cls(int(binary_str, 2))
    
    def to_string(self, width: int = 16) -> str:
        """Convert to binary string"""
        return format(self.value, f'0{width}b')
    
    @classmethod
    def all_connected(cls) -> "BinaryState":
        """Return fully connected state (all 1s)"""
        return cls(0xFFFF)


@dataclass
class MCBMessage:
    """MCB Protocol Message"""
    source_id: str          # Layer 1: Source agent ID (hex)
    dest_id: str            # Layer 1: Destination agent ID (hex)
    binary_state: BinaryState  # Layer 2: Connection state
    command: INQCCommand    # Layer 4: INQC command
    payload: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def encode(self) -> str:
        """
        Encode message to MCB wire format
        
        Format: {source} {dest} {binary_state} • {payload_json} • {command}
        Example: 7C1 5510 1011101010111111 • {"action":"ping"} • I
        """
        payload_json = json.dumps(self.payload) if self.payload else "{}"
        return (
            f"{self.source_id} {self.dest_id} "
            f"{self.binary_state.to_string()} • "
            f"{payload_json} • {self.command.value}"
        )
    
    @classmethod
    def decode(cls, raw: str) -> "MCBMessage":
        """
        Decode MCB wire format to message
        
        Parses: {source} {dest} {binary} • {payload} • {cmd}
        """
        # Pattern: source dest binary • payload • command
        pattern = r'^(\w+)\s+(\w+)\s+([01]+)\s+•\s+(.+?)\s+•\s+([INQC])$'
        match = re.match(pattern, raw.strip())
        
        if not match:
            raise ValueError(f"Invalid MCB message format: {raw}")
        
        source_id, dest_id, binary_str, payload_str, cmd = match.groups()
        
        return cls(
            source_id=source_id,
            dest_id=dest_id,
            binary_state=BinaryState.from_string(binary_str),
            command=INQCCommand(cmd),
            payload=json.loads(payload_str) if payload_str != "{}" else {}
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            "source_id": self.source_id,
            "dest_id": self.dest_id,
            "binary_state": self.binary_state.to_string(),
            "command": self.command.value,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class MCBAgent:
    """MCB Agent Registration"""
    agent_id: str           # Hex ID (e.g., "7C1", "5510")
    name: str               # Human readable name
    binary_state: BinaryState = BinaryState.CONNECTED
    capabilities: list = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "binary_state": self.binary_state.to_string(),
            "capabilities": self.capabilities
        }


class MCBProtocol:
    """MCB Protocol Handler"""
    
    def __init__(self, agent: MCBAgent):
        self.agent = agent
        self.connections: dict[str, MCBAgent] = {}
        self.message_log: list[MCBMessage] = []
    
    def init_connection(self, target: MCBAgent) -> MCBMessage:
        """Send INIT command to establish connection"""
        msg = MCBMessage(
            source_id=self.agent.agent_id,
            dest_id=target.agent_id,
            binary_state=BinaryState.CONNECTED,
            command=INQCCommand.INIT,
            payload={"agent_name": self.agent.name}
        )
        self.message_log.append(msg)
        return msg
    
    def register_node(self, capabilities: list) -> MCBMessage:
        """Send NODE command for discovery"""
        msg = MCBMessage(
            source_id=self.agent.agent_id,
            dest_id="BROADCAST",
            binary_state=self.agent.binary_state,
            command=INQCCommand.NODE,
            payload={"capabilities": capabilities}
        )
        self.message_log.append(msg)
        return msg
    
    def query(self, target_id: str, query_data: dict) -> MCBMessage:
        """Send QUERY command to request data"""
        msg = MCBMessage(
            source_id=self.agent.agent_id,
            dest_id=target_id,
            binary_state=self.agent.binary_state,
            command=INQCCommand.QUERY,
            payload=query_data
        )
        self.message_log.append(msg)
        return msg
    
    def connect(self, target: MCBAgent) -> MCBMessage:
        """Send CONNECT command for persistent link"""
        self.connections[target.agent_id] = target
        msg = MCBMessage(
            source_id=self.agent.agent_id,
            dest_id=target.agent_id,
            binary_state=BinaryState.CONNECTED | BinaryState.PERSISTENT,
            command=INQCCommand.CONNECT,
            payload={"persistent": True}
        )
        self.message_log.append(msg)
        return msg


# Convenience functions
def encode_mcb(source: str, dest: str, state: int, cmd: str, payload: dict = None) -> str:
    """Quick encode MCB message"""
    msg = MCBMessage(
        source_id=source,
        dest_id=dest,
        binary_state=BinaryState(state),
        command=INQCCommand(cmd),
        payload=payload or {}
    )
    return msg.encode()


def decode_mcb(raw: str) -> dict:
    """Quick decode MCB message to dict"""
    return MCBMessage.decode(raw).to_dict()
