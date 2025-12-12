"""
Pytest configuration and fixtures for typedpg tests.

Uses testcontainers to spin up a PostgreSQL container for each test session.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import TYPE_CHECKING, Any

import asyncpg
import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer

from typedpg.inference import TypeInferrer

if TYPE_CHECKING:
    from asyncpg import Connection

# Path to the schema file
SCHEMA_FILE = Path(__file__).parent / "fixtures" / "schema.sql"


def _get_asyncpg_url(container: PostgresContainer) -> str:
    """Convert testcontainers URL to asyncpg-compatible URL."""
    host = container.get_container_host_ip()
    port = container.get_exposed_port(5432)
    return f"postgresql://test_user:test_password@{host}:{port}/test_db"


@pytest.fixture(scope="session")
def postgres_container() -> PostgresContainer:
    """Start a PostgreSQL container for the test session."""
    postgres = PostgresContainer(
        image="postgres:16-alpine",
        username="test_user",
        password="test_password",
        dbname="test_db",
    )
    postgres.start()

    # Run schema migrations using psycopg2
    import psycopg2

    host = postgres.get_container_host_ip()
    port = postgres.get_exposed_port(5432)

    conn = psycopg2.connect(
        host=host,
        port=port,
        user="test_user",
        password="test_password",
        dbname="test_db",
    )
    conn.autocommit = True
    cursor = conn.cursor()

    schema_sql = SCHEMA_FILE.read_text()
    cursor.execute(schema_sql)

    cursor.close()
    conn.close()

    yield postgres

    postgres.stop()


@pytest.fixture(scope="session")
def database_url(postgres_container: PostgresContainer) -> str:
    """Get the database URL for asyncpg."""
    return _get_asyncpg_url(postgres_container)


@pytest_asyncio.fixture
async def db_conn(database_url: str) -> AsyncGenerator[Connection[Any], None]:
    """Create a database connection for a test."""
    conn = await asyncpg.connect(database_url)
    try:
        yield conn
    finally:
        await conn.close()


@pytest_asyncio.fixture
async def inferrer(db_conn: Connection[Any]) -> TypeInferrer:
    """Create a TypeInferrer instance."""
    return TypeInferrer(db_conn)
