"""
Query decorator for marking SQL queries in Python files.

Usage:
    from typedpg import query

    @query(name="GetUserById", param="userId")
    GET_USER = '''
    SELECT id, name, email FROM users WHERE id = $1
    '''

    @query(name="CreateUser", returns="one", params=["name", "email"])
    CREATE_USER = '''
    INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *
    '''
"""

from typing import Any


def query(
    name: str,
    returns: str | None = None,
    param: str | None = None,
    params: list[str] | None = None,
) -> Any:
    """
    Decorator to mark a variable as a SQL query for typedpg.

    This decorator is a no-op at runtime - it simply returns the decorated value.
    It serves as a marker for the typedpg CLI to extract query metadata.

    Args:
        name: The name of the query (used for generated function and class names)
        returns: Return type hint - "one", "many", "exec", or "affected"
        param: Single parameter name (use multiple @query decorators or params= for multiple)
        params: List of parameter names

    Example:
        @query(name="GetUserById", param="userId")
        GET_USER_BY_ID = "SELECT * FROM users WHERE id = $1"

        @query(name="CreateUser", returns="one", params=["name", "email"])
        CREATE_USER = "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *"
    """

    def decorator(value: Any) -> Any:
        # No-op at runtime - just return the value unchanged
        return value

    return decorator
