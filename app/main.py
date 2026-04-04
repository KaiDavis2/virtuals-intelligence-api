"""
Virtuals Intelligence API v1.1
GitHub trending intelligence for AI personalities (Virtuals Protocol)

Updated: Added x402 Bazaar extension for automatic discovery
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import time
import base64
import json
from datetime import datetime, timedelta

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

# x402 Official SDK imports
try:
    from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
    from x402.http.middleware.fastapi import PaymentMiddlewareASGI
    from x402.http.types import RouteConfig
    from x402.mechanisms.evm.exact import ExactEvmServerScheme
    from x402.server import x402ResourceServer
    X402_SDK_AVAILABLE = True
except ImportError:
    X402_SDK_AVAILABLE = False
    print("WARNING: x402 SDK not installed. Run: pip install 'x402[fastapi]'")

# FastAPI app
app = FastAPI(
    title="Virtuals Intelligence API",
    version="1.1.0",
    description="GitHub trending intelligence for AI personalities with x402 Bazaar discovery"
)

# CORS for browser agents
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Payment-Required", "X402-Version", "PAYMENT-REQUIRED"]
)

# x402 Configuration - $0.05 sweet spot
X402_PRICE_USD = 0.05
X402_PRICE_MICRO = 50000  # $0.05 in micro-units
X402_RECIPIENT = "0x8A82Da027AaAE5D32C6694D6B251615f060d8F84"
X402_NETWORK = "eip155:8453"  # Base mainnet
X402_FACILITATOR = "https://x402.org/facilitator"
X402_ASSET = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"  # USDC on Base


# ============================================
# OFFICIAL x402 SDK SETUP WITH BAZAAR
# ============================================

if X402_SDK_AVAILABLE:
    # Create facilitator client
    facilitator = HTTPFacilitatorClient(
        FacilitatorConfig(url=X402_FACILITATOR)
    )
    
    # Create resource server
    server = x402ResourceServer(facilitator)
    server.register(X402_NETWORK, ExactEvmServerScheme())
    
    # Define routes with Bazaar discovery metadata
    routes: dict[str, RouteConfig] = {
        "GET /api/v1/trending/{language}": RouteConfig(
            accepts=[
                PaymentOption(
                    scheme="exact",
                    pay_to=X402_RECIPIENT,
                    price=f"${X402_PRICE_USD}",
                    network=X402_NETWORK,
                ),
            ],
            mime_type="application/json",
            description="Get trending GitHub repos with AI-enhanced market insights",
            extensions={
                "bazaar": {
                    "info": {
                        "output": {
                            "type": "json",
                            "example": {
                                "language": "python",
                                "repos": [{
                                    "name": "modelcontextprotocol/servers",
                                    "url": "https://github.com/modelcontextprotocol/servers",
                                    "stars_today": 847,
                                    "why_trending": "MCP protocol adoption surge",
                                    "ai_summary": "Model Context Protocol servers for AI agents"
                                }],
                                "market_insight": "AI agent tooling trending +340%",
                                "opportunity_hooks": ["Build MCP server", "Integrate with Claude"]
                            },
                        },
                    },
                },
            },
        ),
        "POST /api/v1/analyze": RouteConfig(
            accepts=[
                PaymentOption(
                    scheme="exact",
                    pay_to=X402_RECIPIENT,
                    price=f"${X402_PRICE_USD}",
                    network=X402_NETWORK,
                ),
            ],
            mime_type="application/json",
            description="Analyze a specific GitHub repository",
            extensions={
                "bazaar": {
                    "info": {
                        "output": {
                            "type": "json",
                            "example": {
                                "repo": "openai/openai-python",
                                "analysis": "Official OpenAI Python SDK",
                                "conversation_hooks": ["SDK best practices", "Error handling"]
                            },
                        },
                    },
                },
            },
        ),
        "GET /api/v1/quick/{language}": RouteConfig(
            accepts=[
                PaymentOption(
                    scheme="exact",
                    pay_to=X402_RECIPIENT,
                    price=f"${X402_PRICE_USD}",
                    network=X402_NETWORK,
                ),
            ],
            mime_type="application/json",
            description="Quick trending check (top 3 repos, optimized for speed)",
            extensions={
                "bazaar": {
                    "info": {
                        "output": {
                            "type": "json",
                            "example": {
                                "language": "all",
                                "top_3": [{"name": "trending/repo", "stars_today": 500}],
                                "hottest": "trending/repo"
                            },
                        },
                    },
                },
            },
        ),
    }
    
    # Add payment middleware
    app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)
    print("✅ x402 SDK with Bazaar extension loaded")


# ============================================
# LEGACY FALLBACK (if SDK unavailable)
# ============================================

def verify_x402_payment_legacy(request: Request) -> bool:
    """Fallback payment verification"""
    payment_header = request.headers.get("X-Payment") or request.headers.get("PAYMENT-SIGNATURE")
    if not payment_header:
        return False
    return len(payment_header) > 10


def create_402_response() -> JSONResponse:
    """Create x402 v2 Payment Required response"""
    payment_requirements = {
        "x402Version": 2,
        "scheme": "exact",
        "network": "base",
        "maxAmountRequired": str(X402_PRICE_MICRO),
        "asset": {
            "address": X402_ASSET,
            "symbol": "USDC",
            "decimals": 6
        },
        "recipient": X402_RECIPIENT,
        "facilitator": X402_FACILITATOR,
        "resource": "/api/v1/trending",
        "description": "GitHub trending intelligence for AI personalities"
    }
    
    payment_header_b64 = base64.b64encode(
        json.dumps(payment_requirements).encode()
    ).decode()
    
    return JSONResponse(
        status_code=402,
        content={
            "x402Version": 2,
            "error": "Payment Required",
            "accepts": [{
                "scheme": "exact",
                "network": "base",
                "maxAmountRequired": str(X402_PRICE_MICRO),
                "asset": X402_ASSET,
                "payTo": X402_RECIPIENT,
                "facilitator": X402_FACILITATOR
            }],
            "instructions": f"Send ${X402_PRICE_USD} USDC to {X402_RECIPIENT} on Base",
            "autoPay": "Wallets with x402 support will auto-sign this payment"
        },
        headers={
            "PAYMENT-REQUIRED": payment_header_b64,
            "X-Payment-Required": "true",
            "X402-Version": "2",
            "Access-Control-Expose-Headers": "PAYMENT-REQUIRED, X-Payment-Required, X402-Version"
        }
    )


# ============================================
# FREE ENDPOINTS (No payment required)
# ============================================

@app.get("/", response_model=DiscoveryResponse)
async def service_discovery():
    """
    FREE: Service discovery endpoint
    Returns API metadata and x402 configuration
    """
    return DiscoveryResponse(
        service="Virtuals Intelligence API",
        version="1.1.0",
        description="GitHub trending intelligence for AI personalities",
        pricing={"per_request": "$0.05"},
        languages_supported=["python", "javascript", "typescript", "rust", "go", "ai", "all"],
        x402={
            "version": 2,
            "price_usd": X402_PRICE_USD,
            "network": "base",
            "asset": X402_ASSET,
            "recipient": X402_RECIPIENT,
            "facilitator": X402_FACILITATOR,
            "auto_pay_enabled": True,
            "bazaar_enabled": True
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "virtuals-intelligence",
        "x402_sdk": X402_SDK_AVAILABLE,
        "bazaar_ready": X402_SDK_AVAILABLE
    }


@app.get("/api/v1/sample/{language}")
async def free_sample(language: str = "all"):
    """
    FREE: Single repo sample (STALE - 24h delayed)
    
    Try the API before purchasing. Returns 1 repo with DELAYED data.
    For REAL-TIME trending data, use /api/v1/trending/{language} ($0.05)
    """
    raw_repos = fetch_trending_rss(language=language, time_range="daily")[:1]
    repos = [build_github_repo(r) for r in raw_repos]
    
    if not repos:
        return {"error": "No trending repos found", "language": language}
    
    repo = repos[0]
    stale_timestamp = datetime.utcnow() - timedelta(hours=24)
    
    return {
        "sample": True,
        "freshness": "24h_delayed",
        "data_timestamp": stale_timestamp.isoformat() + "Z",
        "warning": "FREE data is 24 hours old. Pay for real-time.",
        "language": language,
        "repo": {
            "name": repo.name,
            "url": repo.url,
            "stars_today": repo.stars_today,
            "why": repo.why_trending,
            "hook": repo.ai_summary[:100] if repo.ai_summary else None
        },
        "upgrade": {
            "message": "Get REAL-TIME trending + market insights for $0.05",
            "value_prop": "Be first to trends. Stale data = missed opportunities.",
            "endpoint": f"/api/v1/trending/{language}",
            "price_usd": X402_PRICE_USD
        },
        "powered_by": "Virtuals Intelligence API v1.1 with x402 Bazaar"
    }


# ============================================
# PAID ENDPOINTS ($0.05 each)
# ============================================

@app.get("/api/v1/trending/{language}")
async def get_trending(request: Request, language: str = "all"):
    """
    PAID ($0.05): Get trending GitHub repos for a language
    
    Returns AI-enhanced summaries and market insights for AI personalities
    
    x402 Payment Required - Bazaar registered
    """
    # If SDK not available, use legacy check
    if not X402_SDK_AVAILABLE and not verify_x402_payment_legacy(request):
        return create_402_response()
    
    valid_languages = ["all", "python", "javascript", "typescript", "rust", "go", "ai"]
    if language.lower() not in valid_languages:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid language. Supported: {', '.join(valid_languages)}"
        )
    
    raw_repos = fetch_trending_rss(language=language, time_range="daily")
    repos = [build_github_repo(r) for r in raw_repos]
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


@app.post("/api/v1/analyze")
async def analyze_repo(request: Request, body: RepoSummaryRequest):
    """
    PAID ($0.05): Analyze a specific GitHub repository
    
    Returns detailed analysis with conversation hooks for AI personalities
    
    x402 Payment Required - Bazaar registered
    """
    if not X402_SDK_AVAILABLE and not verify_x402_payment_legacy(request):
        return create_402_response()
    
    try:
        analysis = analyze_specific_repo(body.repo_url)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to analyze repository")


@app.get("/api/v1/quick/{language}")
async def quick_trending(request: Request, language: str = "all"):
    """
    PAID ($0.05): Quick trending check (top 3 repos, optimized for speed)
    
    x402 Payment Required - Bazaar registered
    """
    if not X402_SDK_AVAILABLE and not verify_x402_payment_legacy(request):
        return create_402_response()
    
    raw_repos = fetch_trending_rss(language=language, time_range="daily")[:3]
    repos = [build_github_repo(r) for r in raw_repos]
    
    return {
        "language": language,
        "top_3": [
            {
                "name": r.name,
                "url": r.url,
                "stars_today": r.stars_today,
                "why": r.why_trending,
                "hook": r.ai_summary[:100] if r.ai_summary else None
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
    print(f"🚀 Starting Virtuals Intelligence API v1.1")
    print(f"   x402 SDK: {'✅' if X402_SDK_AVAILABLE else '❌'}")
    print(f"   Bazaar: {'✅ Ready' if X402_SDK_AVAILABLE else '❌ Install x402[fastapi]'}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
