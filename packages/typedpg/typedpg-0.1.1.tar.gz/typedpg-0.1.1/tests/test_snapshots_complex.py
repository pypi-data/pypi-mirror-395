"""
Snapshot tests for complex query patterns.
"""

import pytest
from syrupy.assertion import SnapshotAssertion

from typedpg.generators.dataclass_gen import generate_module
from typedpg.inference import TypeInferrer


class TestInsertOnConflict:
    """Test INSERT ... ON CONFLICT (upsert) patterns."""

    @pytest.mark.asyncio
    async def test_insert_on_conflict_do_nothing(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT ON CONFLICT DO NOTHING."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_users (email, name)
            VALUES ($1, $2)
            ON CONFLICT (email) DO NOTHING
            """,
            "CreateUserIfNotExists",
            param_names=["email", "name"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_insert_on_conflict_do_nothing_returning(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT ON CONFLICT DO NOTHING with RETURNING."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_users (email, name)
            VALUES ($1, $2)
            ON CONFLICT (email) DO NOTHING
            RETURNING id, email, name
            """,
            "CreateUserIfNotExistsReturning",
            param_names=["email", "name"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_insert_on_conflict_do_update(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT ON CONFLICT DO UPDATE (upsert)."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_users (email, name, role)
            VALUES ($1, $2, $3)
            ON CONFLICT (email) DO UPDATE
            SET name = EXCLUDED.name, role = EXCLUDED.role, updated_at = NOW()
            RETURNING id, email, name, role, updated_at
            """,
            "UpsertUser",
            param_names=["email", "name", "role"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_insert_on_conflict_do_update_partial(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT ON CONFLICT DO UPDATE with WHERE clause."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_products (name, price, category_id)
            VALUES ($1, $2, $3)
            ON CONFLICT (name) DO UPDATE
            SET price = EXCLUDED.price, updated_at = NOW()
            WHERE test_products.price < EXCLUDED.price
            RETURNING id, name, price, updated_at
            """,
            "UpsertProductIfPriceHigher",
            param_names=["name", "price", "categoryId"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestCTEs:
    """Test Common Table Expressions (WITH clauses)."""

    @pytest.mark.asyncio
    async def test_simple_cte(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """Simple CTE for readability."""
        spec = await inferrer.analyze_query(
            """
            WITH active_users AS (
                SELECT id, email, name
                FROM test_users
                WHERE is_active = true
            )
            SELECT * FROM active_users WHERE email LIKE $1
            """,
            "GetActiveUsersByEmailPattern",
            param_names=["emailPattern"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_multiple_ctes(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """Multiple CTEs."""
        spec = await inferrer.analyze_query(
            """
            WITH
            user_orders AS (
                SELECT user_id, COUNT(*) as order_count, SUM(total_amount) as total_spent
                FROM test_orders
                GROUP BY user_id
            ),
            high_value_users AS (
                SELECT user_id, total_spent
                FROM user_orders
                WHERE total_spent > $1
            )
            SELECT u.id, u.email, u.name, hvu.total_spent
            FROM test_users u
            JOIN high_value_users hvu ON u.id = hvu.user_id
            ORDER BY hvu.total_spent DESC
            """,
            "GetHighValueUsers",
            param_names=["minSpent"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_recursive_cte(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """Recursive CTE for hierarchical data."""
        spec = await inferrer.analyze_query(
            """
            WITH RECURSIVE category_tree AS (
                SELECT id, name, parent_id, 1 as depth
                FROM test_categories
                WHERE id = $1

                UNION ALL

                SELECT c.id, c.name, c.parent_id, ct.depth + 1
                FROM test_categories c
                JOIN category_tree ct ON c.parent_id = ct.id
            )
            SELECT id, name, parent_id, depth
            FROM category_tree
            ORDER BY depth
            """,
            "GetCategoryTree",
            param_names=["rootCategoryId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_cte_with_insert(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """CTE with INSERT (data-modifying CTE)."""
        spec = await inferrer.analyze_query(
            """
            WITH new_user AS (
                INSERT INTO test_users (email, name)
                VALUES ($1, $2)
                RETURNING id, email, name
            )
            INSERT INTO test_audit_log (table_name, record_id, action, new_data, performed_by)
            SELECT 'test_users', id, 'INSERT', to_jsonb(new_user), $3
            FROM new_user
            RETURNING id
            """,
            "CreateUserWithAudit",
            param_names=["email", "name", "performedBy"],
        )
        spec.returns = "one"
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestJoins:
    """Test JOIN query patterns."""

    @pytest.mark.asyncio
    async def test_inner_join(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """INNER JOIN between tables."""
        spec = await inferrer.analyze_query(
            """
            SELECT o.id, o.status, o.total_amount, u.email, u.name
            FROM test_orders o
            INNER JOIN test_users u ON o.user_id = u.id
            WHERE o.status = $1
            """,
            "GetOrdersWithUserByStatus",
            param_names=["status"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_left_join(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """LEFT JOIN with nullable columns."""
        spec = await inferrer.analyze_query(
            """
            SELECT u.id, u.email, u.name, COUNT(o.id) as order_count
            FROM test_users u
            LEFT JOIN test_orders o ON u.id = o.user_id
            WHERE u.is_active = $1
            GROUP BY u.id, u.email, u.name
            """,
            "GetUsersWithOrderCount",
            param_names=["isActive"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_multiple_joins(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Multiple JOINs across tables."""
        spec = await inferrer.analyze_query(
            """
            SELECT
                o.id as order_id,
                o.status,
                u.email as user_email,
                p.name as product_name,
                oi.quantity,
                oi.unit_price
            FROM test_orders o
            JOIN test_users u ON o.user_id = u.id
            JOIN test_order_items oi ON o.id = oi.order_id
            JOIN test_products p ON oi.product_id = p.id
            WHERE o.id = $1
            """,
            "GetOrderDetails",
            param_names=["orderId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_self_join(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """Self JOIN for hierarchical data."""
        spec = await inferrer.analyze_query(
            """
            SELECT
                c.id,
                c.name,
                p.name as parent_name
            FROM test_categories c
            LEFT JOIN test_categories p ON c.parent_id = p.id
            WHERE c.id = $1
            """,
            "GetCategoryWithParent",
            param_names=["categoryId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestSubqueries:
    """Test subquery patterns."""

    @pytest.mark.asyncio
    async def test_subquery_in_where(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Subquery in WHERE clause."""
        spec = await inferrer.analyze_query(
            """
            SELECT id, email, name
            FROM test_users
            WHERE id IN (
                SELECT DISTINCT user_id
                FROM test_orders
                WHERE total_amount > $1
            )
            """,
            "GetUsersWithHighValueOrders",
            param_names=["minAmount"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_subquery_in_select(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Scalar subquery in SELECT."""
        spec = await inferrer.analyze_query(
            """
            SELECT
                u.id,
                u.email,
                u.name,
                (SELECT COUNT(*) FROM test_orders WHERE user_id = u.id) as cnt,
                (SELECT COALESCE(SUM(total_amount), 0) FROM test_orders WHERE user_id = u.id) as sum
            FROM test_users u
            WHERE u.id = $1
            """,
            "GetUserWithStats",
            param_names=["userId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_exists_subquery(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """EXISTS subquery."""
        spec = await inferrer.analyze_query(
            """
            SELECT id, email, name
            FROM test_users u
            WHERE EXISTS (
                SELECT 1 FROM test_orders o
                WHERE o.user_id = u.id AND o.status = $1
            )
            """,
            "GetUsersWithOrderStatus",
            param_names=["status"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_lateral_join(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """LATERAL subquery."""
        spec = await inferrer.analyze_query(
            """
            SELECT u.id, u.email, recent_orders.order_id, recent_orders.total_amount
            FROM test_users u
            CROSS JOIN LATERAL (
                SELECT o.id as order_id, o.total_amount
                FROM test_orders o
                WHERE o.user_id = u.id
                ORDER BY o.created_at DESC
                LIMIT $1
            ) recent_orders
            WHERE u.is_active = true
            """,
            "GetUsersWithRecentOrders",
            param_names=["orderLimit"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestAggregations:
    """Test aggregation and GROUP BY patterns."""

    @pytest.mark.asyncio
    async def test_group_by_with_aggregates(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """GROUP BY with multiple aggregates."""
        spec = await inferrer.analyze_query(
            """
            SELECT
                status,
                COUNT(*) as order_count,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_order_value,
                MIN(created_at) as first_order,
                MAX(created_at) as last_order
            FROM test_orders
            WHERE created_at >= $1
            GROUP BY status
            ORDER BY total_revenue DESC
            """,
            "GetOrderStatsByStatus",
            param_names=["sinceDate"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_having_clause(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """GROUP BY with HAVING clause."""
        spec = await inferrer.analyze_query(
            """
            SELECT
                user_id,
                COUNT(*) as order_count,
                SUM(total_amount) as total_spent
            FROM test_orders
            GROUP BY user_id
            HAVING COUNT(*) >= $1 AND SUM(total_amount) >= $2
            """,
            "GetFrequentHighValueCustomers",
            param_names=["minOrders", "minSpent"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_window_functions(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Window functions."""
        spec = await inferrer.analyze_query(
            """
            SELECT
                id,
                email,
                name,
                created_at,
                ROW_NUMBER() OVER (ORDER BY created_at) as signup_order,
                RANK() OVER (PARTITION BY role ORDER BY created_at) as role_rank
            FROM test_users
            WHERE is_active = $1
            """,
            "GetUsersWithRankings",
            param_names=["isActive"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestComplexUpdates:
    """Test complex UPDATE patterns."""

    @pytest.mark.asyncio
    async def test_update_from_subquery(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """UPDATE with FROM clause."""
        spec = await inferrer.analyze_query(
            """
            UPDATE test_orders o
            SET status = $1, updated_at = NOW()
            FROM test_users u
            WHERE o.user_id = u.id AND u.is_active = false
            RETURNING o.id, o.status, o.user_id
            """,
            "CancelOrdersForInactiveUsers",
            param_names=["newStatus"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_update_with_case(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """UPDATE with CASE expression."""
        spec = await inferrer.analyze_query(
            """
            UPDATE test_orders
            SET status = CASE
                WHEN total_amount >= $1 THEN 'priority'
                WHEN total_amount >= $2 THEN 'standard'
                ELSE 'economy'
            END,
            updated_at = NOW()
            WHERE status = 'pending'
            RETURNING id, status, total_amount
            """,
            "ClassifyPendingOrders",
            param_names=["priorityThreshold", "standardThreshold"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestComplexDeletes:
    """Test complex DELETE patterns."""

    @pytest.mark.asyncio
    async def test_delete_with_subquery(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """DELETE with subquery condition."""
        spec = await inferrer.analyze_query(
            """
            DELETE FROM test_orders
            WHERE user_id IN (
                SELECT id FROM test_users WHERE is_active = false
            )
            AND created_at < $1
            """,
            "DeleteOldOrdersForInactiveUsers",
            param_names=["beforeDate"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_delete_using(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """DELETE with USING clause."""
        spec = await inferrer.analyze_query(
            """
            DELETE FROM test_order_items oi
            USING test_orders o
            WHERE oi.order_id = o.id AND o.status = $1
            RETURNING oi.id, oi.order_id, oi.product_id
            """,
            "DeleteItemsFromOrdersByStatus",
            param_names=["status"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestBatchOperations:
    """Test batch/bulk operation patterns."""

    @pytest.mark.asyncio
    async def test_insert_multiple_rows(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """INSERT with unnest for batch insert."""
        spec = await inferrer.analyze_query(
            """
            INSERT INTO test_tags (name)
            SELECT unnest($1::text[])
            ON CONFLICT (name) DO NOTHING
            RETURNING id, name
            """,
            "CreateTagsBatch",
            param_names=["tagNames"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_update_multiple_with_values(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Batch UPDATE using VALUES."""
        spec = await inferrer.analyze_query(
            """
            UPDATE test_products p
            SET stock_count = v.new_stock, updated_at = NOW()
            FROM (
                SELECT unnest($1::int[]) as id, unnest($2::int[]) as new_stock
            ) v
            WHERE p.id = v.id
            RETURNING p.id, p.name, p.stock_count
            """,
            "UpdateProductStockBatch",
            param_names=["productIds", "newStockCounts"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestJsonOperations:
    """Test JSONB query patterns."""

    @pytest.mark.asyncio
    async def test_jsonb_field_access(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Access JSONB fields."""
        spec = await inferrer.analyze_query(
            """
            SELECT
                id,
                email,
                metadata->>'theme' as theme,
                metadata->>'language' as language,
                (metadata->>'notifications')::boolean as notifications_enabled
            FROM test_users
            WHERE metadata->>'theme' = $1
            """,
            "GetUsersByTheme",
            param_names=["theme"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_jsonb_containment(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """JSONB containment query."""
        spec = await inferrer.analyze_query(
            """
            SELECT id, email, name, metadata
            FROM test_users
            WHERE metadata @> $1
            """,
            "GetUsersByMetadataMatch",
            param_names=["metadataFilter"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_jsonb_array_elements(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Query JSONB array elements."""
        spec = await inferrer.analyze_query(
            """
            SELECT
                o.id,
                o.status,
                addr->>'street' as street,
                addr->>'city' as city,
                addr->>'zip' as zip_code
            FROM test_orders o,
            jsonb_array_elements(o.shipping_address->'addresses') as addr
            WHERE o.id = $1
            """,
            "GetOrderShippingAddresses",
            param_names=["orderId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot


class TestArrayOperations:
    """Test array query patterns."""

    @pytest.mark.asyncio
    async def test_array_contains(
        self, inferrer: TypeInferrer, snapshot: SnapshotAssertion
    ) -> None:
        """Array containment query."""
        spec = await inferrer.analyze_query(
            """
            SELECT id, email, name, tags
            FROM test_users
            WHERE tags @> $1
            """,
            "GetUsersByTags",
            param_names=["requiredTags"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_array_overlap(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """Array overlap query."""
        spec = await inferrer.analyze_query(
            """
            SELECT id, email, name, tags
            FROM test_users
            WHERE tags && $1
            """,
            "GetUsersByAnyTag",
            param_names=["anyOfTags"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot

    @pytest.mark.asyncio
    async def test_array_unnest(self, inferrer: TypeInferrer, snapshot: SnapshotAssertion) -> None:
        """Unnest array to rows."""
        spec = await inferrer.analyze_query(
            """
            SELECT u.id, u.email, unnest(u.tags) as tag
            FROM test_users u
            WHERE u.id = $1
            """,
            "GetUserTagsExpanded",
            param_names=["userId"],
        )
        code = generate_module([spec], driver="asyncpg")
        assert code == snapshot
