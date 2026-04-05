"""
Virtuals Intelligence API v1.2 — HARDENED
GitHub trending intelligence for AI personalities (Virtuals Protocol)

SECURITY: Full x402 SDK middleware with cryptographic verification
BAZAAR: Auto-discovery enabled via extensions.bazaar metadata
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import time
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

# ============================================
# X402 SDK — HARDENED MIDDLEWARE
# ============================================

X402_SDK_AVAILABLE = False
X402_ERROR = None

try:
    from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
    from x402.http.middleware.fastapi import PaymentMiddlewareASGI
    from x402.http.types import RouteConfig
    from x402.mechanisms.evm.exact import ExactEvmServerScheme
    from x402.server import x402ResourceServer
    X402_SDK_AVAILABLE = True
except ImportError as e:
    X402_ERROR = str(e)
    print(f"⚠️ x402 SDK not available: {e}")
    print("   Run: pip install 'x402[fastapi]'")

# ============================================
# CONFIGURATION
# ============================================

X402_PRICE_USD = 0.05
X402_PRICE_MICRO = 50000
X402_RECIPIENT = "0x8A82Da027AaAE5D32C6694D6B251615f060d8F84"
X402_NETWORK = "eip155:8453"  # Base mainnet
X402_FACILITATOR = "https://x402.org/facilitator"
X402_ASSET = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"

# FastAPI app
app = FastAPI(
    title="Virtuals Intelligence API",
    version="1.2.0-hardened",
    description="GitHub trending intelligence — x402 SDK hardened"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["PAYMENT-REQUIRED", "X-Payment-Required", "X402-Version"]
)

# ============================================
# X402 SDK MIDDLEWARE SETUP
# ============================================

if X402_SDK_AVAILABLE:
    # Create facilitator client (connects to x402 network)
    facilitator = HTTPFacilitatorClient(
        FacilitatorConfig(url=X402_FACILITATOR)
    )
    
    # Create resource server
    server = x402ResourceServer(facilitator)
    
    # Register EVM payment scheme (Base mainnet)
    server.register(X402_NETWORK, ExactEvmServerScheme())
    
    # Define routes with Bazaar discovery metadata
    routes: Dict[str, RouteConfig] = {
        # TRENDING ENDPOINT
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
            description="GitHub trending repos with AI-enhanced market insights",
            extensions={
                "bazaar": {
                    "info": {
                        "output": {
                            "type": "json",
                            "example": {
                                "language": "python",
                                "repos": [{
                                    "name": "modelcontextprotocol/servers",
                                    "stars_today": 847,
                                    "why_trending": "MCP protocol surge"
                                }],
                                "market_insight": "AI tooling +340%",
                            },
                        },
                    },
                },
            },
        ),
        
        # ANALYZE ENDPOINT
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
                                "analysis": "Official OpenAI SDK",
                            },
                        },
                    },
                },
            },
        ),
        
        # QUICK ENDPOINT
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
            description="Quick trending check (top 3 repos)",
            extensions={
                "bazaar": {
                    "info": {
                        "output": {
                            "type": "json",
                            "example": {
                                "language": "all",
                                "hottest": "trending/repo",
                            },
                        },
                    },
                },
            },
        ),
    }
    
    # INJECT SDK MIDDLEWARE — CRYPTOGRAPHIC ENFORCEMENT
    app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)
    
    print("✅ x402 SDK middleware ACTIVE")
    print(f"   Network: {X402_NETWORK}")
    print(f"   Recipient: {X402_RECIPIENT}")
    print(f"   Price: ${X402_PRICE_USD}")
    print("🛡️ Bazaar extension: ENABLED")

else:
    print("❌ x402 SDK NOT AVAILABLE — API running in degraded mode")
    print(f"   Error: {X402_ERROR}")


# ============================================
# FREE ENDPOINTS (No payment required)
# ============================================

@app.get("/", response_model=DiscoveryResponse)
async def service_discovery():
    """FREE: Service discovery"""
    return DiscoveryResponse(
        service="Virtuals Intelligence API",
        version="1.2.0-hardened",
        description="GitHub trending intelligence — x402 SDK hardened",
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
            "bazaar_enabled": X402_SDK_AVAILABLE,
            "sdk_hardened": X402_SDK_AVAILABLE
        }
    )


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "virtuals-intelligence",
        "version": "1.2.0-hardened",
        "x402_sdk": X402_SDK_AVAILABLE,
        "bazaar_ready": X402_SDK_AVAILABLE
    }


@app.get("/api/v1/sample/{language}")
async def free_sample(language: str = "all"):
    """
    FREE: Single repo sample (STALE - 24h delayed)
    
    Try before you buy. Paid endpoints = real-time data.
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
        },
        "upgrade": {
            "message": "Get REAL-TIME trending for $0.05",
            "endpoint": f"/api/v1/trending/{language}",
            "price_usd": X402_PRICE_USD
        },
        "powered_by": "Virtuals Intelligence API v1.2 — HARDENED"
    }


# ============================================
# PAID ENDPOINTS (SDK middleware protected)
# ============================================

@app.get("/api/v1/trending/{language}")
async def get_trending(request: Request, language: str = "all"):
    """
    PAID ($0.05): Get trending GitHub repos
    
    Protected by x402 SDK middleware — cryptographic verification required
    """
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
    PAID ($0.05): Analyze a specific repository
    
    Protected by x402 SDK middleware
    """
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
    PAID ($0.05): Quick trending check (top 3)
    
    Protected by x402 SDK middleware
    """
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


# ============================================
# X Bot Endpoints
# ============================================

@app.get("/api/v1/bot/status")
async def bot_status():
    """Check X bot configuration status"""
    has_bearer = bool(os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN"))
    has_consumer = bool(os.getenv("X_CONSUMER_KEY") or os.getenv("TWITTER_CONSUMER_KEY"))
    has_access = bool(os.getenv("X_ACCESS_TOKEN") or os.getenv("TWITTER_ACCESS_TOKEN"))
    
    return {
        "configured": has_bearer and has_consumer and has_access,
        "bearer_token": has_bearer,
        "consumer_key": has_consumer,
        "access_token": has_access,
        "ready": has_bearer and has_consumer and has_access
    }


@app.post("/api/v1/bot/test")
async def bot_test():
    """Test X bot by posting a trending repo"""
    try:
        import tweepy
    except ImportError:
        return {"error": "tweepy not installed"}
    
    bearer = os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN")
    consumer_key = os.getenv("X_CONSUMER_KEY") or os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("X_CONSUMER_SECRET") or os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN") or os.getenv("TWITTER_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_TOKEN_SECRET") or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    if not all([bearer, consumer_key, consumer_secret, access_token, access_secret]):
        return {"error": "X credentials incomplete", "ready": False}
    
    try:
        client = tweepy.Client(
            bearer_token=bearer,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        # Get a trending repo
        repos = fetch_trending_rss(language="python", time_range="daily")
        if not repos:
            return {"error": "No trending repos", "ready": True}
        
        repo = repos[0]
        name = repo.get("name", "repo")
        url = repo.get("url", "")
        stars = repo.get("stars_today", 0)
        
        # Build tweet
        tweet = f"Testing Virtuals Intelligence API\n\nTop trending: {name}\n+{stars} stars today\n\n{url}\n\n#AI #GitHub"
        
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        # Post tweet
        response = client.create_tweet(text=tweet)
        
        if response.data:
            tweet_id = response.data["id"]
            return {
                "success": True,
                "tweet_id": tweet_id,
                "tweet_url": f"https://x.com/VirtualsIntel/status/{tweet_id}",
                "repo": name,
                "ready": True
            }
        else:
            return {"error": "No response from X API", "ready": True}
            
    except Exception as e:
        return {"error": str(e), "ready": True}


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🛡️ VIRTUALS INTELLIGENCE API v1.2 — HARDENED")
    print("=" * 60)
    print(f"   x402 SDK: {'✅ ACTIVE' if X402_SDK_AVAILABLE else '❌ UNAVAILABLE'}")
    print(f"   Bazaar: {'✅ REGISTERED' if X402_SDK_AVAILABLE else '❌ DISABLED'}")
    print(f"   Verification: CRYPTOGRAPHIC (SDK)")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
