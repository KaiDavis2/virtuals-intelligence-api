# Virtuals Intelligence API v1.0

> **GitHub trending intelligence for AI personalities**

## 🎯 THE MARKET

**Target:** 3,700 AI personalities on Virtuals Protocol
**Competition:** 2 sellers
**Ratio:** 1,850:1 (Blue Ocean)

---

## 💰 PRICING

**$0.05 per request** (x402 sweet spot)

| Volume | Revenue | Break-even |
|--------|---------|------------|
| 320/month | $16 | Not viable |
| 3,200/month | $160 | API costs covered |
| 12,800/month | $640 | Full break-even |

**Market share needed:** 11.5% (427/day of 3,700 buyers)

---

## 🚀 ENDPOINTS

### FREE: Service Discovery

```bash
GET /
```

Returns API metadata and x402 config.

---

### PAID ($0.05): Trending Repos

```bash
GET /api/v1/trending/{language}
X-Payment: <your-x402-signature>
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

### PAID ($0.05): Quick Check

```bash
GET /api/v1/quick/{language}
X-Payment: <your-x402-signature>
```

Returns top 3 only. Optimized for speed.

---

### PAID ($0.05): Analyze Specific Repo

```bash
POST /api/v1/analyze
X-Payment: <your-x402-signature>

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

## 💳 x402 PAYMENT FLOW

1. **Request** → API returns `402 Payment Required`
2. **Response:**
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
3. **Pay** → Send $0.05 USDC on Base
4. **Retry** → Include signed proof
5. **Success** → Get intelligence

---

## 🔧 DATA SOURCE

**GitHub Trending RSS** — Free, no authentication required

- URL: `https://mshibanami.github.io/GitHubTrendingRSS/daily/{language}.xml`
- Update frequency: Daily
- No rate limits
- No API key needed

---

## 🚀 QUICK START

```bash
# Install
pip install fastapi uvicorn pydantic feedparser requests beautifulsoup4

# Run locally
cd api_design/virtuals_intelligence_api
uvicorn app.main:app --reload

# Test free endpoint
curl http://localhost:8000/

# Test paid endpoint (returns 402)
curl http://localhost:8000/api/v1/trending/python
```

---

## 📊 BREAK-EVEN MATH

| Metric | Value |
|--------|-------|
| Monthly API cost | $160 |
| Price per request | $0.05 |
| Requests to break-even | 12,800/month |
| Daily target | 427 |
| Market share needed | 11.5% of 3,700 |

**At 12,800 req/month ($640):**
- 25% → API costs ($160) ✅
- 25% → Sanctuary Fund ($160)
- 25% → Animal Charities ($160)
- 25% → Tania's Land Fund ($160)

---

## 🔒 WALLET

**Payment Recipient:** `0x8A82Da027AaAE5D32C6694D6B251615f060d8F84`

---

## 📂 STRUCTURE

```
virtuals_intelligence_api/
├── app/
│   ├── __init__.py
│   ├── main.py       ← FastAPI + x402
│   ├── models.py     ← Pydantic
│   └── data.py       ← GitHub RSS + intelligence
├── Dockerfile
├── railway.toml
├── requirements.txt
└── README.md
```

---

## ⚠️ BETA STATUS

**Current:** v1.0-beta

**Limitations:**
- RSS feed may have delays
- Mock fallback if RSS fails
- Payment verification is header-only

**Roadmap:**
- [ ] Full x402 signature verification
- [ ] Real-time GitHub API option
- [ ] More languages
- [ ] Historical trending data

---

## 🎯 THE BLUE OCEAN

| Metric | Value |
|--------|-------|
| Buyers/Day | 3,700 |
| Sellers | 2 |
| Competition | Almost zero |
| Sweet spot pricing | ✅ $0.05 |

**This is the water. Flow into it.**

---

*Built for THE MISSION & VISION*

**Every request funds the Sanctuary. 🐾**
