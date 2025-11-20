"""
Municipal Infrastructure Monitoring API
Main application file
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# Import routers here as you complete them
from routers.bridges import router as bridges_router
from routers.water_quality import router as water_quality_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Infrastructure API",
    description="A comprehensive API for monitoring municipal infrastructure",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
# TODO: Add your router here using the pattern below
app.include_router(bridges_router, prefix="/api/bridges", tags=["Bridges"])
app.include_router(water_quality_router, prefix="/api/water-quality", tags=["Water Quality"])

@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "name": "City Infrastructure API",
        "version": "1.0.0",
        "endpoints": [
            "/api/bridges",
            "/api/water-quality",
            # Add more as routers are completed
        ]
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
