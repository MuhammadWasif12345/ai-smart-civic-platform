from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from contextlib import asynccontextmanager

from .database import engine, Base, SessionLocal
from .models import User
from .services.auth_service import AuthService
from .routers import complaints, admin, analytics, auth, chat

# Set up logging so we can see what the server is doing in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------
# FASTAPI APPLICATION ENTRY POINT (main.py)
# This is where the server starts. It wires together the database, the routers,
# the frontend files, and the global error handlers.
# --------------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function runs exactly once when the server starts up, before accepting 
    any web requests. We use it to ensure our database is ready.
    """
    logger.info("Starting up AI Smart Civic Services Backend...")
    
    # 1. Create the database tables if they don't exist yet
    # (Based on the models defined in models.py)
    Base.metadata.create_all(bind=engine)
    
    # 2. Check if DB is seeded
    db = SessionLocal()
    try:
        # Check if any users exist
        if not db.query(User).first():
            logger.info("Database is empty. Running seeder...")
            from .seed_data import seed_db
            try:
                seed_db()
            except Exception as e:
                logger.error(f"Failed to seed db: {e}")
                
    finally:
        db.close()
        
    yield # The server runs while paused here
    
    # Code after the yield would run on server shutdown
    logger.info("Shutting down...")

# Create the main FastAPI application object
app = FastAPI(
    title="AI Smart Civic Services API",
    description="API for managing civic complaints with AI classification",
    version="1.0.0",
    lifespan=lifespan
)

# --------------------------------------------------------------------------------
# CORS CONFIGURATION
# Cross-Origin Resource Sharing. This allows our frontend (even if hosted on a 
# different domain during dev) to talk to our backend without browser security blocks.
# --------------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real production app, restrict this to the actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------------
# GLOBAL EXCEPTION HANDLER
# This is a critical requirement from the prompt. If ANY unexpected error happens 
# anywhere in the backend, it gets caught here instead of crashing the server or 
# sending a raw, ugly Python stack trace to the user.
# --------------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled exception: {exc}")
    # We return a standard JSON response so the frontend can display a friendly message
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong on our end — please try again shortly."},
    )

# --------------------------------------------------------------------------------
# ROUTERS
# We attach the separate API files we created in the routers/ folder to the main app.
# --------------------------------------------------------------------------------
app.include_router(complaints.router, prefix="/api/complaints", tags=["Complaints"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

# --------------------------------------------------------------------------------
# HEALTH CHECK
# A simple endpoint used by deployment platforms (like Render) to see if the app is alive.
# --------------------------------------------------------------------------------
@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "Server is running perfectly."}

# --------------------------------------------------------------------------------
# FRONTEND STATIC FILES MOUNT
# This tells FastAPI to serve our HTML, CSS, and JS files directly.
# This means we don't need a separate server for the frontend — the single Render 
# web service will host both the backend API and the frontend website.
# Note: We put this LAST so it doesn't accidentally intercept API calls.
# --------------------------------------------------------------------------------
# We need to make sure the folder exists first, otherwise FastAPI crashes on startup
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "frontend"), exist_ok=True)
app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "frontend"), html=True), name="frontend")
