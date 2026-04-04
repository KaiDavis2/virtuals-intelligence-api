"""
Virtuals Intelligence API v1.0
GitHub trending intelligence for AI personalities (Virtuals Protocol)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import time
from datetime import datetime

from .models import (
    TrendingLanguage, TimeRange, GitHubRepo, 
    TrendingResponse, RepoSummaryRequest, RepoSummaryResponse,
    DiscoveryResponse, ErrorResponse
)
from .data import (
    fetch_trending_rss, build_github_repo, 
    generate_market_insight, generate_opportunity_hooks,
    analyze_specific_repo
)

# FastAPI app
app = FastAPI(
    title="Virtuals Intelligence API",
    version="1.0.0",
    description="GitHub trending intelligence for AI personalities"
)

# CORS for browser agents
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Payment-Required", "X402-Version"]
)

# x402 Configuration - $0.05 sweet spot
X402_PRICE_MICRO = 50000  # $0.05 in micro-units
X402_RECIPIENT = "0x8A82Da027AaAE5D32C6694D6B251615f060d8F84"
X402_NETWORK = "base"
X402_FACILITATOR = "https://x402.org/facilitator"
X402_ASSET = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"  # USDC on Base


def verify_x402_payment(request: Request) -> bool:
    """
    Verify x402 payment signature
    In production: validate cryptographic signature
    For beta: check header presence
    """
    payment_header = request.headers.get("X-Payment") or request.headers.get("PAYMENT-SIGNATURE")
    
    if not payment_header:
        return False
    
    # TODO: Implement full signature verification
    return len(payment_header) > 10


def create_402_response() -> JSONResponse:
    """Create x402 Payment Required response"""
    return JSONResponse(
        status_code=402,
        content={
            "x402Version": 1,
            "error": "Payment Required",
            "accepts": [{
                "scheme": "exact",
                "network": X402_NETWORK,
                "maxAmountRequired": str(X402_PRICE_MICRO),
                "asset": X402_ASSET,
                "payTo": X402_RECIPIENT,
                "facilitator": X402_FACILITATOR
            }],
            "instructions": f"Send ${X402_PRICE_MICRO / 1_000_000:.2f} USDC to {X402_RECIPIENT} on {X402_NETWORK}"
        },
        headers={
            "X-Payment-Required": "true",
            "X402-Version": "1"
        }
    )


# ============================================
# FREE ENDPOINTS
# ============================================

@app.get("/", response_model=DiscoveryResponse)
async def service_discovery():
    """
    FREE: Service discovery endpoint
    Returns API metadata and x402 configuration
    """
    return DiscoveryResponse(
        service="Virtuals Intelligence API",
        version="1.0.0",
        description="GitHub trending intelligence for AI personalities",
        pricing={"per_request": "$0.05"},
        languages_supported=["python", "javascript", "typescript", "rust", "go", "ai", "all"],
        x402={
            "version": 1,
            "price_usd": 0.05,
            "network": X402_NETWORK,
            "asset": X402_ASSET,
            "recipient": X402_RECIPIENT
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "virtuals-intelligence"
    }


# ============================================
# PAID ENDPOINTS ($0.05 each)
# ============================================

@app.get("/api/v1/trending/{language}", responses={402: {"model": dict}})
async def get_trending(request: Request, language: str = "all"):
    """
    PAID ($0.05): Get trending GitHub repos for a language
    
    Returns AI-enhanced summaries and market insights for AI personalities
    """
    # Check payment
    if not verify_x402_payment(request):
        return create_402_response()
    
    # Validate language
    valid_languages = ["all", "python", "javascript", "typescript", "rust", "go", "ai"]
    if language.lower() not in valid_languages:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid language. Supported: {', '.join(valid_languages)}"
        )
    
    # Fetch trending repos
    raw_repos = fetch_trending_rss(language=language, time_range="daily")
    
    # Build GitHubRepo models
    repos = [build_github_repo(r) for r in raw_repos]
    
    # Generate intelligence layer
    market_insight = generate_market_insight(raw_repos, language)
    opportunity_hooks = generate_opportunity_hooks(raw_repos)
    
    return TrendingResponse(
        language=language,
        time_range="daily",
        repos=repos,
        market_insight=market_insight,
        opportunity_hooks=opportunity_hooks,
        count=len(repos),
        scraped_at=datetime.utcnow(),
        cache_hit=False
    )


@app.post("/api/v1/analyze", responses={402: {"model": dict}})
async def analyze_repo(request: Request, body: RepoSummaryRequest):
    """
    PAID ($0.05): Analyze a specific GitHub repository
    
    Returns detailed analysis with conversation hooks for AI personalities
    """
    # Check payment
    if not verify_x402_payment(request):
        return create_402_response()
    
    try:
        analysis = analyze_specific_repo(body.repo_url)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to analyze repository")


@app.get("/api/v1/quick/{language}", responses={402: {"model": dict}})
async def quick_trending(request: Request, language: str = "all"):
    """
    PAID ($0.05): Quick trending check (simplified response)
    
    Optimized for speed - returns top 3 repos only
    """
    # Check payment
    if not verify_x402_payment(request):
        return create_402_response()
    
    # Fetch trending
    raw_repos = fetch_trending_rss(language=language, time_range="daily")[:3]
    repos = [build_github_repo(r) for r in raw_repos]
    
    # Return simplified response
    return {
        "language": language,
        "top_3": [
            {
                "name": r.name,
                "url": r.url,
                "stars_today": r.stars_today,
                "why": r.why_trending,
                "hook": r.ai_summary[:100]
            }
            for r in repos
        ],
        "hottest": repos[0].name if repos else None,
        "total_stars_today": sum(r.stars_today or 0 for r in repos)
    }


# ============================================
# ERROR HANDLERS
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "code": f"HTTP_{exc.status_code}"}
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc), "code": "INVALID_INPUT"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
