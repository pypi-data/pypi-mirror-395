"""
Snapshot tests for basic CRUD operations.
"""

import pytest
from syrupy.assertion import SnapshotAssertion

from typedpg.generators.dataclass_gen import generate_module
from typedpg.generators.pydantic_gen import generate_module as generate_pydantic_module
from typedpg.inference import TypeInferrer


class TestBasicSelect:
    """Test basic SELECT query generation."""

    @pytest.mark.asyncio
    async def test_select_all_columns(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """SELECT * from a table."""
        spec = await inferrer.analyze_query(
            "SELECT * FROM test_users",
            "GetAllUsers",
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_select_specific_columns(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """SELECT specific columns."""
        spec = await inferrer.analyze_query(
            "SELECT id, email, name, created_at FROM test_users",
            "GetUserBasicInfo",
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_select_with_where_single_param(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """SELECT with single WHERE parameter."""
        spec = await inferrer.analyze_query(
            "SELECT id, email, name FROM test_users WHERE id = $1",
            "GetUserById",
            param_names=["userId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_select_with_multiple_params(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """SELECT with multiple WHERE parameters."""
        spec = await inferrer.analyze_query(
            """
            SELECT id, email, name, role
            FROM test_users
            WHERE is_active = $1 AND role = $2
            """,
            "GetUsersByStatusAndRole",
            param_names=["isActive", "role"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_select_with_limit(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """SELECT with LIMIT 1 should return 'one'."""
        spec = await inferrer.analyze_query(
            "SELECT id, email FROM test_users ORDER BY created_at DESC LIMIT 1",
            "GetLatestUser",
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot
        assert spec.returns == "one"

    @pytest.mark.asyncio
    async def test_select_with_order_and_pagination(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """SELECT with ORDER BY, LIMIT, and OFFSET."""
        spec = await inferrer.analyze_query(
            """
            SELECT id, email, name, created_at
            FROM test_users
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
            """,
            "GetUsersPaginated",
            param_names=["limit", "offset"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_select_with_like(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """SELECT with LIKE pattern matching."""
        spec = await inferrer.analyze_query(
            "SELECT id, email, name FROM test_users WHERE email LIKE $1",
            "SearchUsersByEmail",
            param_names=["emailPattern"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_select_with_in_clause(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """SELECT with IN clause using array parameter."""
        spec = await inferrer.analyze_query(
            "SELECT id, email, name FROM test_users WHERE id = ANY($1)",
            "GetUsersByIds",
            param_names=["userIds"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_select_count(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """SELECT COUNT aggregate."""
        spec = await inferrer.analyze_query(
            "SELECT COUNT(*) as total FROM test_users WHERE is_active = $1",
            "CountActiveUsers",
            param_names=["isActive"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestBasicInsert:
    """Test basic INSERT query generation."""

    @pytest.mark.asyncio
    async def test_insert_simple(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """Simple INSERT without RETURNING."""
        spec = await inferrer.analyze_query(
            "INSERT INTO test_users (email, name) VALUES ($1, $2)",
            "CreateUserSimple",
            param_names=["email", "name"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot
        assert spec.returns == "affected"

    @pytest.mark.asyncio
    async def test_insert_returning_id(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT with RETURNING id."""
        spec = await inferrer.analyze_query(
            "INSERT INTO test_users (email, name) VALUES ($1, $2) RETURNING id",
            "CreateUserReturningId",
            param_names=["email", "name"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_insert_returning_all(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT with RETURNING *."""
        spec = await inferrer.analyze_query(
            "INSERT INTO test_users (email, name, role) VALUES ($1, $2, $3) RETURNING *",
            "CreateUserFull",
            param_names=["email", "name", "role"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_insert_with_defaults(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT relying on DEFAULT values."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_users (email, name)
            VALUES ($1, $2)
            RETURNING id, email, name, is_active, role, created_at
            """,
            "CreateUserWithDefaults",
            param_names=["email", "name"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_insert_with_jsonb(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT with JSONB column."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_users (email, name, metadata)
            VALUES ($1, $2, $3)
            RETURNING id, email, metadata
            """,
            "CreateUserWithMetadata",
            param_names=["email", "name", "metadata"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_insert_with_array(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT with array column."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_users (email, name, tags)
            VALUES ($1, $2, $3)
            RETURNING id, email, tags
            """,
            "CreateUserWithTags",
            param_names=["email", "name", "tags"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestBasicUpdate:
    """Test basic UPDATE query generation."""

    @pytest.mark.asyncio
    async def test_update_single_column(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """UPDATE single column."""
        spec = await inferrer.analyze_query(
            "UPDATE test_users SET name = $1 WHERE id = $2",
            "UpdateUserName",
            param_names=["name", "userId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot
        assert spec.returns == "affected"

    @pytest.mark.asyncio
    async def test_update_multiple_columns(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """UPDATE multiple columns."""
        spec = await inferrer.analyze_query(
            """
            UPDATE test_users
            SET name = $1, email = $2, role = $3, updated_at = NOW()
            WHERE id = $4
            """,
            "UpdateUserDetails",
            param_names=["name", "email", "role", "userId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_update_returning(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """UPDATE with RETURNING."""
        spec = await inferrer.analyze_query(
            """
            UPDATE test_users
            SET name = $1, updated_at = NOW()
            WHERE id = $2
            RETURNING id, name, email, updated_at
            """,
            "UpdateUserNameReturning",
            param_names=["name", "userId"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_update_with_condition(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """UPDATE with complex WHERE condition."""
        spec = await inferrer.analyze_query(
            """
            UPDATE test_users
            SET is_active = $1
            WHERE role = $2 AND created_at < $3
            """,
            "DeactivateOldUsersByRole",
            param_names=["isActive", "role", "beforeDate"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_update_jsonb(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """UPDATE JSONB column."""
        spec = await inferrer.analyze_query(
            """
            UPDATE test_users
            SET metadata = metadata || $1
            WHERE id = $2
            RETURNING id, metadata
            """,
            "UpdateUserMetadata",
            param_names=["newMetadata", "userId"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestBasicDelete:
    """Test basic DELETE query generation."""

    @pytest.mark.asyncio
    async def test_delete_by_id(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """DELETE by primary key."""
        spec = await inferrer.analyze_query(
            "DELETE FROM test_users WHERE id = $1",
            "DeleteUserById",
            param_names=["userId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot
        assert spec.returns == "affected"

    @pytest.mark.asyncio
    async def test_delete_with_condition(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """DELETE with complex condition."""
        spec = await inferrer.analyze_query(
            "DELETE FROM test_users WHERE is_active = false AND deleted_at < $1",
            "DeleteInactiveUsersBefore",
            param_names=["beforeDate"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_delete_returning(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """DELETE with RETURNING."""
        spec = await inferrer.analyze_query(
            "DELETE FROM test_users WHERE id = $1 RETURNING id, email, name",
            "DeleteUserReturning",
            param_names=["userId"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_soft_delete(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """Soft delete (UPDATE deleted_at)."""
        spec = await inferrer.analyze_query(
            """
            UPDATE test_users
            SET deleted_at = NOW(), is_active = false
            WHERE id = $1
            RETURNING id, email, deleted_at
            """,
            "SoftDeleteUser",
            param_names=["userId"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestPydanticOutput:
    """Test Pydantic model generation."""

    @pytest.mark.asyncio
    async def test_pydantic_select(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Generate Pydantic models for SELECT."""
        spec = await inferrer.analyze_query(
            "SELECT id, email, name, metadata, created_at FROM test_users WHERE id = $1",
            "GetUserById",
            param_names=["userId"],
        )
        code = generate_pydantic_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_pydantic_insert_returning(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Generate Pydantic models for INSERT RETURNING."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_users (email, name, metadata)
            VALUES ($1, $2, $3)
            RETURNING *
            """,
            "CreateUser",
            param_names=["email", "name", "metadata"],
        )
        spec.returns = "one"
        code = generate_pydantic_module([spec], driver="asyncpg")
        assert code == snapshot


class TestPsycopgDriver:
    """Test psycopg driver code generation."""

    @pytest.mark.asyncio
    async def test_psycopg_select(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Generate psycopg code for SELECT."""
        spec = await inferrer.analyze_query(
            "SELECT id, email, name FROM test_users WHERE is_active = $1",
            "GetActiveUsers",
            param_names=["isActive"],
        )
        code = generate_module([spec], driver="psycopg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_psycopg_insert_returning(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Generate psycopg code for INSERT RETURNING."""
        spec = await inferrer.analyze_query(
            "INSERT INTO test_users (email, name) VALUES ($1, $2) RETURNING id, email",
            "CreateUser",
            param_names=["email", "name"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="psycopg")
        assert code == snapshot
