"""Tag breaking mutator with proper interface"""
from typing import List
from .base import BaseMutator, MutatorResult, PayloadContext, MutatorConfig

class TagBreakMutator(BaseMutator):
    """Tag breaking for XSS bypass"""
    
    def get_name(self) -> str:
        return "tag_break"
    
    def supports_context(self, context: PayloadContext) -> bool:
        # Only for XSS
        return context in [PayloadContext.XSS, PayloadContext.GENERIC]
    
    def mutate(self, payload: str, context: PayloadContext) -> MutatorResult:
        variants = []
        max_count = self.config.max_variants_per_mutator
        
        if '<' not in payload:
            return MutatorResult(strategy_name=self.get_name(), variants=[], confidence=0.0)
        
        # Split tags
        variants.append(payload.replace('<script', '<scr<script>ipt'))
        variants.append(payload.replace('<img', '<i<img>mg'))
        variants.append(payload.replace('<svg', '<s<svg>vg'))
        
        # Encode opening bracket
        variants.append(payload.replace('<', '%3c'))
        variants.append(payload.replace('<', '&lt;'))
        
        # Break event handlers
        variants.append(payload.replace('on', 'o\x00n'))
        
        return MutatorResult(
            strategy_name=self.get_name(),
            variants=variants[:max_count],
            confidence=0.95
        )
