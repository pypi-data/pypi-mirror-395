"""Tests for parsing SQL queries from Python files."""


from typedpg.parser import parse_python_file


class TestDecoratorStyle:
    """Tests for @query decorator parsing."""

    def test_simple_decorator(self) -> None:
        """Parse a simple @query decorated variable."""
        content = '''
from typedpg import query

@query(name="GetUserById", param="userId")
GET_USER = """SELECT id, name, email FROM users WHERE id = $1"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 1
        assert queries[0].name == "GetUserById"
        assert queries[0].param_names == ["userId"]
        assert "SELECT id, name, email FROM users WHERE id = $1" in queries[0].sql

    def test_decorator_with_returns(self) -> None:
        """Parse @query with returns annotation."""
        content = '''
@query(name="CreateUser", returns="one", params=["name", "email"])
CREATE_USER = """
INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *
"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 1
        assert queries[0].name == "CreateUser"
        assert queries[0].returns == "one"
        assert queries[0].param_names == ["name", "email"]

    def test_decorator_multiple_params(self) -> None:
        """Parse @query with multiple param= arguments."""
        content = '''
@query(name="UpdateUser", param="name", param="userId")
UPDATE_USER = """UPDATE users SET name = $1 WHERE id = $2"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 1
        assert queries[0].name == "UpdateUser"
        assert queries[0].param_names == ["name", "userId"]

    def test_decorator_single_quotes(self) -> None:
        """Parse @query with single-quoted SQL."""
        content = """
@query(name="DeleteUser", param="userId")
DELETE_USER = '''DELETE FROM users WHERE id = $1'''
"""
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 1
        assert queries[0].name == "DeleteUser"
        assert "DELETE FROM users WHERE id = $1" in queries[0].sql

    def test_multiple_queries(self) -> None:
        """Parse multiple @query decorated variables."""
        content = '''
@query(name="GetUser", param="id")
GET_USER = """SELECT * FROM users WHERE id = $1"""

@query(name="ListUsers")
LIST_USERS = """SELECT * FROM users"""

@query(name="CountUsers", returns="one")
COUNT_USERS = """SELECT COUNT(*) as count FROM users"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 3
        assert queries[0].name == "GetUser"
        assert queries[1].name == "ListUsers"
        assert queries[2].name == "CountUsers"


class TestInlineAnnotationStyle:
    """Tests for inline /* @name ... */ annotation parsing."""

    def test_inline_annotation(self) -> None:
        """Parse inline annotation in SQL string."""
        content = '''
GET_USER = """
/* @name GetUserById @param userId */
SELECT id, name, email FROM users WHERE id = $1
"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 1
        assert queries[0].name == "GetUserById"
        assert queries[0].param_names == ["userId"]
        assert "SELECT id, name, email FROM users WHERE id = $1" in queries[0].sql

    def test_inline_with_returns(self) -> None:
        """Parse inline annotation with returns."""
        content = '''
CREATE_USER = """
/* @name CreateUser @returns one @param name @param email */
INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *
"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 1
        assert queries[0].name == "CreateUser"
        assert queries[0].returns == "one"
        assert queries[0].param_names == ["name", "email"]

    def test_multiple_inline_queries(self) -> None:
        """Parse multiple inline annotated queries."""
        content = '''
GET_USER = """
/* @name GetUser @param id */
SELECT * FROM users WHERE id = $1
"""

LIST_USERS = """
/* @name ListUsers */
SELECT * FROM users
"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 2
        assert queries[0].name == "GetUser"
        assert queries[1].name == "ListUsers"


class TestMixedStyles:
    """Tests for files with both decorator and inline styles."""

    def test_mixed_styles(self) -> None:
        """Parse file with both decorator and inline styles."""
        content = '''
from typedpg import query

@query(name="GetUser", param="id")
GET_USER = """SELECT * FROM users WHERE id = $1"""

LIST_USERS = """
/* @name ListUsers */
SELECT * FROM users
"""

@query(name="DeleteUser", param="id")
DELETE_USER = """DELETE FROM users WHERE id = $1"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 3
        names = [q.name for q in queries]
        assert "GetUser" in names
        assert "ListUsers" in names
        assert "DeleteUser" in names


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_file(self) -> None:
        """Parse empty file returns no queries."""
        queries = parse_python_file("", source_file="test.py")
        assert len(queries) == 0

    def test_no_queries(self) -> None:
        """Parse file with no queries returns empty list."""
        content = '''
def hello():
    return "world"

x = 42
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 0

    def test_syntax_error_returns_empty(self) -> None:
        """Parse file with syntax error returns empty list."""
        content = "def broken("
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 0

    def test_multiline_sql(self) -> None:
        """Parse multiline SQL query."""
        content = '''
@query(name="ComplexQuery", params=["status", "limit"])
COMPLEX_QUERY = """
SELECT
    u.id,
    u.name,
    u.email,
    COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = $1
GROUP BY u.id
ORDER BY order_count DESC
LIMIT $2
"""
'''
        queries = parse_python_file(content, source_file="test.py")
        assert len(queries) == 1
        assert queries[0].name == "ComplexQuery"
        assert "LEFT JOIN orders" in queries[0].sql
        assert "GROUP BY" in queries[0].sql

    def test_source_file_and_line_number(self) -> None:
        """Verify source file and line number are captured."""
        content = '''
# Line 1
# Line 2
@query(name="TestQuery")
TEST = """SELECT 1"""
'''
        queries = parse_python_file(content, source_file="my_queries.py")
        assert len(queries) == 1
        assert queries[0].source_file == "my_queries.py"
        assert queries[0].line_number > 0
