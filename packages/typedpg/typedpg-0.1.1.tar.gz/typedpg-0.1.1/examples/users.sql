-- Example SQL queries for typedpg

/* @name GetUserById */
SELECT id, name, email, created_at
FROM users
WHERE id = $1;

/* @name ListActiveUsers */
SELECT id, name, email
FROM users
WHERE is_active = true
ORDER BY created_at DESC;

/* @name CreateUser @returns one @param name @param email */
INSERT INTO users (name, email)
VALUES ($1, $2)
RETURNING id, name, email, created_at;

/* @name UpdateUserEmail @param userId @param newEmail */
UPDATE users
SET email = $2
WHERE id = $1;

/* @name DeleteUser @param userId */
DELETE FROM users WHERE id = $1;

/* @name SearchUsers @param searchTerm */
SELECT id, name, email
FROM users
WHERE name ILIKE '%' || $1 || '%'
   OR email ILIKE '%' || $1 || '%'
ORDER BY name;

/* @name GetUserWithTags @returns one @param userId */
SELECT u.id, u.name, u.email, u.tags, u.metadata
FROM users u
WHERE u.id = $1;

/* @name CountActiveUsers @returns one */
SELECT COUNT(*) as count
FROM users
WHERE is_active = true;
