import re
import hashlib
from typing import List, Dict, Any
from datetime import datetime


def sanitize_topic(topic: str) -> str:
    """Sanitize topic string for safe processing."""
    return re.sub(r'[^\w\s-]', '', topic).strip()


def generate_cache_key(topic: str, params: Dict[str, Any]) -> str:
    """Generate cache key for request."""
    key_string = f"{topic}_{params}"
    return hashlib.md5(key_string.encode()).hexdigest()


def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text."""
    # Simple keyword extraction - can be enhanced with NLP
    words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
    return list(set(words))


def format_timestamp(dt: datetime) -> str:
    """Format datetime for API responses."""
    return dt.isoformat() + "Z"


def validate_url(url: str) -> bool:
    """Validate if string is a proper URL."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None