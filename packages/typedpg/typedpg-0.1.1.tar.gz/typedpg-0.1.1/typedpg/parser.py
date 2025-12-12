"""
Parse annotated SQL files to extract named queries.

Supports:
- .sql files with /* @name ... */ annotations
- .py files with @query decorator or inline /* @name ... */ comments
"""

import ast
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ParsedQuery:
    """A query parsed from an SQL file."""

    name: str
    sql: str
    returns: str | None = None
    param_names: list[str] | None = None
    line_number: int = 0
    source_file: str | None = None


def parse_sql_file(content: str, source_file: str | None = None) -> list[ParsedQuery]:
    """
    Parse an SQL file with pgtyped-style annotations.

    Format:
        /* @name QueryName */
        SELECT * FROM table WHERE id = $1;

        /* @name InsertThing @returns one */
        INSERT INTO things (x) VALUES ($1) RETURNING *;

        /* @name GetUser @param userId @param includeDeleted */
        SELECT * FROM users WHERE id = $1 AND ($2 OR deleted_at IS NULL);
    """
    queries: list[ParsedQuery] = []

    # Pattern for annotation comments
    # Matches: /* @name QueryName [@returns one|many|exec|affected] [@param name]* */
    annotation_pattern = re.compile(
        r"/\*\s*@name\s+(\w+)"  # Required: @name QueryName
        r"(?:\s+@returns\s+(\w+))?"  # Optional: @returns one|many|exec|affected
        r"((?:\s+@param\s+\w+)*)"  # Optional: @param name (can repeat)
        r"\s*\*/",
        re.IGNORECASE,
    )

    param_pattern = re.compile(r"@param\s+(\w+)", re.IGNORECASE)

    lines = content.split("\n")
    current_annotation: tuple[str, str | None, list[str]] | None = None
    current_sql_lines: list[str] = []
    annotation_line = 0

    for i, line in enumerate(lines, 1):
        match = annotation_pattern.search(line)
        if match:
            # Save previous query if exists
            if current_annotation and current_sql_lines:
                sql = "\n".join(current_sql_lines).strip()
                if sql:
                    queries.append(
                        ParsedQuery(
                            name=current_annotation[0],
                            sql=sql,
                            returns=current_annotation[1],
                            param_names=current_annotation[2] if current_annotation[2] else None,
                            line_number=annotation_line,
                            source_file=source_file,
                        )
                    )

            # Extract param names from the annotation
            param_str = match.group(3) or ""
            param_names = param_pattern.findall(param_str)

            current_annotation = (match.group(1), match.group(2), param_names)
            current_sql_lines = []
            annotation_line = i

            # Handle SQL on same line as annotation
            remaining = line[match.end() :].strip()
            if remaining and not remaining.startswith("/*"):
                current_sql_lines.append(remaining)

        elif current_annotation:
            # Skip empty lines at the start
            if not current_sql_lines and not line.strip():
                continue

            # Accumulate SQL until semicolon
            current_sql_lines.append(line)

            # Check if statement is complete (ends with semicolon)
            full_sql = "\n".join(current_sql_lines)
            if ";" in line:
                # Find the semicolon and truncate there
                sql = full_sql.split(";")[0] + ";"

                queries.append(
                    ParsedQuery(
                        name=current_annotation[0],
                        sql=sql.strip(),
                        returns=current_annotation[1],
                        param_names=current_annotation[2] if current_annotation[2] else None,
                        line_number=annotation_line,
                        source_file=source_file,
                    )
                )
                current_annotation = None
                current_sql_lines = []

    # Handle case where file doesn't end with semicolon
    if current_annotation and current_sql_lines:
        sql = "\n".join(current_sql_lines).strip()
        if sql:
            queries.append(
                ParsedQuery(
                    name=current_annotation[0],
                    sql=sql,
                    returns=current_annotation[1],
                    param_names=current_annotation[2] if current_annotation[2] else None,
                    line_number=annotation_line,
                    source_file=source_file,
                )
            )

    return queries


def parse_python_file(content: str, source_file: str | None = None) -> list[ParsedQuery]:
    """
    Parse a Python file to extract SQL queries.

    Supports two formats:

    1. Decorator style (parsed via regex since Python doesn't allow decorators on variables):
        @query(name="GetUserById", param="userId")
        GET_USER = '''
        SELECT * FROM users WHERE id = $1
        '''

    2. Inline annotation style (same as .sql files):
        GET_USER = '''
        /* @name GetUserById @param userId */
        SELECT * FROM users WHERE id = $1
        '''
    """
    queries: list[ParsedQuery] = []

    # First, parse decorated variables using regex (works even with "invalid" Python syntax)
    # Note: @decorator on a variable is not valid Python, but we support it as a convention
    queries.extend(_parse_decorated_variables(content, source_file))

    # Then, try to parse inline annotations using AST
    # Strip out @query decorators first to make it valid Python
    cleaned_content = _strip_query_decorators(content)

    try:
        tree = ast.parse(cleaned_content)
    except SyntaxError:
        # If AST parsing fails, just return what we found with regex
        return queries

    # Pattern for inline annotations within SQL strings
    annotation_pattern = re.compile(
        r"/\*\s*@name\s+(\w+)"
        r"(?:\s+@returns\s+(\w+))?"
        r"((?:\s+@param\s+\w+)*)"
        r"\s*\*/",
        re.IGNORECASE,
    )
    param_pattern = re.compile(r"@param\s+(\w+)", re.IGNORECASE)

    # Track names we've already found to avoid duplicates
    found_names = {q.name for q in queries}

    for node in ast.walk(tree):
        # Look for assignments with string values containing inline annotations
        if isinstance(node, ast.Assign):
            # Check if the value is a string (the SQL query)
            sql_value: str | None = None
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                sql_value = node.value.value

            if sql_value:
                # Check for inline annotation in the SQL string
                match = annotation_pattern.search(sql_value)
                if match:
                    # Extract the SQL after the annotation
                    sql = sql_value[match.end() :].strip()
                    # Remove trailing comment if present
                    sql = re.sub(r"\s*/\*.*?\*/\s*$", "", sql, flags=re.DOTALL).strip()

                    param_str = match.group(3) or ""
                    param_names = param_pattern.findall(param_str)

                    name = match.group(1)
                    # Skip if we already found this query via decorator parsing
                    if name not in found_names:
                        queries.append(
                            ParsedQuery(
                                name=name,
                                sql=sql,
                                returns=match.group(2),
                                param_names=param_names if param_names else None,
                                line_number=node.lineno,
                                source_file=source_file,
                            )
                        )
                        found_names.add(name)

        # Look for @query decorator on functions that return SQL
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if _is_query_decorator(decorator) and isinstance(decorator, ast.Call):
                    query = _parse_query_decorator(decorator, node, source_file)
                    if query and query.name not in found_names:
                        queries.append(query)
                        found_names.add(query.name)

    return queries


def _strip_query_decorators(content: str) -> str:
    """Remove @query(...) decorators from content to make it valid Python."""
    # Pattern matches @query(...) on its own line
    pattern = re.compile(r"^\s*@query\s*\([^)]*\)\s*\n", re.MULTILINE)
    return pattern.sub("", content)


def _is_query_decorator(decorator: ast.expr) -> bool:
    """Check if a decorator is @query(...)."""
    if isinstance(decorator, ast.Call):
        if isinstance(decorator.func, ast.Name) and decorator.func.id == "query":
            return True
    return False


def _parse_query_decorator(
    decorator: ast.Call, node: ast.FunctionDef, source_file: str | None
) -> ParsedQuery | None:
    """Parse a @query decorator on a function."""
    name: str | None = None
    returns: str | None = None
    param_names: list[str] = []

    for keyword in decorator.keywords:
        if keyword.arg == "name" and isinstance(keyword.value, ast.Constant):
            if isinstance(keyword.value.value, str):
                name = keyword.value.value
        elif keyword.arg == "returns" and isinstance(keyword.value, ast.Constant):
            if isinstance(keyword.value.value, str):
                returns = keyword.value.value
        elif keyword.arg == "param" and isinstance(keyword.value, ast.Constant):
            if isinstance(keyword.value.value, str):
                param_names.append(keyword.value.value)
        elif keyword.arg == "params" and isinstance(keyword.value, ast.List):
            for elt in keyword.value.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    param_names.append(elt.value)

    if not name:
        return None

    # Extract SQL from function body (look for return statement with string)
    sql: str | None = None
    for stmt in node.body:
        if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Constant):
            if isinstance(stmt.value.value, str):
                sql = stmt.value.value.strip()
                break
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            if isinstance(stmt.value.value, str):
                sql = stmt.value.value.strip()
                break

    if not sql:
        return None

    return ParsedQuery(
        name=name,
        sql=sql,
        returns=returns,
        param_names=param_names if param_names else None,
        line_number=node.lineno,
        source_file=source_file,
    )


def _parse_decorated_variables(
    content: str, source_file: str | None
) -> list[ParsedQuery]:
    """
    Parse @query decorated variable assignments.

    Format:
        @query(name="GetUser", param="userId")
        GET_USER = '''SELECT * FROM users WHERE id = $1'''
    """
    queries: list[ParsedQuery] = []

    # Pattern for @query decorator
    decorator_pattern = re.compile(
        r"@query\s*\(\s*"
        r'name\s*=\s*["\'](\w+)["\']'  # name="QueryName"
        r"(?:\s*,\s*returns\s*=\s*[\"'](\w+)[\"'])?"  # optional returns="one"
        r"((?:\s*,\s*param\s*=\s*[\"']\w+[\"'])*)"  # optional param="name" (repeatable)
        r"(?:\s*,\s*params\s*=\s*\[(.*?)\])?"  # optional params=["a", "b"]
        r"\s*\)",
        re.IGNORECASE | re.DOTALL,
    )

    param_pattern = re.compile(r'param\s*=\s*["\'](\w+)["\']', re.IGNORECASE)
    params_list_pattern = re.compile(r'["\'](\w+)["\']')

    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        match = decorator_pattern.search(line)

        if match:
            name = match.group(1)
            returns = match.group(2)

            # Extract param names
            param_names: list[str] = []
            if match.group(3):
                param_names.extend(param_pattern.findall(match.group(3)))
            if match.group(4):
                param_names.extend(params_list_pattern.findall(match.group(4)))

            # Look for the variable assignment on the next non-empty line
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1

            if j < len(lines):
                # Try to extract the SQL string
                sql = _extract_sql_from_assignment(lines, j)
                if sql:
                    queries.append(
                        ParsedQuery(
                            name=name,
                            sql=sql.strip(),
                            returns=returns,
                            param_names=param_names if param_names else None,
                            line_number=i + 1,
                            source_file=source_file,
                        )
                    )
                    i = j
        i += 1

    return queries


def _extract_sql_from_assignment(lines: list[str], start_line: int) -> str | None:
    """Extract a SQL string from a variable assignment."""
    line = lines[start_line]

    # Check for triple-quoted string
    triple_match = re.search(r'=\s*(?:f)?(?:"""|\'\'\')(.*)', line, re.DOTALL)
    if triple_match:
        # Find the closing triple quote
        quote_char = '"""' if '"""' in line else "'''"
        content_parts = [triple_match.group(1)]

        # Check if it closes on the same line
        remaining = triple_match.group(1)
        if quote_char in remaining:
            return remaining.split(quote_char)[0]

        # Multi-line string
        for i in range(start_line + 1, len(lines)):
            if quote_char in lines[i]:
                content_parts.append(lines[i].split(quote_char)[0])
                break
            content_parts.append(lines[i])

        return "\n".join(content_parts)

    # Check for single-quoted string
    single_match = re.search(r'=\s*(?:f)?["\'](.+)["\']', line)
    if single_match:
        return single_match.group(1)

    return None


def parse_sql_directory(path: Path) -> list[ParsedQuery]:
    """Parse all .sql and .py files in a directory recursively."""
    queries: list[ParsedQuery] = []

    # Parse .sql files
    for sql_file in sorted(path.glob("**/*.sql")):
        content = sql_file.read_text()
        file_queries = parse_sql_file(content, source_file=str(sql_file))
        queries.extend(file_queries)

    # Parse .py files
    for py_file in sorted(path.glob("**/*.py")):
        content = py_file.read_text()
        file_queries = parse_python_file(content, source_file=str(py_file))
        queries.extend(file_queries)

    return queries
