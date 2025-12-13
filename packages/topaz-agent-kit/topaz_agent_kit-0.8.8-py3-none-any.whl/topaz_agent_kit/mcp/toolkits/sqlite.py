"""SQLite MCP Toolkit - Generic database operations for SQLite databases.

Provides tools for querying and executing SQL operations on SQLite database files.
Supports SELECT queries and INSERT/UPDATE/DELETE operations with parameterized queries.
"""

import sqlite3
import json
import os
from typing import Any, Dict, List, Optional
from topaz_agent_kit.utils.logger import Logger
from fastmcp import FastMCP


class SQLiteMCPTools:
    """MCP toolkit for SQLite database operations."""
    
    def __init__(self, **kwargs):
        self._logger = Logger("MCP.SQLite")
    
    def _validate_db_file(self, db_file: str) -> None:
        """Validate that database file exists and is accessible."""
        if not db_file:
            raise ValueError("db_file parameter is required")
        
        if not os.path.exists(db_file):
            raise FileNotFoundError(f"Database file not found: {db_file}")
        
        if not os.path.isfile(db_file):
            raise ValueError(f"Path is not a file: {db_file}")
    
    def _execute_query(
        self, 
        db_file: str, 
        query: str, 
        params: Optional[List[Any]] = None,
        fetch_results: bool = True
    ) -> Any:
        """Execute a SQL query and return results."""
        self._validate_db_file(db_file)
        
        if not query or not query.strip():
            raise ValueError("query parameter is required and cannot be empty")
        
        try:
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
            cursor = conn.cursor()
            
            # Execute query with parameters
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Fetch results if it's a SELECT query
            if fetch_results:
                rows = cursor.fetchall()
                # Convert rows to list of dicts
                result = [dict(row) for row in rows]
            else:
                # For INSERT/UPDATE/DELETE, return affected rows and last insert id
                conn.commit()
                result = {
                    "rows_affected": cursor.rowcount,
                    "last_insert_id": cursor.lastrowid
                }
            
            cursor.close()
            conn.close()
            
            return result
            
        except sqlite3.Error as e:
            self._logger.error("SQLite error: {}", e)
            raise RuntimeError(f"Database error: {str(e)}")
        except Exception as e:
            self._logger.error("Unexpected error: {}", e)
            raise
    
    def register(self, mcp: FastMCP) -> None:
        """Register SQLite tools with MCP server."""
        
        @mcp.tool(name="sqlite_query")
        def sqlite_query(db_file: str, query: str, params: Optional[List[Any]] = None) -> str:
            """Execute a SELECT query on SQLite database and return results as JSON.
            
            Args:
                db_file: Path to SQLite database file
                query: SQL SELECT query (parameterized queries supported with ? placeholders)
                params: Optional list of parameters for parameterized query
            
            Returns:
                JSON string containing array of result rows (each row is a dict)
            
            Example:
                sqlite_query(
                    db_file="/path/to/db.db",
                    query="SELECT * FROM purchase_orders WHERE po_number = ?",
                    params=["PO-2024-123"]
                )
            """
            self._logger.input("sqlite_query INPUT: db_file={}, query={}, params={}", 
                             db_file, query[:100] if len(query) > 100 else query, params)
            
            try:
                # Validate that this is a SELECT query (basic check)
                query_upper = query.strip().upper()
                if not query_upper.startswith("SELECT"):
                    raise ValueError("sqlite_query only supports SELECT queries. Use sqlite_execute for INSERT/UPDATE/DELETE.")
                
                result = self._execute_query(db_file, query, params, fetch_results=True)
                result_json = json.dumps(result, default=str)  # default=str handles dates, etc.
                
                self._logger.output("sqlite_query OUTPUT: {} rows returned", len(result))
                return result_json
                
            except Exception as e:
                self._logger.error("sqlite_query failed: {}", e)
                raise
        
        @mcp.tool(name="sqlite_execute")
        def sqlite_execute(db_file: str, query: str, params: List[Any]) -> str:
            """Execute INSERT, UPDATE, or DELETE query on SQLite database.
            
            Args:
                db_file: Path to SQLite database file
                query: SQL INSERT/UPDATE/DELETE query (parameterized queries with ? placeholders)
                params: List of parameters for parameterized query (required)
            
            Returns:
                JSON string with rows_affected and last_insert_id (for INSERT)
            
            Example:
                sqlite_execute(
                    db_file="/path/to/db.db",
                    query="INSERT INTO invoice_processing (invoice_file, status) VALUES (?, ?)",
                    params=["invoice_001.pdf", "approved"]
                )
            """
            self._logger.input("sqlite_execute INPUT: db_file={}, query={}, params={}", 
                             db_file, query[:100] if len(query) > 100 else query, params)
            
            try:
                # Validate that this is not a SELECT query
                query_upper = query.strip().upper()
                if query_upper.startswith("SELECT"):
                    raise ValueError("sqlite_execute does not support SELECT queries. Use sqlite_query for SELECT.")
                
                if params is None:
                    raise ValueError("params parameter is required for sqlite_execute")
                
                result = self._execute_query(db_file, query, params, fetch_results=False)
                result_json = json.dumps(result, default=str)
                
                self._logger.output("sqlite_execute OUTPUT: rows_affected={}, last_insert_id={}", 
                                   result.get("rows_affected"), result.get("last_insert_id"))
                return result_json
                
            except Exception as e:
                self._logger.error("sqlite_execute failed: {}", e)
                raise
        
        @mcp.tool(name="sqlite_schema")
        def sqlite_schema(db_file: str, table_name: str) -> str:
            """Get schema information for a table in SQLite database.
            
            Args:
                db_file: Path to SQLite database file
                table_name: Name of the table to get schema for
            
            Returns:
                JSON string containing table schema information (columns, types, constraints)
            
            Example:
                sqlite_schema(
                    db_file="/path/to/db.db",
                    table_name="purchase_orders"
                )
            """
            self._logger.input("sqlite_schema INPUT: db_file={}, table_name={}", db_file, table_name)
            
            try:
                self._validate_db_file(db_file)
                
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Get table info
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                # Get foreign keys
                cursor.execute(f"PRAGMA foreign_key_list({table_name})")
                foreign_keys = cursor.fetchall()
                
                # Get indexes
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = cursor.fetchall()
                
                # Structure the result
                schema = {
                    "table_name": table_name,
                    "columns": [
                        {
                            "cid": col[0],
                            "name": col[1],
                            "type": col[2],
                            "notnull": bool(col[3]),
                            "default_value": col[4],
                            "primary_key": bool(col[5])
                        }
                        for col in columns
                    ],
                    "foreign_keys": [
                        {
                            "id": fk[0],
                            "seq": fk[1],
                            "table": fk[2],
                            "from": fk[3],
                            "to": fk[4],
                            "on_update": fk[5],
                            "on_delete": fk[6],
                            "match": fk[7]
                        }
                        for fk in foreign_keys
                    ],
                    "indexes": [
                        {
                            "seq": idx[0],
                            "name": idx[1],
                            "unique": bool(idx[2]),
                            "origin": idx[3],
                            "partial": bool(idx[4])
                        }
                        for idx in indexes
                    ]
                }
                
                cursor.close()
                conn.close()
                
                result_json = json.dumps(schema, default=str)
                self._logger.output("sqlite_schema OUTPUT: {} columns found", len(schema["columns"]))
                return result_json
                
            except sqlite3.Error as e:
                self._logger.error("sqlite_schema failed: {}", e)
                raise RuntimeError(f"Database error: {str(e)}")
            except Exception as e:
                self._logger.error("sqlite_schema failed: {}", e)
                raise

