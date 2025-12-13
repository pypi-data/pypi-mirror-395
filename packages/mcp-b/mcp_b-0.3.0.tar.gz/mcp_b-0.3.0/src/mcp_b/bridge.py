"""
MCP-B Database Bridge

Bridges DuckDB (analytics) and SurrealDB (graph) for unified data flow.
DuckDB = SQL analytics, Ollama/LLM macros, time travel
SurrealDB = Graph relations, live queries, vector search
"""

import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

import duckdb

try:
    from surrealdb import Surreal
    HAS_SURREALDB = True
except ImportError:
    HAS_SURREALDB = False
    Surreal = None


@dataclass
class BridgeConfig:
    """Configuration for the database bridge."""
    duckdb_path: str = ":memory:"
    surreal_url: str = "ws://localhost:8000/rpc"
    surreal_namespace: str = "mcp_b"
    surreal_database: str = "main"
    surreal_user: str = "root"
    surreal_pass: str = "root"


class DatabaseBridge:
    """
    Bridges DuckDB (analytics layer) and SurrealDB (graph layer).

    Architecture:
        DuckDB  ←→  Bridge  ←→  SurrealDB
        - SQL Analytics      - Agent Graph (RELATE)
        - Ollama/LLM Macros  - Vector Search
        - Time Travel        - Live Queries
        - http_client ext    - Graph Traversal
    """

    def __init__(self, config: Optional[BridgeConfig] = None):
        self.config = config or BridgeConfig()
        self.duck: Optional[duckdb.DuckDBPyConnection] = None
        self.surreal: Optional[Any] = None
        self._connected = False

    def connect_duckdb(self) -> duckdb.DuckDBPyConnection:
        """Connect to DuckDB."""
        if self.duck is None:
            self.duck = duckdb.connect(self.config.duckdb_path)
            self._load_duckdb_extensions()
        return self.duck

    def _load_duckdb_extensions(self):
        """Load required DuckDB extensions."""
        extensions = [
            ("http_client", "community"),
            ("json", None),
        ]
        for ext, source in extensions:
            try:
                if source:
                    self.duck.execute(f"INSTALL {ext} FROM {source}")
                self.duck.execute(f"LOAD {ext}")
            except Exception:
                pass  # Extension may already be loaded or not available

    async def connect_surreal(self) -> Any:
        """Connect to SurrealDB."""
        if not HAS_SURREALDB:
            raise ImportError("surrealdb package not installed")

        if self.surreal is None:
            self.surreal = Surreal(self.config.surreal_url)
            await self.surreal.connect()
            await self.surreal.signin({
                "user": self.config.surreal_user,
                "pass": self.config.surreal_pass
            })
            await self.surreal.use(
                self.config.surreal_namespace,
                self.config.surreal_database
            )
        return self.surreal

    async def connect(self):
        """Connect to both databases."""
        self.connect_duckdb()
        if HAS_SURREALDB:
            await self.connect_surreal()
        self._connected = True

    async def close(self):
        """Close all connections."""
        if self.duck:
            self.duck.close()
            self.duck = None
        if self.surreal:
            await self.surreal.close()
            self.surreal = None
        self._connected = False

    # =========================================
    # SYNC OPERATIONS
    # =========================================

    async def sync_agents_to_surreal(self) -> int:
        """Sync agents from DuckDB to SurrealDB graph."""
        if not self.duck or not self.surreal:
            raise RuntimeError("Not connected to both databases")

        # Get agents from DuckDB
        agents = self.duck.execute("""
            SELECT agent_id, name, binary_state::VARCHAR, capabilities
            FROM mcb_agents
        """).fetchall()

        synced = 0
        for agent_id, name, binary_state, capabilities in agents:
            await self.surreal.query("""
                UPSERT mcb_agents SET
                    agent_id = $agent_id,
                    name = $name,
                    binary_state = $binary_state,
                    capabilities = $capabilities,
                    last_seen = time::now()
            """, {
                "agent_id": agent_id,
                "name": name,
                "binary_state": binary_state,
                "capabilities": capabilities
            })
            synced += 1

        return synced

    async def sync_messages_to_duck(self, limit: int = 100) -> int:
        """Sync recent messages from SurrealDB to DuckDB for analytics."""
        if not self.duck or not self.surreal:
            raise RuntimeError("Not connected to both databases")

        # Get recent messages from SurrealDB
        result = await self.surreal.query(f"""
            SELECT * FROM mcb_messages
            ORDER BY timestamp DESC
            LIMIT {limit}
        """)

        messages = result[0]["result"] if result else []
        synced = 0

        for msg in messages:
            try:
                self.duck.execute("""
                    INSERT INTO mcb_messages (raw_message, source_id, dest_id, binary_state, command, payload)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT DO NOTHING
                """, [
                    msg.get("raw_message"),
                    msg.get("source_id"),
                    msg.get("dest_id"),
                    msg.get("binary_state"),
                    msg.get("command"),
                    str(msg.get("payload", {}))
                ])
                synced += 1
            except Exception:
                pass

        return synced

    # =========================================
    # GRAPH OPERATIONS (SurrealDB)
    # =========================================

    async def get_agent_network(self) -> List[Dict[str, Any]]:
        """Get the full agent network graph from SurrealDB."""
        if not self.surreal:
            raise RuntimeError("Not connected to SurrealDB")

        result = await self.surreal.query("""
            SELECT
                id, name, agent_id, binary_state,
                ->connects->mcb_agents.name AS connects_to,
                <-connects<-mcb_agents.name AS connected_from
            FROM mcb_agents
        """)

        return result[0]["result"] if result else []

    async def create_agent_connection(
        self,
        source_agent: str,
        dest_agent: str,
        connection_type: str = "communicates"
    ) -> Dict[str, Any]:
        """Create a connection between two agents in the graph."""
        if not self.surreal:
            raise RuntimeError("Not connected to SurrealDB")

        result = await self.surreal.query("""
            RELATE (SELECT id FROM mcb_agents WHERE agent_id = $source LIMIT 1)
                -> connects ->
                (SELECT id FROM mcb_agents WHERE agent_id = $dest LIMIT 1)
            SET
                connection_type = $conn_type,
                binary_state = '1111111111111111'
        """, {
            "source": source_agent,
            "dest": dest_agent,
            "conn_type": connection_type
        })

        return result[0] if result else {}

    # =========================================
    # ANALYTICS OPERATIONS (DuckDB)
    # =========================================

    def get_message_analytics(self) -> Dict[str, Any]:
        """Get message flow analytics from DuckDB."""
        if not self.duck:
            raise RuntimeError("Not connected to DuckDB")

        # Message counts by command
        command_counts = self.duck.execute("""
            SELECT command, COUNT(*) as count
            FROM mcb_messages
            GROUP BY command
            ORDER BY count DESC
        """).fetchall()

        # Agent activity
        agent_activity = self.duck.execute("""
            SELECT source_id, COUNT(*) as sent,
                   (SELECT COUNT(*) FROM mcb_messages m2 WHERE m2.dest_id = m1.source_id) as received
            FROM mcb_messages m1
            GROUP BY source_id
            ORDER BY sent DESC
        """).fetchall()

        return {
            "command_distribution": dict(command_counts),
            "agent_activity": [
                {"agent": a[0], "sent": a[1], "received": a[2]}
                for a in agent_activity
            ]
        }

    def run_sql(self, query: str) -> Any:
        """Run a SQL query on DuckDB."""
        if not self.duck:
            self.connect_duckdb()
        return self.duck.execute(query).fetchall()

    async def run_surql(self, query: str, params: Optional[Dict] = None) -> Any:
        """Run a SurrealQL query on SurrealDB."""
        if not self.surreal:
            await self.connect_surreal()
        result = await self.surreal.query(query, params or {})
        return result[0]["result"] if result else []

    # =========================================
    # STATUS
    # =========================================

    def status(self) -> Dict[str, Any]:
        """Get bridge connection status."""
        return {
            "duckdb": {
                "connected": self.duck is not None,
                "path": self.config.duckdb_path
            },
            "surrealdb": {
                "connected": self.surreal is not None,
                "url": self.config.surreal_url,
                "namespace": self.config.surreal_namespace,
                "database": self.config.surreal_database,
                "available": HAS_SURREALDB
            },
            "bridge_active": self._connected
        }


# Convenience functions
def create_bridge(
    duckdb_path: str = ":memory:",
    surreal_url: str = "ws://localhost:8000/rpc"
) -> DatabaseBridge:
    """Create a new database bridge."""
    config = BridgeConfig(
        duckdb_path=duckdb_path,
        surreal_url=surreal_url
    )
    return DatabaseBridge(config)


async def quick_sync(bridge: DatabaseBridge) -> Dict[str, int]:
    """Quick sync between databases."""
    await bridge.connect()
    agents_synced = await bridge.sync_agents_to_surreal()
    messages_synced = await bridge.sync_messages_to_duck()
    return {
        "agents_to_surreal": agents_synced,
        "messages_to_duck": messages_synced
    }
