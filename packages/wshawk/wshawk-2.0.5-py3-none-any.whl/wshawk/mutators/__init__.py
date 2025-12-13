"""Mutator registry and factory"""
from typing import List
from .base import BaseMutator, MutatorConfig
from .encoding import EncodingMutator
from .comments import CommentMutator
from .tag_break import TagBreakMutator
from .polyglot import PolyglotMutator

def create_default_mutators(config: MutatorConfig = None) -> List[BaseMutator]:
    """
    Create default set of mutators
    
    Args:
        config: Optional configuration
        
    Returns:
        List of mutator instances
    """
    config = config or MutatorConfig()
    mutators = []
    
    if config.enable_polyglots:
        mutators.append(PolyglotMutator(config))
    
    if config.enable_encoding:
        mutators.append(EncodingMutator(config))
    
    if config.enable_comments:
        mutators.append(CommentMutator(config))
    
    if config.enable_tag_break:
        mutators.append(TagBreakMutator(config))
    
    return mutators

__all__ = [
    'BaseMutator',
    'MutatorConfig',
    'PayloadContext',
    'MutatorResult',
    'create_default_mutators'
]
