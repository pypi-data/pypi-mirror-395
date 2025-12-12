"""
Command-line interface for typedpg.
"""

import asyncio
import sys
from pathlib import Path
from typing import Any

import asyncpg
import click

from typedpg.generators.dataclass_gen import generate_module as generate_dataclass_module
from typedpg.generators.pydantic_gen import generate_module as generate_pydantic_module
from typedpg.inference import QuerySpec, TypeInferrer
from typedpg.parser import parse_python_file, parse_sql_directory, parse_sql_file


async def process_queries(
    dsn: str,
    sql_path: Path,
    output_path: Path,
    driver: str = "asyncpg",
    model_type: str = "dataclass",
) -> bool:
    """Process SQL files and generate typed Python code."""
    click.echo("Connecting to database...")

    try:
        conn: asyncpg.Connection[Any] = await asyncpg.connect(dsn)
    except Exception as e:
        click.echo(f"Error connecting to database: {e}", err=True)
        return False

    try:
        inferrer = TypeInferrer(conn)

        click.echo(f"Parsing files from {sql_path}...")
        if sql_path.is_file():
            content = sql_path.read_text()
            if sql_path.suffix == ".py":
                parsed_queries = parse_python_file(content, source_file=str(sql_path))
            else:
                parsed_queries = parse_sql_file(content, source_file=str(sql_path))
        else:
            parsed_queries = parse_sql_directory(sql_path)

        if not parsed_queries:
            click.echo(
                "No queries found. Use @name annotations or @query decorators.",
                err=True,
            )
            return False

        click.echo(f"Found {len(parsed_queries)} queries")

        specs: list[QuerySpec] = []
        for pq in parsed_queries:
            click.echo(f"  Analyzing: {pq.name}")
            try:
                spec = await inferrer.analyze_query(pq.sql, pq.name, pq.param_names)
                if pq.returns:
                    spec.returns = pq.returns
                specs.append(spec)
            except asyncpg.PostgresSyntaxError as e:
                click.echo(f"    SQL syntax error: {e}", err=True)
                if pq.source_file:
                    click.echo(f"    File: {pq.source_file}:{pq.line_number}", err=True)
                return False
            except Exception as e:
                click.echo(f"    Error: {e}", err=True)
                return False

        click.echo(f"Generating {model_type} code for {driver}...")

        if model_type == "pydantic":
            code = generate_pydantic_module(specs, driver=driver)
        else:
            code = generate_dataclass_module(specs, driver=driver)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(code)
        click.echo(f"Written to {output_path}")
        return True

    finally:
        await conn.close()


async def watch_and_generate(
    dsn: str,
    sql_path: Path,
    output_path: Path,
    driver: str,
    model_type: str,
) -> None:
    """Watch for file changes and regenerate."""
    try:
        from watchfiles import awatch
    except ImportError:
        click.echo("watchfiles not installed. Run: pip install watchfiles", err=True)
        sys.exit(1)

    click.echo(f"Watching {sql_path} for changes...")

    # Initial generation
    await process_queries(dsn, sql_path, output_path, driver, model_type)

    watch_path = sql_path if sql_path.is_dir() else sql_path.parent

    async for changes in awatch(watch_path):
        relevant_changes = [
            c for c in changes if c[1].endswith(".sql") or c[1].endswith(".py")
        ]
        if relevant_changes:
            click.echo(f"\nDetected changes in {len(relevant_changes)} file(s), regenerating...")
            await process_queries(dsn, sql_path, output_path, driver, model_type)


@click.command()
@click.argument("sql_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=Path("generated_queries.py"),
    help="Output Python file",
)
@click.option(
    "-d",
    "--dsn",
    default="postgresql://postgres:postgres@localhost/postgres",
    help="Database connection string",
)
@click.option(
    "--driver",
    type=click.Choice(["asyncpg", "psycopg"]),
    default="asyncpg",
    help="Target database driver",
)
@click.option(
    "--model",
    type=click.Choice(["dataclass", "pydantic"]),
    default="dataclass",
    help="Model type to generate",
)
@click.option(
    "-w",
    "--watch",
    is_flag=True,
    help="Watch for file changes and regenerate",
)
def main(
    sql_path: Path,
    output: Path,
    dsn: str,
    driver: str,
    model: str,
    watch: bool,
) -> None:
    """Generate typed Python code from SQL queries.

    SQL_PATH can be a single .sql/.py file or a directory containing query files.

    Supports:
      - .sql files with /* @name ... */ annotations
      - .py files with @query decorator or inline /* @name ... */ comments

    Example:
        typedpg queries/ -o src/db/queries.py -d postgresql://user:pass@localhost/mydb
        typedpg queries.py -o generated.py -d postgresql://localhost/mydb
    """
    if watch:
        asyncio.run(watch_and_generate(dsn, sql_path, output, driver, model))
    else:
        success = asyncio.run(process_queries(dsn, sql_path, output, driver, model))
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
