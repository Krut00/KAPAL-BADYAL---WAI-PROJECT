from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.api import companies, analysis

# Create FastAPI app
app = FastAPI(
    title="CCC Analyzer API",
    description="Cash Conversion Cycle Analysis API",
    version="1.0.0"
)

# CORS middleware configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5000,https://badyal.pages.dev").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok", "message": "CCC Analyzer API is running"}

# Include routers
app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
