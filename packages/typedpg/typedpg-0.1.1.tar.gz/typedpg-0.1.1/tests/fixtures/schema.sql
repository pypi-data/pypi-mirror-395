-- Test schema for typedpg snapshot tests
-- This schema is used by testcontainers to set up a clean database for each test run

-- Users table with various column types
CREATE TABLE test_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    age INTEGER,
    is_active BOOLEAN DEFAULT true,
    role VARCHAR(50) DEFAULT 'user',
    metadata JSONB,
    tags TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Categories with self-referential foreign key (for recursive CTE tests)
CREATE TABLE test_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    parent_id INTEGER REFERENCES test_categories(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Products with foreign key to categories
CREATE TABLE test_products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    category_id INTEGER REFERENCES test_categories(id),
    stock_count INTEGER DEFAULT 0,
    is_available BOOLEAN DEFAULT true,
    attributes JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Orders with foreign key to users
CREATE TABLE test_orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES test_users(id),
    status VARCHAR(50) DEFAULT 'pending',
    total_amount NUMERIC(12, 2),
    shipping_address JSONB,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Order items (junction table with additional columns)
CREATE TABLE test_order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES test_orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES test_products(id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Posts for blog-like queries
CREATE TABLE test_posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES test_users(id),
    title VARCHAR(255) NOT NULL,
    content TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    view_count INTEGER DEFAULT 0,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Comments with self-referential foreign key (for nested comments)
CREATE TABLE test_comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES test_posts(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES test_users(id),
    parent_id INTEGER REFERENCES test_comments(id),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tags for many-to-many relationship
CREATE TABLE test_tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Junction table for posts and tags
CREATE TABLE test_post_tags (
    post_id INTEGER NOT NULL REFERENCES test_posts(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES test_tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- Audit log for CTE with INSERT tests
CREATE TABLE test_audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    performed_by INTEGER REFERENCES test_users(id),
    performed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for common query patterns
CREATE INDEX idx_test_users_email ON test_users(email);
CREATE INDEX idx_test_users_is_active ON test_users(is_active);
CREATE INDEX idx_test_users_role ON test_users(role);
CREATE INDEX idx_test_orders_user_id ON test_orders(user_id);
CREATE INDEX idx_test_orders_status ON test_orders(status);
CREATE INDEX idx_test_order_items_order_id ON test_order_items(order_id);
CREATE INDEX idx_test_posts_author_id ON test_posts(author_id);
CREATE INDEX idx_test_posts_status ON test_posts(status);
CREATE INDEX idx_test_comments_post_id ON test_comments(post_id);
