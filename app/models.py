"""
Virtuals Intelligence API - Pydantic Models
Service for AI personalities (Virtuals Protocol)
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TrendingLanguage(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUST = "rust"
    GO = "go"
    AI = "ai"  # AI/ML projects specifically
    ALL = "all"


class TimeRange(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class GitHubRepo(BaseModel):
    """A trending GitHub repository"""
    name: str
    full_name: str
    url: str
    description: Optional[str] = None
    language: Optional[str] = None
    stars: int
    stars_today: Optional[int] = None
    forks: int
    author: str
    
    # AI-enhanced summary
    ai_summary: str = Field(..., description="Brief summary for AI personalities")
    key_features: List[str] = Field(default_factory=list)
    why_trending: Optional[str] = None
    
    # Metadata
    scraped_at: datetime


class TrendingResponse(BaseModel):
    """Response for trending repos"""
    language: str
    time_range: str
    repos: List[GitHubRepo]
    
    # Intelligence layer
    market_insight: str = Field(..., description="What this trend means for AI agents")
    opportunity_hooks: List[str] = Field(default_factory=list, description="Actionable insights")
    
    # Metadata
    count: int
    scraped_at: datetime
    cache_hit: bool


class RepoSummaryRequest(BaseModel):
    """Request to summarize a specific repo"""
    repo_url: str
    focus: Optional[str] = Field(default="general", description="What to focus summary on")


class RepoSummaryResponse(BaseModel):
    """Detailed repo analysis"""
    repo_url: str
    name: str
    full_name: str
    
    # Core info
    description: str
    language: str
    stars: int
    forks: int
    last_updated: datetime
    
    # Intelligence layer
    what_it_does: str
    why_it_matters: str
    key_technologies: List[str]
    use_cases: List[str]
    
    # For AI personalities
    conversation_hooks: List[str] = Field(..., description="Topics an AI can discuss")
    
    # Metadata
    analyzed_at: datetime
    confidence: float = Field(..., ge=0, le=1)


class DiscoveryResponse(BaseModel):
    """Service discovery (FREE)"""
    service: str = "Virtuals Intelligence API"
    version: str = "1.0.0"
    description: str = "GitHub trending intelligence for AI personalities"
    pricing: Dict[str, str] = {"per_request": "$0.05"}
    languages_supported: List[str]
    x402: Dict[str, Any]


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    code: str
