"""Comment mutator with proper interface"""
from typing import List
from .base import BaseMutator, MutatorResult, PayloadContext, MutatorConfig

class CommentMutator(BaseMutator):
    """Comment injection mutations"""
    
    def get_name(self) -> str:
        return "comment"
    
    def supports_context(self, context: PayloadContext) -> bool:
        # Comments work best for SQL and command injection
        return context in [PayloadContext.SQLI, PayloadContext.CMDI, PayloadContext.GENERIC]
    
    def mutate(self, payload: str, context: PayloadContext) -> MutatorResult:
        variants = []
        max_count = self.config.max_variants_per_mutator
        
        # SQL comments
        variants.append(payload.replace(' ', '/**/'))
        variants.append(payload.replace(' ', '--\n'))
        variants.append(payload.replace('=', '/**/=/**/'))
        variants.append(payload.replace('OR', '/**/OR/**/'))
        variants.append(payload.replace('AND', '/**/AND/**/'))
        
        # MySQL specific
        variants.append(payload.replace(' ', '/*!*/'))
        
        return MutatorResult(
            strategy_name=self.get_name(),
            variants=variants[:max_count],
            confidence=0.9
        )
