"""
Type inference engine using asyncpg's prepared statement introspection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from asyncpg import Connection

PG_TYPE_MAP: dict[str, str] = {
    # Integers
    "int2": "int",
    "int4": "int",
    "int8": "int",
    "smallint": "int",
    "integer": "int",
    "bigint": "int",
    "serial": "int",
    "bigserial": "int",
    "smallserial": "int",
    "oid": "int",
    # Floats
    "float4": "float",
    "float8": "float",
    "real": "float",
    "double precision": "float",
    "numeric": "Decimal",
    "money": "Decimal",
    # Strings
    "text": "str",
    "varchar": "str",
    "char": "str",
    "character varying": "str",
    "character": "str",
    "name": "str",
    "bpchar": "str",
    "citext": "str",
    # Boolean
    "bool": "bool",
    "boolean": "bool",
    # Date/Time
    "timestamp": "datetime",
    "timestamptz": "datetime",
    "timestamp without time zone": "datetime",
    "timestamp with time zone": "datetime",
    "date": "date",
    "time": "time",
    "timetz": "time",
    "time without time zone": "time",
    "time with time zone": "time",
    "interval": "timedelta",
    # Binary
    "bytea": "bytes",
    # UUID
    "uuid": "UUID",
    # JSON
    "json": "Any",
    "jsonb": "Any",
    # Network
    "inet": "str",
    "cidr": "str",
    "macaddr": "str",
    "macaddr8": "str",
    # Geometric (return as strings for simplicity)
    "point": "str",
    "line": "str",
    "lseg": "str",
    "box": "str",
    "path": "str",
    "polygon": "str",
    "circle": "str",
    # Arrays (common ones)
    "_int2": "list[int]",
    "_int4": "list[int]",
    "_int8": "list[int]",
    "_text": "list[str]",
    "_varchar": "list[str]",
    "_float4": "list[float]",
    "_float8": "list[float]",
    "_bool": "list[bool]",
    "_uuid": "list[UUID]",
    "_timestamp": "list[datetime]",
    "_timestamptz": "list[datetime]",
    "_date": "list[date]",
    "_numeric": "list[Decimal]",
    "_jsonb": "list[Any]",
    "_json": "list[Any]",
}

PYTHON_TYPE_IMPORTS: dict[str, str] = {
    "datetime": "from datetime import datetime",
    "date": "from datetime import date",
    "time": "from datetime import time",
    "timedelta": "from datetime import timedelta",
    "Decimal": "from decimal import Decimal",
    "UUID": "from uuid import UUID",
    "Any": "from typing import Any",
}


@dataclass
class ColumnInfo:
    """Information about a result column."""

    name: str
    pg_type: str
    pg_oid: int
    python_type: str
    nullable: bool = True


@dataclass
class ParamInfo:
    """Information about a query parameter."""

    index: int  # 1-based ($1, $2, etc.)
    name: str  # Derived name or generic param_N
    pg_type: str
    pg_oid: int
    python_type: str


@dataclass
class QuerySpec:
    """Complete specification for a typed query."""

    name: str
    sql: str
    params: list[ParamInfo] = field(default_factory=list)
    columns: list[ColumnInfo] = field(default_factory=list)
    returns: str = "many"  # 'one', 'many', 'exec', 'affected'

    def get_required_imports(self) -> set[str]:
        """Get Python imports needed for this query's types."""
        imports: set[str] = set()
        all_types = [p.python_type for p in self.params] + [c.python_type for c in self.columns]

        for t in all_types:
            # Handle generic types like list[int]
            base_type = t.split("[")[0] if "[" in t else t
            inner_match = t.split("[")[1].rstrip("]") if "[" in t else None

            if base_type in PYTHON_TYPE_IMPORTS:
                imports.add(PYTHON_TYPE_IMPORTS[base_type])
            if inner_match and inner_match in PYTHON_TYPE_IMPORTS:
                imports.add(PYTHON_TYPE_IMPORTS[inner_match])

        return imports


class TypeInferrer:
    """Infers Python types from PostgreSQL queries using a live database connection."""

    def __init__(self, conn: Connection[Any]) -> None:
        self.conn = conn
        self._type_cache: dict[int, str] = {}

    async def _get_type_name(self, oid: int) -> str:
        """Look up a PostgreSQL type name from its OID."""
        if oid in self._type_cache:
            return self._type_cache[oid]

        row = await self.conn.fetchrow("SELECT typname FROM pg_type WHERE oid = $1", oid)
        if row:
            self._type_cache[oid] = row["typname"]
            return str(row["typname"])
        return "unknown"

    def _map_pg_to_python(self, pg_type: str) -> str:
        """Map a PostgreSQL type name to a Python type."""
        pg_type = pg_type.lower().strip()

        if pg_type in PG_TYPE_MAP:
            return PG_TYPE_MAP[pg_type]

        # Array types (start with underscore)
        if pg_type.startswith("_"):
            element_type = pg_type[1:]
            python_element = self._map_pg_to_python(element_type)
            return f"list[{python_element}]"

        return "Any"

    async def analyze_query(
        self,
        sql: str,
        name: str,
        param_names: list[str] | None = None,
    ) -> QuerySpec:
        """
        Analyze a SQL query and return its type specification.

        Uses PostgreSQL's PREPARE to get type information without executing the query.
        """
        stmt = await self.conn.prepare(sql)

        # Extract parameter types
        params: list[ParamInfo] = []
        param_types = stmt.get_parameters()
        for i, param_type in enumerate(param_types):
            pg_type = param_type.name
            if param_names and i < len(param_names):
                param_name = param_names[i]
            else:
                param_name = f"param_{i + 1}"
            params.append(
                ParamInfo(
                    index=i + 1,
                    name=param_name,
                    pg_type=pg_type,
                    pg_oid=param_type.oid,
                    python_type=self._map_pg_to_python(pg_type),
                )
            )

        # Extract result column types
        columns: list[ColumnInfo] = []
        for attr in stmt.get_attributes():
            columns.append(
                ColumnInfo(
                    name=attr.name,
                    pg_type=attr.type.name,
                    pg_oid=attr.type.oid,
                    python_type=self._map_pg_to_python(attr.type.name),
                    nullable=True,
                )
            )

        returns = self._infer_return_type(sql, columns)

        return QuerySpec(
            name=name,
            sql=sql,
            params=params,
            columns=columns,
            returns=returns,
        )

    def _infer_return_type(self, sql: str, columns: list[ColumnInfo]) -> str:
        """Heuristically determine if query returns one, many, or no rows."""
        sql_upper = sql.upper().strip()

        # No columns = exec or affected
        if not columns:
            if any(kw in sql_upper for kw in ["INSERT", "UPDATE", "DELETE"]):
                return "affected"
            return "exec"

        # LIMIT 1 or single-row functions
        if "LIMIT 1" in sql_upper or "FETCH FIRST 1" in sql_upper:
            return "one"

        # Primary key lookups (heuristic)
        if "WHERE" in sql_upper and "=" in sql_upper and sql.count("$") == 1:
            return "one"

        return "many"
