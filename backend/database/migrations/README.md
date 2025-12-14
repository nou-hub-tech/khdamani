# Database Migrations

This directory contains Alembic migration files for database schema changes.

## Setup

1. Initialize Alembic (if not already done):
```bash
cd backend
alembic init alembic
```

2. Configure `alembic/env.py` to use your database URL and import your models.

3. Generate initial migration from the schema:
```bash
alembic revision --autogenerate -m "Initial schema"
```

4. Review the generated migration file in `alembic/versions/`

5. Apply the migration:
```bash
alembic upgrade head
```

## Using the SQL Schema Directly

Alternatively, you can use the SQL schema file directly:

```bash
psql -U postgres -d khadamni -f database/schema.sql
```

This approach is useful for:
- Initial setup
- Development environments
- Testing the schema

## Migration Workflow

1. **Make changes to models** in `app/models/`
2. **Generate migration**: `alembic revision --autogenerate -m "description"`
3. **Review migration**: Check the generated SQL in the migration file
4. **Apply migration**: `alembic upgrade head`
5. **Rollback if needed**: `alembic downgrade -1`

## Important Notes

- Always review auto-generated migrations before applying
- Test migrations on a development database first
- Keep migrations small and focused
- Never edit existing migrations that have been applied to production
- Use `alembic downgrade` carefully in production

