"""Main FastAPI application interface."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import router1, router2

# Initialize FastAPI app
rest_api = FastAPI(
    title="{project_name}",
    description="FastAPI application with multiple routers",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        {
            "email": "{author_email}",
        }
    },
)

# Configure CORS
rest_api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
rest_api.include_router(router1.router)
rest_api.include_router(router2.router)


@rest_api.get("/")
async def root() -> dict:
    """
    Root endpoint.

    Returns:
        dict: Welcome message
    """
    return {{"message": "Welcome to {{project_name}}", "docs": "/docs"}}


@rest_api.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {{"status": "healthy", "service": "{{project_name}}"}}
