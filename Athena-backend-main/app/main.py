"""
Main FastAPI application
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.routes import auth_routes, student_routes, teacher_routes, admin_routes, rooms_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered EdTech platform backend API",
    version="1.0.0",
    lifespan=lifespan
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)


# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"][1:])  # Skip 'body'
        message = error["msg"]
        errors.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors,
            "message": "; ".join(errors) if errors else "Invalid request data"
        }
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ATHENA EdTech Platform API",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(auth_routes.router)
app.include_router(student_routes.router)
app.include_router(teacher_routes.router)
app.include_router(admin_routes.router)
app.include_router(rooms_routes.router, prefix="/rooms", tags=["Rooms"])
from app.routes.assistant_routes import router as assistant_router
app.include_router(assistant_router)
from app.routes.rag_router import router as rag_router
app.include_router(rag_router)
# ❌ DISABLED: Conversation routes (stateless mode - no history)
# from app.routes.conversation_routes import router as conversation_router
# app.include_router(conversation_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
