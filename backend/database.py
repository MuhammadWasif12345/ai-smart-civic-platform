import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------------------------------------
# DATABASE SETUP
# This file manages our connection to the database. It is designed to work with
# a simple local SQLite file during development, and a powerful Postgres database
# when deployed to production (like on Render), seamlessly switching between them.
# --------------------------------------------------------------------------------

# 1. READ THE CONNECTION STRING FROM ENVIRONMENT VARIABLES
# We check if a DATABASE_URL was provided by the hosting environment (like Render).
# The os.getenv function looks for this variable.
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. DETERMINE WHICH DATABASE TO USE
if DATABASE_URL:
    # If the URL exists, we are likely in production (e.g., Render Postgres).
    # Some older Postgres URLs start with "postgres://", but SQLAlchemy requires
    # "postgresql://". This quick fix ensures compatibility.
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # We create the database engine using the production URL.
    # The engine is the core interface to the database.
    engine = create_engine(DATABASE_URL)
else:
    # If no URL was found, we default to local development mode using SQLite.
    # Vercel's filesystem is read-only, except for the /tmp directory.
    if os.getenv("VERCEL"):
        SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/civic_services.db"
    else:
        SQLALCHEMY_DATABASE_URL = "sqlite:///./civic_services.db"
    
    # We create the SQLite engine.
    # 'check_same_thread': False is a specific requirement for SQLite in FastAPI
    # to allow multiple web requests (threads) to interact with the database safely.
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

# 3. CREATE THE SESSION MAKER
# A "Session" is a temporary workspace for database operations (like adding or querying data).
# We configure this factory to create sessions bound to our engine.
# autocommit=False and autoflush=False ensure we have manual control over when data is saved.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. DEFINE THE BASE MODEL CLASS
# Every database table we define in models.py will inherit from this Base class.
# It acts as a catalog, keeping track of all our tables so SQLAlchemy can create them.
Base = declarative_base()

# 5. DEPENDENCY INJECTION FUNCTION
# This function is used by FastAPI routes to get a database connection.
# It ensures that every web request gets its own separate database session,
# and more importantly, it guarantees the session is closed when the request is done.
def get_db():
    # Create a new session
    db = SessionLocal()
    try:
        # Give the session to the route that requested it (using Python's 'yield')
        yield db
    finally:
        # Always close the connection, even if an error occurred in the route
        db.close()
