"""WAF detection with proper types"""
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class WAFInfo:
    """WAF detection information"""
    name: str
    confidence: float
    recommended_strategy: str

class WAFDetector:
    """Detects WAFs from responses"""
    
    def __init__(self):
        self.detected_waf: Optional[str] = None
        self.confidence: float = 0.0
    
    def detect(self, headers: Dict[str, str], body: str) -> Optional[WAFInfo]:
        """
        Detect WAF from response
        
        Args:
            headers: Response headers
            body: Response body
            
        Returns:
            WAFInfo if detected
        """
        headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
        body_lower = body.lower()
        
        # Cloudflare
        if 'cf-ray' in headers_lower or 'cloudflare' in body_lower:
            return WAFInfo(name="Cloudflare", confidence=1.0, recommended_strategy="encoding")
        
        # Akamai
        if 'akamai' in str(headers_lower) or 'akamai' in body_lower:
            return WAFInfo(name="Akamai", confidence=0.9, recommended_strategy="tag_break")
        
        # Imperva
        if 'imperva' in body_lower or 'incapsula' in body_lower:
            return WAFInfo(name="Imperva", confidence=0.95, recommended_strategy="polyglot")
        
        # ModSecurity
        if 'mod_security' in body_lower or 'modsec' in body_lower:
            return WAFInfo(name="ModSecurity", confidence=0.85, recommended_strategy="comment")
        
        return None

__all__ = ['WAFDetector', 'WAFInfo']
