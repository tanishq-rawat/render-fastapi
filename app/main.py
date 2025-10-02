"""
Main FastAPI application entry point.
Configures the application, middleware, and routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import create_tables
from app.routers import auth, expense, category


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for application startup and shutdown.
    Creates database tables on startup.
    """
    # Startup: Create database tables
    create_tables()
    print("✅ Database tables created successfully")
    yield
    # Shutdown: Cleanup if needed
    print("👋 Application shutting down")


# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    description="A Progressive Web App for tracking personal expenses with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(expense.router, prefix="/api/v1")
app.include_router(category.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Welcome to Expense Tracker API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected"
    }
