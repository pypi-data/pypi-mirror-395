SELECT
    c.column_name,
    CASE 
        WHEN c.data_type = 'USER-DEFINED' THEN c.udt_name
        ELSE c.data_type
    END as data_type,
    c.is_nullable,
    c.column_default
FROM information_schema.columns c
WHERE c.table_schema NOT IN ('information_schema', 'pg_catalog')
AND LOWER(c.table_name) = LOWER('{{table_name}}')
AND LOWER(c.table_schema) = LOWER('{{schema_name}}')
ORDER BY c.ordinal_position