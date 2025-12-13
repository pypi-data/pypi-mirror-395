"""Base mutator interface with proper types"""
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
from enum import Enum

class PayloadContext(Enum):
    """Payload context types"""
    GENERIC = "generic"
    XSS = "xss"
    SQLI = "sqli"
    CMDI = "cmdi"
    XXE = "xxe"
    SSRF = "ssrf"

@dataclass
class MutatorConfig:
    """Configuration for mutators"""
    max_variants_per_mutator: int = 5
    enable_encoding: bool = True
    enable_comments: bool = True
    enable_tag_break: bool = True
    enable_polyglots: bool = True

@dataclass
class MutatorResult:
    """Result from a mutator"""
    strategy_name: str
    variants: List[str]
    confidence: float = 1.0

class BaseMutator(ABC):
    """Base class for all mutators"""
    
    def __init__(self, config: MutatorConfig = None):
        self.config = config or MutatorConfig()
    
    @abstractmethod
    def mutate(self, payload: str, context: PayloadContext) -> MutatorResult:
        """Generate mutations of the payload"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return mutator name"""
        pass
    
    def supports_context(self, context: PayloadContext) -> bool:
        """Check if mutator supports this context"""
        return True  # Default: support all contexts
