"""
PostgreSQL plugin for Daita Agents.

Simple database connection and querying - no over-engineering.
"""
import logging
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from .base_db import BaseDatabasePlugin

if TYPE_CHECKING:
    from ..core.tools import AgentTool

logger = logging.getLogger(__name__)

class PostgreSQLPlugin(BaseDatabasePlugin):
    """
    PostgreSQL plugin for agents with standardized connection management.
    
    Inherits common database functionality from BaseDatabasePlugin.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "",
        username: str = "",
        user: Optional[str] = None,  # Add this
        password: str = "",
        connection_string: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize PostgreSQL connection.
        
        Args:
            host: Database host
            port: Database port
            database: Database name
            username: Username
            user: Username (alias for username)
            password: Password
            connection_string: Full connection string (overrides individual params)
            **kwargs: Additional asyncpg parameters
        """
        # Use 'user' parameter as alias for 'username' if provided
        effective_username = user if user is not None else username
        
        # Build connection string
        if connection_string:
            self.connection_string = connection_string
        else:
            self.connection_string = f"postgresql://{effective_username}:{password}@{host}:{port}/{database}"
        
        # PostgreSQL-specific pool configuration
        self.pool_config = {
            'min_size': kwargs.get('min_size', 1),
            'max_size': kwargs.get('max_size', 10),
            'command_timeout': kwargs.get('command_timeout', 60),
            'statement_cache_size': kwargs.get('statement_cache_size', 0),  # Set to 0 for pgbouncer compatibility
        }
        
        # Initialize base class with all config
        super().__init__(
            host=host, port=port, database=database, 
            username=effective_username, connection_string=connection_string,
            **kwargs
        )
        
        logger.debug(f"PostgreSQL plugin configured for {host}:{port}/{database}")
    
    async def connect(self):
        """Connect to PostgreSQL database."""
        if self._pool is not None:
            return  # Already connected
        
        try:
            import asyncpg
            self._pool = await asyncpg.create_pool(
                self.connection_string,
                **self.pool_config
            )
            logger.info("Connected to PostgreSQL")
        except ImportError:
            self._handle_connection_error(
                ImportError("asyncpg not installed. Run: pip install asyncpg"),
                "connection"
            )
        except Exception as e:
            self._handle_connection_error(e, "connection")
    
    async def disconnect(self):
        """Disconnect from PostgreSQL database."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("Disconnected from PostgreSQL")
    
    async def query(self, sql: str, params: Optional[List] = None) -> List[Dict[str, Any]]:
        """
        Run a SELECT query and return results.
        
        Args:
            sql: SQL query with $1, $2, etc. placeholders
            params: List of parameters for the query
            
        Returns:
            List of rows as dictionaries
            
        Example:
            results = await db.query("SELECT * FROM users WHERE age > $1", [25])
        """
        # Only auto-connect if pool is None - allows manual mocking
        if self._pool is None:
            await self.connect()
        
        async with self._pool.acquire() as conn:
            if params:
                rows = await conn.fetch(sql, *params)
            else:
                rows = await conn.fetch(sql)
            
            return [dict(row) for row in rows]
    
    async def execute(self, sql: str, params: Optional[List] = None) -> int:
        """
        Execute INSERT/UPDATE/DELETE and return affected rows.
        
        Args:
            sql: SQL statement
            params: List of parameters
            
        Returns:
            Number of affected rows
        """
        # Only auto-connect if pool is None - allows manual mocking
        if self._pool is None:
            await self.connect()
        
        async with self._pool.acquire() as conn:
            if params:
                result = await conn.execute(sql, *params)
            else:
                result = await conn.execute(sql)
            
            # Extract number from result like "INSERT 0 5"
            return int(result.split()[-1]) if result else 0
    
    async def insert_many(self, table: str, data: List[Dict[str, Any]]) -> int:
        """
        Bulk insert data into a table.
        
        Args:
            table: Table name
            data: List of dictionaries to insert
            
        Returns:
            Number of rows inserted
        """
        if not data:
            return 0
        
        # Only auto-connect if pool is None - allows manual mocking
        if self._pool is None:
            await self.connect()
        
        # Get columns from first row
        columns = list(data[0].keys())
        placeholders = ', '.join([f'${i+1}' for i in range(len(columns))])
        
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Convert to list of tuples for executemany
        rows = [[row[col] for col in columns] for row in data]
        
        async with self._pool.acquire() as conn:
            await conn.executemany(sql, rows)
        
        return len(data)
    
    async def tables(self) -> List[str]:
        """List all tables in the database."""
        sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
        """
        results = await self.query(sql)
        return [row['table_name'] for row in results]

    def get_tools(self) -> List['AgentTool']:
        """
        Expose PostgreSQL operations as agent tools.

        Returns:
            List of AgentTool instances for database operations
        """
        from ..core.tools import AgentTool

        return [
            AgentTool(
                name="query_database",
                description="Execute a SQL SELECT query on the PostgreSQL database and return results as a list of dictionaries",
                parameters={
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL SELECT query with $1, $2, etc. placeholders for parameters"
                        },
                        "params": {
                            "type": "array",
                            "description": "Optional list of parameter values for query placeholders",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["sql"]
                },
                handler=self._tool_query,
                category="database",
                source="plugin",
                plugin_name="PostgreSQL",
                timeout_seconds=60
            ),
            AgentTool(
                name="list_tables",
                description="List all tables in the PostgreSQL database",
                parameters={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
                handler=self._tool_list_tables,
                category="database",
                source="plugin",
                plugin_name="PostgreSQL",
                timeout_seconds=30
            ),
            AgentTool(
                name="get_table_schema",
                description="Get column information (name, data type, nullable) for a specific table in PostgreSQL",
                parameters={
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to inspect"
                        }
                    },
                    "required": ["table_name"]
                },
                handler=self._tool_get_schema,
                category="database",
                source="plugin",
                plugin_name="PostgreSQL",
                timeout_seconds=30
            ),
            AgentTool(
                name="execute_sql",
                description="Execute an INSERT, UPDATE, or DELETE SQL statement on PostgreSQL. Returns the number of affected rows.",
                parameters={
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL statement to execute (INSERT, UPDATE, or DELETE)"
                        },
                        "params": {
                            "type": "array",
                            "description": "Optional list of parameter values for statement placeholders",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["sql"]
                },
                handler=self._tool_execute,
                category="database",
                source="plugin",
                plugin_name="PostgreSQL",
                timeout_seconds=60
            )
        ]

    async def _tool_query(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tool handler for query_database"""
        sql = args.get("sql")
        params = args.get("params")

        results = await self.query(sql, params)

        return {
            "success": True,
            "rows": results,
            "row_count": len(results)
        }

    async def _tool_list_tables(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tool handler for list_tables"""
        tables = await self.tables()

        return {
            "success": True,
            "tables": tables,
            "count": len(tables)
        }

    async def _tool_get_schema(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tool handler for get_table_schema"""
        table_name = args.get("table_name")

        schema_query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = $1
            ORDER BY ordinal_position
        """

        columns = await self.query(schema_query, [table_name])

        return {
            "success": True,
            "table": table_name,
            "columns": columns,
            "column_count": len(columns)
        }

    async def _tool_execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tool handler for execute_sql"""
        sql = args.get("sql")
        params = args.get("params")

        affected_rows = await self.execute(sql, params)

        return {
            "success": True,
            "affected_rows": affected_rows
        }

def postgresql(**kwargs) -> PostgreSQLPlugin:
    """Create PostgreSQL plugin with simplified interface."""
    return PostgreSQLPlugin(**kwargs)