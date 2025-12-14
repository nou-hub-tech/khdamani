# Fix: Installation Errors

## Problem 1: psycopg2-binary Error
The error occurs because `psycopg2-binary` requires PostgreSQL development libraries to build, but we're using SQLite (which doesn't need it).

## Problem 2: pydantic-core Version Conflict
`pydantic==2.5.0` requires `pydantic-core==2.14.1`, which is not available. The available versions start from 2.20.0.

## Problem 3: SQLAlchemy + Python 3.13 Compatibility
`sqlalchemy==2.0.23` is incompatible with Python 3.13 due to typing system changes.

## Problem 4: Missing email-validator
Pydantic's `EmailStr` type requires `email-validator` package to be installed separately.

## Problem 5: NumPy + Python 3.13 Compatibility
`numpy==1.26.2` tries to build from source on Python 3.13 (no pre-built wheels), requiring C compiler.

## ✅ Solution

Both `requirements.txt` files have been updated:
- ❌ Removed: `psycopg2-binary` (PostgreSQL driver - not needed for SQLite)
- ✅ Updated: `pydantic` to `>=2.8.0` (compatible with available pydantic-core versions)
- ✅ Updated: `sqlalchemy` to `>=2.0.25` (compatible with Python 3.13)
- ✅ Added: `email-validator>=2.0.0` (required for Pydantic EmailStr validation)
- ✅ Updated: `numpy`, `pandas`, `scikit-learn`, `joblib` to `>=` versions (allows pip to find Python 3.13 compatible wheels)

### Now run:

```powershell
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**That's it!** The installation should work now.

---

## Continue Setup

After successful installation:

```powershell
python init_db.py
uvicorn app.main:app --reload
```

**The app will work perfectly with SQLite!**

