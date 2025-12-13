#!/usr/bin/env python3
"""
WSHawk Production Payload Mutation Engine V3
Clean API with proper types and modular architecture
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

from .mutators import create_default_mutators
from .mutators.base import BaseMutator, MutatorConfig, PayloadContext, MutatorResult
from .waf.detector import WAFDetector, WAFInfo


@dataclass
class MutationReport:
    """Complete mutation report"""
    base_payload: str
    context: PayloadContext
    waf: Optional[WAFInfo]
    variants: List[str]
    by_strategy: Dict[str, List[str]]


class PayloadMutationEngineV3:
    """
    High-level orchestrator for payload mutation.
    
    Features:
    - WAF detection
    - Modular mutators
    - Clean API
    - Context-aware mutations
    """
    
    def __init__(self, mutator_config: Optional[MutatorConfig] = None):
        self.mutators: List[BaseMutator] = create_default_mutators(mutator_config)
        self.waf_detector = WAFDetector()
    
    def _detect_waf(self, response_headers: Optional[Dict[str, str]], 
                    response_body: Optional[str]) -> Optional[WAFInfo]:
        """Detect WAF from response"""
        return self.waf_detector.detect(response_headers or {}, response_body or "")
    
    def generate(
        self,
        base_payload: str,
        context: str = "generic",
        max_total: int = 15,
        response_headers: Optional[Dict[str, str]] = None,
        response_body: Optional[str] = None,
    ) -> MutationReport:
        """
        Main API for WSHawk.
        
        Args:
            base_payload: Original payload
            context: "xss", "sqli", "cmdi", etc.
            max_total: Max total variants
            response_headers: Optional - for WAF detection
            response_body: Optional - for WAF detection
            
        Returns:
            MutationReport with all variants grouped by strategy
        """
        # Parse context
        try:
            ctx_enum = PayloadContext(context)
        except ValueError:
            ctx_enum = PayloadContext.GENERIC
        
        # Detect WAF
        waf_info = self._detect_waf(response_headers, response_body)
        
        # Generate mutations
        all_variants: List[str] = [base_payload]
        by_strategy: Dict[str, List[str]] = {}
        
        for mutator in self.mutators:
            if not mutator.supports_context(ctx_enum):
                continue
            
            result: MutatorResult = mutator.mutate(base_payload, ctx_enum)
            if not result.variants:
                continue
            
            by_strategy.setdefault(result.strategy_name, [])
            for v in result.variants:
                if v not in all_variants:
                    all_variants.append(v)
                    by_strategy[result.strategy_name].append(v)
                if len(all_variants) >= max_total:
                    break
            
            if len(all_variants) >= max_total:
                break
        
        return MutationReport(
            base_payload=base_payload,
            context=ctx_enum,
            waf=waf_info,
            variants=all_variants[:max_total],
            by_strategy=by_strategy,
        )


# Test the production engine
if __name__ == "__main__":
    print("=" * 70)
    print("WSHawk Production Payload Mutation Engine V3")
    print("=" * 70)
    
    engine = PayloadMutationEngineV3()
    
    # Test 1: XSS mutations
    print("\n1. XSS Mutations:")
    report = engine.generate("<script>alert(1)</script>", context="xss", max_total=10)
    
    print(f"  Base: {report.base_payload}")
    print(f"  Context: {report.context.value}")
    print(f"  Total variants: {len(report.variants)}")
    print(f"\n  By strategy:")
    for strategy, variants in report.by_strategy.items():
        print(f"    [{strategy}] {len(variants)} variants")
        for v in variants[:2]:
            print(f"      {v[:60]}")
    
    # Test 2: SQL mutations
    print("\n2. SQL Mutations:")
    report = engine.generate("' OR 1=1--", context="sqli", max_total=10)
    
    print(f"  Total variants: {len(report.variants)}")
    for strategy, variants in report.by_strategy.items():
        print(f"    [{strategy}]")
        for v in variants[:3]:
            print(f"      {v}")
    
    # Test 3: WAF detection
    print("\n3. WAF Detection:")
    report = engine.generate(
        "test",
        context="xss",
        response_headers={'cf-ray': '12345'},
        response_body="Cloudflare blocked"
    )
    
    if report.waf:
        print(f"  WAF: {report.waf.name}")
        print(f"  Confidence: {report.waf.confidence}")
        print(f"  Recommended: {report.waf.recommended_strategy}")
    
    print("\n[SUCCESS] Production Engine V3 working!")
