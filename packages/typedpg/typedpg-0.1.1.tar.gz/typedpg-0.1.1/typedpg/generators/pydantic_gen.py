"""
Generate Pydantic models from QuerySpec.
"""

from typedpg.inference import QuerySpec


def to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    result: list[str] = []
    for i, char in enumerate(name):
        if char.isupper() and i > 0:
            result.append("_")
        result.append(char.lower())
    return "".join(result)


def generate_result_class(spec: QuerySpec) -> str:
    """Generate a Pydantic model for query results."""
    if not spec.columns:
        return ""

    class_name = f"{spec.name}Result"
    fields: list[str] = []

    for col in spec.columns:
        type_str = col.python_type
        if col.nullable:
            type_str = f"{type_str} | None"
        fields.append(f"    {col.name}: {type_str}")

    return f"""class {class_name}(BaseModel):
    model_config = ConfigDict(frozen=True)

{chr(10).join(fields)}
"""


def generate_params_class(spec: QuerySpec) -> str:
    """Generate a Pydantic model for query parameters."""
    if not spec.params:
        return ""

    class_name = f"{spec.name}Params"
    fields: list[str] = []

    for param in spec.params:
        fields.append(f"    {param.name}: {param.python_type}")

    return f"""class {class_name}(BaseModel):
    model_config = ConfigDict(frozen=True)

{chr(10).join(fields)}
"""


def generate_query_function(spec: QuerySpec, driver: str = "asyncpg") -> str:
    """Generate an async query function."""
    func_name = to_snake_case(spec.name)
    result_class = f"{spec.name}Result" if spec.columns else "None"

    # Determine return type annotation
    if spec.returns == "one":
        return_type = f"{result_class} | None"
    elif spec.returns == "many":
        return_type = f"list[{result_class}]"
    elif spec.returns == "affected":
        return_type = "int"
    else:
        return_type = "None"

    # Build parameter list
    if spec.params:
        params_arg = f"params: {spec.name}Params"
        param_refs = ", ".join(f"params.{p.name}" for p in spec.params)
    else:
        params_arg = ""
        param_refs = ""

    if driver == "asyncpg":
        return _generate_asyncpg_function(
            spec, func_name, params_arg, param_refs, return_type, result_class
        )
    else:
        return _generate_psycopg_function(
            spec, func_name, params_arg, param_refs, return_type, result_class
        )


def _generate_asyncpg_function(
    spec: QuerySpec,
    func_name: str,
    params_arg: str,
    param_refs: str,
    return_type: str,
    result_class: str,
) -> str:
    """Generate asyncpg-specific query function."""
    conn_arg = "conn: asyncpg.Connection[Any]"
    args = f"{conn_arg}, {params_arg}" if params_arg else conn_arg

    sql_literal = f'"""{spec.sql}"""'

    if param_refs:
        fetch_args = f"\n        {sql_literal},\n        {param_refs},\n    "
    else:
        fetch_args = f"\n        {sql_literal},\n    "

    if spec.returns == "one":
        body = f"""    row = await conn.fetchrow({fetch_args})
    return {result_class}.model_validate(dict(row)) if row else None"""

    elif spec.returns == "many":
        body = f"""    rows = await conn.fetch({fetch_args})
    return [{result_class}.model_validate(dict(row)) for row in rows]"""

    elif spec.returns == "affected":
        body = f"""    result = await conn.execute({fetch_args})
    return int(result.split()[-1])"""

    else:
        body = f"""    await conn.execute({fetch_args})"""

    return f"""async def {func_name}({args}) -> {return_type}:
{body}
"""


def _generate_psycopg_function(
    spec: QuerySpec,
    func_name: str,
    params_arg: str,
    param_refs: str,
    return_type: str,
    result_class: str,
) -> str:
    """Generate psycopg-specific query function."""
    conn_arg = "conn: psycopg.AsyncConnection[Any]"
    args = f"{conn_arg}, {params_arg}" if params_arg else conn_arg

    sql_literal = f'"""{spec.sql}"""'

    if param_refs:
        execute_args = f"{sql_literal}, ({param_refs},)"
    else:
        execute_args = sql_literal

    if spec.returns == "one":
        body = f"""    async with conn.cursor(row_factory=class_row({result_class})) as cur:
        await cur.execute({execute_args})
        return await cur.fetchone()"""

    elif spec.returns == "many":
        body = f"""    async with conn.cursor(row_factory=class_row({result_class})) as cur:
        await cur.execute({execute_args})
        return await cur.fetchall()"""

    elif spec.returns == "affected":
        body = f"""    async with conn.cursor() as cur:
        await cur.execute({execute_args})
        return cur.rowcount or 0"""

    else:
        body = f"""    async with conn.cursor() as cur:
        await cur.execute({execute_args})"""

    return f"""async def {func_name}({args}) -> {return_type}:
{body}
"""


def generate_module(specs: list[QuerySpec], driver: str = "asyncpg") -> str:
    """Generate a complete Python module from multiple query specs."""
    # Collect all required imports
    all_imports: set[str] = set()
    for spec in specs:
        all_imports.update(spec.get_required_imports())

    # Standard imports
    imports = [
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "from pydantic import BaseModel, ConfigDict",
    ]

    # Type-specific imports
    imports.extend(sorted(all_imports))

    # Driver imports
    if driver == "asyncpg":
        imports.append("import asyncpg")
    else:
        imports.append("import psycopg")
        imports.append("from psycopg.rows import class_row")

    # Generate code sections
    sections = [
        '"""',
        "Auto-generated typed queries.",
        "DO NOT EDIT - Generated by typedpg",
        '"""',
        "",
        "\n".join(imports),
        "",
    ]

    for spec in specs:
        if spec.columns:
            sections.append(generate_result_class(spec))
        if spec.params:
            sections.append(generate_params_class(spec))
        sections.append(generate_query_function(spec, driver))

    return "\n\n".join(sections)
