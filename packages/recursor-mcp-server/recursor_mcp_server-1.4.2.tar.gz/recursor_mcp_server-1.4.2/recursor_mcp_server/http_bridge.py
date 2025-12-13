"""
HTTP Bridge for MCP Server
Exposes MCP tools as REST API endpoints for Docker, n8n, and IDE integration
"""
import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from .client import RecursorClient

# Use standard logging instead of recursor.core.logging
logger = logging.getLogger("recursor_mcp_http_bridge")


# Pydantic models for request/response
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query for corrections")
    limit: int = Field(default=5, ge=1, le=50, description="Maximum number of results")


class SearchResponse(BaseModel):
    results: list
    count: int


class CorrectionRequest(BaseModel):
    original_code: str = Field(..., description="Original incorrect code")
    fixed_code: str = Field(..., description="Corrected code")
    explanation: str = Field(..., description="Explanation of the correction")


class CorrectionResponse(BaseModel):
    success: bool
    message: str
    correction_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    mcp_server: str
    api_connection: str


# Initialize FastAPI app
app = FastAPI(
    title="Recursor MCP HTTP Bridge",
    description="HTTP wrapper for Recursor MCP tools - enables Docker, n8n, and IDE integration",
    version="1.0.0"
)

# Add CORS middleware with secure configuration
# Get allowed origins from environment or use secure defaults
allowed_origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)


# Dependency to verify API key
async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    """Verify the API key from request headers"""
    expected_key = os.getenv("RECURSOR_API_KEY")
    if not expected_key:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: RECURSOR_API_KEY not set"
        )
    
    if x_api_key != expected_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return x_api_key


# Initialize client
def get_client():
    """Get RecursorClient instance"""
    try:
        return RecursorClient()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    client = get_client()
    api_connected = await client.check_health()
    
    return HealthResponse(
        status="healthy",
        mcp_server="running",
        api_connection="connected" if api_connected else "disconnected"
    )


@app.post("/search", response_model=SearchResponse)
async def search_corrections(
    request: SearchRequest,
    api_key: str = Depends(verify_api_key)
):
    """Search for corrections"""
    client = get_client()
    results = await client.search_corrections(request.query, request.limit)
    
    return SearchResponse(
        results=results,
        count=len(results)
    )


@app.post("/corrections", response_model=CorrectionResponse)
async def add_correction(
    request: CorrectionRequest,
    api_key: str = Depends(verify_api_key)
):
    """Add a new correction"""
    client = get_client()
    try:
        result = await client.add_correction(
            request.original_code,
            request.fixed_code,
            request.explanation
        )
        
        return CorrectionResponse(
            success=True,
            message="Correction saved successfully",
            correction_id=result.get("id")
        )
    except Exception as e:
        logger.error(f"Failed to add correction: {e}")
        return CorrectionResponse(
            success=False,
            message=str(e)
        )


def main():
    """Run the HTTP bridge server"""
    port = int(os.getenv("MCP_HTTP_PORT", "8001"))
    host = os.getenv("MCP_HTTP_HOST", "0.0.0.0")
    
    logger.info(f"Starting Recursor MCP HTTP Bridge on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()

