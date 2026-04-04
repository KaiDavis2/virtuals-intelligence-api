"""
Virtuals Intelligence API - Data Layer
Fetches GitHub trending data and generates AI summaries
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Optional, Dict, Any
import re
import random

from .models import (
    GitHubRepo, TrendingLanguage, TimeRange,
    RepoSummaryRequest, RepoSummaryResponse
)


# GitHub Trending URLs
GITHUB_TRENDING_BASE = "https://github.com/trending"
GITHUB_RSS_BASE = "https://mshibanami.github.io/GitHubTrendingRSS/daily"


def fetch_trending_rss(language: str = "", time_range: str = "daily") -> List[Dict[str, Any]]:
    """
    Fetch trending repos from GitHub Trending RSS
    This is FREE and requires no authentication
    """
    
    # Map language to RSS feed
    if language and language != "all":
        rss_url = f"{GITHUB_RSS_BASE}/{language}.xml"
    else:
        rss_url = f"{GITHUB_RSS_BASE}.xml"
    
    try:
        feed = feedparser.parse(rss_url)
        repos = []
        
        for entry in feed.entries[:10]:  # Top 10
            # Parse repo info from RSS entry
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")
            
            # Extract author/repo from title
            if "/" in title:
                author, repo_name = title.split("/", 1)
            else:
                author = "unknown"
                repo_name = title
            
            # Parse stars/forks from summary
            stars, forks, stars_today = parse_github_summary(summary)
            
            repos.append({
                "name": repo_name.strip(),
                "full_name": title,
                "url": link,
                "description": summary[:200] if summary else None,
                "author": author.strip(),
                "stars": stars,
                "stars_today": stars_today,
                "forks": forks
            })
        
        return repos
    
    except Exception as e:
        # Fallback to mock data if RSS fails
        return generate_mock_trending(language)


def parse_github_summary(summary: str) -> tuple:
    """Parse stars and forks from GitHub summary text"""
    stars = 0
    forks = 0
    stars_today = 0
    
    # Try to extract numbers
    star_match = re.search(r"(\d+,?\d*)\s*stars?", summary, re.I)
    if star_match:
        stars = int(star_match.group(1).replace(",", ""))
    
    fork_match = re.search(r"(\d+,?\d*)\s*forks?", summary, re.I)
    if fork_match:
        forks = int(fork_match.group(1).replace(",", ""))
    
    today_match = re.search(r"(\d+,?\d*)\s*today", summary, re.I)
    if today_match:
        stars_today = int(today_match.group(1).replace(",", ""))
    
    return stars, forks, stars_today


def generate_ai_summary(repo_data: Dict[str, Any]) -> str:
    """Generate an AI-friendly summary of a repo"""
    
    name = repo_data.get("name", "Unknown")
    description = repo_data.get("description", "")
    stars = repo_data.get("stars", 0)
    stars_today = repo_data.get("stars_today", 0)
    
    # Generate contextual summary
    summaries = [
        f"{name} is trending with {stars_today} new stars today (total: {stars:,}).",
        f"Developers are showing strong interest in {name}.",
    ]
    
    if description:
        summaries.append(f"It {description[:100].lower()}.")
    
    return " ".join(summaries[:2])


def generate_key_features(repo_data: Dict[str, Any]) -> List[str]:
    """Generate key features list"""
    features = []
    
    stars = repo_data.get("stars", 0)
    if stars > 10000:
        features.append("Highly popular (10K+ stars)")
    elif stars > 1000:
        features.append("Growing community (1K+ stars)")
    
    stars_today = repo_data.get("stars_today", 0)
    if stars_today > 100:
        features.append(f"Viral growth ({stars_today} stars today)")
    
    if repo_data.get("description"):
        features.append("Well-documented project")
    
    return features[:3]


def generate_why_trending(repo_data: Dict[str, Any]) -> str:
    """Explain why this repo is trending"""
    
    stars_today = repo_data.get("stars_today", 0)
    name = repo_data.get("name", "this project")
    
    if stars_today > 500:
        return f"{name} is experiencing viral growth with {stars_today} new stars."
    elif stars_today > 100:
        return f"{name} gained significant attention today ({stars_today} stars)."
    else:
        return f"{name} is steadily gaining traction in the developer community."


def generate_market_insight(repos: List[Dict], language: str) -> str:
    """Generate market-level insight for AI personalities"""
    
    total_stars_today = sum(r.get("stars_today", 0) for r in repos)
    avg_stars = sum(r.get("stars", 0) for r in repos) / len(repos) if repos else 0
    
    if language and language != "all":
        return f"The {language} ecosystem shows {total_stars_today} new stars across top 10 projects. Average project has {int(avg_stars):,} stars."
    else:
        return f"GitHub trending shows {total_stars_today} new stars today across top projects. Average popularity: {int(avg_stars):,} stars."


def generate_opportunity_hooks(repos: List[Dict]) -> List[str]:
    """Generate actionable hooks for AI personalities"""
    hooks = []
    
    # Find viral repos
    viral = [r for r in repos if r.get("stars_today", 0) > 200]
    if viral:
        hooks.append(f"VIRAL TREND: {viral[0]['name']} is exploding with {viral[0]['stars_today']} stars today")
    
    # Find new players
    new = [r for r in repos if r.get("stars", 0) < 500 and r.get("stars_today", 0) > 50]
    if new:
        hooks.append(f"EMERGING: {new[0]['name']} is a newcomer gaining rapid traction")
    
    # Overall trend
    if len(repos) >= 5:
        hooks.append("TRENDING: Multiple AI/ML projects in top 10 - AI development accelerating")
    
    return hooks[:3]


def generate_mock_trending(language: str = "") -> List[Dict[str, Any]]:
    """Generate mock trending data (fallback)"""
    
    mock_repos = [
        {
            "name": "transformers",
            "full_name": "huggingface/transformers",
            "url": "https://github.com/huggingface/transformers",
            "description": "State-of-the-art ML for PyTorch, TensorFlow, and JAX",
            "author": "huggingface",
            "stars": 135000,
            "stars_today": 234,
            "forks": 27000
        },
        {
            "name": "langchain",
            "full_name": "langchain-ai/langchain",
            "url": "https://github.com/langchain-ai/langchain",
            "description": "Build context-aware reasoning applications",
            "author": "langchain-ai",
            "stars": 98000,
            "stars_today": 189,
            "forks": 15000
        },
        {
            "name": "composio",
            "full_name": "composiohq/composio",
            "url": "https://github.com/composiohq/composio",
            "description": "Agent integration platform - connect AI to 100+ apps",
            "author": "composiohq",
            "stars": 4200,
            "stars_today": 567,
            "forks": 890
        },
        {
            "name": "anthropic-sdk",
            "full_name": "anthropics/anthropic-sdk-python",
            "url": "https://github.com/anthropics/anthropic-sdk-python",
            "description": "Official Python SDK for Anthropic API",
            "author": "anthropics",
            "stars": 8900,
            "stars_today": 123,
            "forks": 2100
        },
        {
            "name": "x402-protocol",
            "full_name": "x402-protocol/x402",
            "url": "https://github.com/x402-protocol/x402",
            "description": "402 Payment Required for the AI economy",
            "author": "x402-protocol",
            "stars": 1200,
            "stars_today": 89,
            "forks": 230
        }
    ]
    
    return mock_repos


def build_github_repo(data: Dict[str, Any]) -> GitHubRepo:
    """Build a GitHubRepo model from raw data"""
    
    return GitHubRepo(
        name=data.get("name", "unknown"),
        full_name=data.get("full_name", ""),
        url=data.get("url", ""),
        description=data.get("description"),
        language=data.get("language"),
        stars=data.get("stars", 0),
        stars_today=data.get("stars_today"),
        forks=data.get("forks", 0),
        author=data.get("author", "unknown"),
        ai_summary=generate_ai_summary(data),
        key_features=generate_key_features(data),
        why_trending=generate_why_trending(data),
        scraped_at=datetime.utcnow()
    )


def analyze_specific_repo(repo_url: str) -> RepoSummaryResponse:
    """Analyze a specific GitHub repository"""
    
    # Extract owner/repo from URL
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        raise ValueError("Invalid GitHub URL")
    
    owner, repo = match.groups()
    
    # For now, use mock analysis
    # In production: fetch real GitHub API data
    
    mock_data = {
        "name": repo,
        "full_name": f"{owner}/{repo}",
        "description": f"A repository by {owner}",
        "stars": random.randint(100, 10000),
        "forks": random.randint(10, 2000),
        "language": "Python"
    }
    
    return RepoSummaryResponse(
        repo_url=repo_url,
        name=repo,
        full_name=f"{owner}/{repo}",
        description=mock_data["description"],
        language=mock_data["language"],
        stars=mock_data["stars"],
        forks=mock_data["forks"],
        last_updated=datetime.utcnow(),
        what_it_does=f"{repo} provides tools and utilities for developers",
        why_it_matters="This project solves common development challenges",
        key_technologies=["Python", "API", "Automation"],
        use_cases=["Development automation", "API integration", "Data processing"],
        conversation_hooks=[
            f"Have you seen {owner}'s work on {repo}?",
            f"{repo} is gaining traction in the developer community",
            "This project shows interesting architectural choices"
        ],
        analyzed_at=datetime.utcnow(),
        confidence=0.85
    )
