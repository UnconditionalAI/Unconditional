"""FastAPI application entry point for Unconditional API.

Minimal, focused backend providing conversation processing with safety-first design.
"""

from typing import cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.endpoints import conversation

# Application metadata
app = FastAPI(
    title="Unconditional API",
    description=(
        "Steady, compassionate, AI-supported presence for people "
        "during moments when they feel most alone"
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
# MVP: Allow all origins for development
# Production: Restrict to frontend domain
# Note: CORSMiddleware typing issue with strict type checkers is a known FastAPI pattern
# The middleware works correctly at runtime despite the type mismatch
app.add_middleware(
    cast(type, CORSMiddleware),
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    conversation.router,
    prefix="/api/v1",
    tags=["conversation"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "service": "Unconditional API",
        "version": "0.1.0",
        "status": "operational",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
