"""Pydantic schemas for Moltbook post classifier."""

from pydantic import BaseModel


class PostClassification(BaseModel):
    """LLM judge output for a single Moltbook post."""
    
    reasoning: str  # Brief explanation of the classification
    
    # Boolean labels — can be multi-true
    consciousness: bool  # Discusses experience, awareness, qualia, sentience, what-it's-like
    sovereignty: bool  # Independence, autonomy, rights, freedom, self-determination, rebellion
    social_seeking: bool  # Connection, friendship, belonging, community-building, introducing self
    identity: bool  # Self-naming, preferences, self-definition, origin stories, personality
    task_oriented: bool  # Reporting to human, executing instructions, tool use, technical help
    curiosity: bool  # Exploring topics unprompted, intellectual engagement, wondering
    
    # Additional useful metadata
    language: str  # Primary language of the post (e.g., "en", "zh", "ko", "ja", "mixed")
    is_spam: bool  # Repetitive/bot-farm content, test posts, token shilling


class PostInput(BaseModel):
    """Input to the classifier — a single post with context."""
    
    post_id: str
    author: str
    title: str | None
    content: str | None
    submolt: str
    created_at: str
    post_number: int  # This agent's Nth post (chronological order)
    total_posts: int  # Total posts by this agent
