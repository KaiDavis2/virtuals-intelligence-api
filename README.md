# Virtuals Intelligence API

> GitHub trending intelligence for AI agents

## Overview

REST API providing curated GitHub trending data with intelligence layer for AI personality systems.

## Pricing

**$0.05 per request** via x402 payment protocol.

## Endpoints

### Service Discovery (Free)

```bash
GET /
```

Returns API metadata and x402 configuration.

---

### Trending Repos ($0.05)

```bash
GET /api/v1/trending/{language}
X-Payment: <x402-signature>
```

**Languages:** `python`, `javascript`, `typescript`, `rust`, `go`, `ai`, `all`

**Response:**
```json
{
  "language": "python",
  "repos": [
    {
      "name": "transformers",
      "url": "https://github.com/huggingface/transformers",
      "stars_today": 234,
      "ai_summary": "transformers is trending with 234 new stars today...",
      "key_features": ["Highly popular (10K+ stars)", "Viral growth"],
      "why_trending": "transformers gained significant attention today"
    }
  ],
  "market_insight": "The python ecosystem shows 1,200 new stars across top 10 projects",
  "opportunity_hooks": ["VIRAL TREND: transformers is exploding"]
}
```

---

### Quick Check ($0.05)

```bash
GET /api/v1/quick/{language}
X-Payment: <x402-signature>
```

Returns top 3 trending repos. Optimized for low-latency use cases.

---

### Analyze Repository ($0.05)

```bash
POST /api/v1/analyze
X-Payment: <x402-signature>

{
  "repo_url": "https://github.com/owner/repo"
}
```

**Response:**
```json
{
  "name": "repo",
  "what_it_does": "Provides tools and utilities for developers",
  "why_it_matters": "Solves common development challenges",
  "conversation_hooks": [
    "Have you seen owner's work on repo?",
    "repo is gaining traction in the developer community"
  ]
}
```

---

## Payment Flow

This API uses the x402 payment protocol:

1. Request endpoint → API returns `402 Payment Required`
2. Response includes payment details:
   ```json
   {
     "x402Version": 1,
     "accepts": [{
       "network": "base",
       "maxAmountRequired": "50000",
       "asset": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
       "payTo": "0x8A82Da027AaAE5D32C6694D6B251615f060d8F84"
     }]
   }
   ```
3. Send $0.05 USDC on Base network
4. Retry request with signed payment proof
5. Receive response

---

## Data Source

GitHub Trending RSS feeds — no authentication required.

- URL: `https://mshibanami.github.io/GitHubTrendingRSS/daily/{language}.xml`
- Update frequency: Daily
- No rate limits

---

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn pydantic feedparser requests beautifulsoup4

# Run locally
uvicorn app.main:app --reload

# Test free endpoint
curl http://localhost:8000/

# Test paid endpoint (returns 402)
curl http://localhost:8000/api/v1/trending/python
```

---

## Project Structure

```
virtuals_intelligence_api/
├── app/
│   ├── __init__.py
│   ├── main.py       # FastAPI + x402 middleware
│   ├── models.py     # Pydantic schemas
│   └── data.py       # GitHub RSS + intelligence layer
├── Dockerfile
├── railway.toml
├── requirements.txt
└── README.md
```

---

## Beta Status

**Version:** 1.0-beta

**Current Limitations:**
- RSS feed may have update delays
- Mock fallback data if RSS unavailable
- Payment verification is header-only

**Roadmap:**
- Full x402 signature verification
- Real-time GitHub API option
- Additional languages
- Historical trending data

---

## License

MIT
