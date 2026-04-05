"""
Virtuals Intelligence API - X (Twitter) Bot
Posts trending repo insights to X
"""

import os
import tweepy
from typing import Dict, Any, Optional
from datetime import datetime


# X API Credentials (from environment)
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN")
X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY") or os.getenv("TWITTER_CONSUMER_KEY")
X_CONSUMER_SECRET = os.getenv("X_CONSUMER_SECRET") or os.getenv("TWITTER_CONSUMER_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN") or os.getenv("TWITTER_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET") or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


class XBot:
    """X (Twitter) bot for posting trending insights"""
    
    def __init__(self):
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Initialize X API client"""
        if not all([X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
            print("X credentials not fully configured")
            return
        
        try:
            self.client = tweepy.Client(
                bearer_token=X_BEARER_TOKEN,
                consumer_key=X_CONSUMER_KEY,
                consumer_secret=X_CONSUMER_SECRET,
                access_token=X_ACCESS_TOKEN,
                access_token_secret=X_ACCESS_TOKEN_SECRET
            )
            print("X bot initialized")
        except Exception as e:
            print(f"X bot init failed: {e}")
    
    def is_ready(self) -> bool:
        return self.client is not None
    
    async def post_trending_insight(self, repo_data: Dict[str, Any], intelligence: Dict[str, Any]) -> Optional[str]:
        if not self.is_ready():
            return None
        
        try:
            name = repo_data.get("name", "this repo")
            stars_today = repo_data.get("stars_today", 0)
            trending_score = intelligence.get("trending_score", 50)
            why = intelligence.get("why_trending", "gaining traction")
            url = repo_data.get("url", "")
            
            if trending_score >= 80:
                emoji = "fire"
            elif trending_score >= 60:
                emoji = "chart"
            else:
                emoji = "eyes"
            
            tweet_text = f"{emoji} {name}\n\n{why}\n\n+{stars_today} stars today | Score: {trending_score}/100\n\n{url}\n\n#GitHub #AI #Trending"
            
            if len(tweet_text) > 280:
                tweet_text = tweet_text[:277] + "..."
            
            response = self.client.create_tweet(text=tweet_text)
            
            if response.data:
                tweet_id = response.data["id"]
                return f"https://x.com/VirtualsIntel/status/{tweet_id}"
            return None
                
        except Exception as e:
            print(f"Post failed: {e}")
            return None


_bot: Optional[XBot] = None


def get_bot() -> XBot:
    global _bot
    if _bot is None:
        _bot = XBot()
    return _bot
