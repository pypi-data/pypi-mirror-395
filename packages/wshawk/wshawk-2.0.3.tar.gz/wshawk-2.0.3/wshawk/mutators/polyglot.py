"""Polyglot mutator that loads from JSON files"""
import json
import os
from typing import List, Dict
from .base import BaseMutator, MutatorResult, PayloadContext, MutatorConfig

class PolyglotMutator(BaseMutator):
    """Loads polyglot payloads from external JSON files"""
    
    def __init__(self, config: MutatorConfig = None, polyglot_dir: str = "payloads/polyglots"):
        super().__init__(config)
        self.polyglots = self._load_polyglots(polyglot_dir)
    
    def _load_polyglots(self, polyglot_dir: str) -> Dict[str, List[str]]:
        """Load polyglots from JSON files"""
        polyglots = {}
        
        # Try multiple paths
        possible_paths = [
            polyglot_dir,
            os.path.join(os.path.dirname(__file__), '..', '..', polyglot_dir),
            os.path.join('/home/regaan/Desktop/wshawk', polyglot_dir)
        ]
        
        for base_path in possible_paths:
            if os.path.exists(base_path):
                for filename in os.listdir(base_path):
                    if filename.endswith('.json'):
                        filepath = os.path.join(base_path, filename)
                        try:
                            with open(filepath, 'r') as f:
                                data = json.load(f)
                                polyglots.update(data)
                        except Exception as e:
                            print(f"[WARNING] Failed to load {filename}: {e}")
                break
        
        return polyglots
    
    def get_name(self) -> str:
        return "polyglot"
    
    def mutate(self, payload: str, context: PayloadContext) -> MutatorResult:
        """Return polyglots for the given context"""
        context_key = context.value
        
        if context_key in self.polyglots:
            variants = self.polyglots[context_key][:self.config.max_variants_per_mutator]
        else:
            variants = []
        
        return MutatorResult(
            strategy_name=self.get_name(),
            variants=variants,
            confidence=1.0
        )
