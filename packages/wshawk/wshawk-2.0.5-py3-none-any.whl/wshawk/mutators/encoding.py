"""Encoding mutator with proper interface"""
import base64
from typing import List
from .base import BaseMutator, MutatorResult, PayloadContext, MutatorConfig

class EncodingMutator(BaseMutator):
    """Advanced encoding mutations"""
    
    def get_name(self) -> str:
        return "encoding"
    
    def mutate(self, payload: str, context: PayloadContext) -> MutatorResult:
        variants = []
        max_count = self.config.max_variants_per_mutator
        
        # URL encoding
        variants.append(''.join(f'%{ord(c):02x}' for c in payload))
        
        # Double URL encoding
        variants.append(''.join(f'%25{ord(c):02x}' for c in payload))
        
        # HTML entity (decimal)
        variants.append(''.join(f'&#{ord(c)};' for c in payload))
        
        # HTML entity (hex)
        variants.append(''.join(f'&#x{ord(c):x};' for c in payload))
        
        # Unicode
        variants.append(''.join(f'\\u{ord(c):04x}' for c in payload))
        
        # Base64
        variants.append(base64.b64encode(payload.encode()).decode())
        
        return MutatorResult(
            strategy_name=self.get_name(),
            variants=variants[:max_count],
            confidence=1.0
        )
