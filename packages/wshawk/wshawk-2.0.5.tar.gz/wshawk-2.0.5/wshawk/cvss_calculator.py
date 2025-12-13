#!/usr/bin/env python3
"""
CVSS Scoring Calculator for WSHawk
Calculates CVSS v3.1 scores for vulnerabilities
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict

class CVSSMetric(Enum):
    """CVSS v3.1 Metrics"""
    # Attack Vector
    NETWORK = ("AV:N", 0.85)
    ADJACENT = ("AV:A", 0.62)
    LOCAL = ("AV:L", 0.55)
    PHYSICAL = ("AV:P", 0.2)
    
    # Attack Complexity
    LOW = ("AC:L", 0.77)
    HIGH = ("AC:H", 0.44)
    
    # Privileges Required
    NONE = ("PR:N", 0.85)
    LOW_PRIV = ("PR:L", 0.62)
    HIGH_PRIV = ("PR:H", 0.27)
    
    # User Interaction
    NO_INTERACTION = ("UI:N", 0.85)
    REQUIRED = ("UI:R", 0.62)
    
    # Impact
    HIGH_IMPACT = ("I:H", 0.56)
    LOW_IMPACT = ("I:L", 0.22)
    NONE_IMPACT = ("I:N", 0.0)

@dataclass
class CVSSScore:
    """CVSS Score result"""
    base_score: float
    severity: str  # None, Low, Medium, High, Critical
    vector_string: str
    breakdown: Dict[str, str]

class CVSSCalculator:
    """
    Calculate CVSS v3.1 scores for vulnerabilities
    Simplified for WebSocket vulnerabilities
    """
    
    def calculate_for_vulnerability(self, vuln_type: str, confidence: str) -> CVSSScore:
        """
        Calculate CVSS score based on vulnerability type and confidence
        
        Args:
            vuln_type: Type of vulnerability (XSS, SQLi, etc.)
            confidence: Confidence level (CRITICAL, HIGH, MEDIUM, LOW)
            
        Returns:
            CVSSScore object
        """
        # Base metrics based on vulnerability type
        metrics = self._get_base_metrics(vuln_type, confidence)
        
        # Calculate base score
        base_score = self._calculate_base_score(metrics)
        
        # Determine severity
        severity = self._get_severity(base_score)
        
        # Build vector string
        vector = self._build_vector_string(metrics)
        
        return CVSSScore(
            base_score=round(base_score, 1),
            severity=severity,
            vector_string=vector,
            breakdown=metrics
        )
    
    def _get_base_metrics(self, vuln_type: str, confidence: str) -> Dict[str, str]:
        """Get base CVSS metrics for vulnerability type"""
        
        # Default metrics
        metrics = {
            'AV': 'N',  # Network (WebSocket is network-based)
            'AC': 'L',  # Low complexity
            'PR': 'N',  # No privileges required
            'UI': 'N',  # No user interaction
            'S': 'U',   # Unchanged scope
            'C': 'N',   # Confidentiality impact
            'I': 'N',   # Integrity impact
            'A': 'N'    # Availability impact
        }
        
        vuln_lower = vuln_type.lower()
        
        # SQL Injection
        if 'sql' in vuln_lower:
            metrics['C'] = 'H'  # High confidentiality impact
            metrics['I'] = 'H'  # High integrity impact
            metrics['A'] = 'H'  # High availability impact
            if confidence == 'CRITICAL':
                metrics['AC'] = 'L'
            else:
                metrics['AC'] = 'H'
        
        # XSS
        elif 'xss' in vuln_lower or 'cross-site' in vuln_lower:
            metrics['C'] = 'L'  # Low confidentiality
            metrics['I'] = 'L'  # Low integrity
            metrics['UI'] = 'R' # Requires user interaction
            if 'browser_verified' in vuln_type or confidence == 'CRITICAL':
                metrics['C'] = 'H'
                metrics['I'] = 'H'
        
        # Command Injection
        elif 'command' in vuln_lower:
            metrics['C'] = 'H'
            metrics['I'] = 'H'
            metrics['A'] = 'H'
        
        # XXE
        elif 'xxe' in vuln_lower or 'xml' in vuln_lower:
            metrics['C'] = 'H'
            metrics['I'] = 'L'
            metrics['A'] = 'L'
        
        # SSRF
        elif 'ssrf' in vuln_lower:
            metrics['C'] = 'H'
            metrics['I'] = 'L'
            metrics['A'] = 'L'
        
        # Path Traversal
        elif 'path' in vuln_lower or 'traversal' in vuln_lower:
            metrics['C'] = 'H'
            metrics['I'] = 'N'
            metrics['A'] = 'N'
        
        # NoSQL Injection
        elif 'nosql' in vuln_lower:
            metrics['C'] = 'H'
            metrics['I'] = 'H'
            metrics['A'] = 'L'
        
        return metrics
    
    def _calculate_base_score(self, metrics: Dict[str, str]) -> float:
        """
        Calculate CVSS base score
        Simplified calculation based on CVSS v3.1 formula
        """
        # Impact Sub Score (ISS)
        impact_values = {
            'H': 0.56,
            'L': 0.22,
            'N': 0.0
        }
        
        iss_base = 1 - (
            (1 - impact_values[metrics['C']]) *
            (1 - impact_values[metrics['I']]) *
            (1 - impact_values[metrics['A']])
        )
        
        # Scope unchanged
        impact = 6.42 * iss_base
        
        # Exploitability
        av_values = {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.2}
        ac_values = {'L': 0.77, 'H': 0.44}
        pr_values = {'N': 0.85, 'L': 0.62, 'H': 0.27}
        ui_values = {'N': 0.85, 'R': 0.62}
        
        exploitability = (
            8.22 *
            av_values[metrics['AV']] *
            ac_values[metrics['AC']] *
            pr_values[metrics['PR']] *
            ui_values[metrics['UI']]
        )
        
        # Base Score
        if impact <= 0:
            return 0.0
        
        base_score = min(impact + exploitability, 10.0)
        
        # Round up
        return round(base_score * 10) / 10
    
    def _get_severity(self, score: float) -> str:
        """Get severity rating from score"""
        if score == 0.0:
            return "None"
        elif score < 4.0:
            return "Low"
        elif score < 7.0:
            return "Medium"
        elif score < 9.0:
            return "High"
        else:
            return "Critical"
    
    def _build_vector_string(self, metrics: Dict[str, str]) -> str:
        """Build CVSS vector string"""
        return f"CVSS:3.1/AV:{metrics['AV']}/AC:{metrics['AC']}/PR:{metrics['PR']}/UI:{metrics['UI']}/S:{metrics['S']}/C:{metrics['C']}/I:{metrics['I']}/A:{metrics['A']}"


# Test the calculator
if __name__ == "__main__":
    calc = CVSSCalculator()
    
    print("=" * 70)
    print("CVSS Score Calculator Test")
    print("=" * 70)
    
    test_vulns = [
        ("SQL Injection", "HIGH"),
        ("Cross-Site Scripting (XSS)", "MEDIUM"),
        ("Command Injection", "CRITICAL"),
        ("XXE", "HIGH"),
        ("SSRF", "MEDIUM"),
        ("Path Traversal", "LOW")
    ]
    
    for vuln_type, confidence in test_vulns:
        score = calc.calculate_for_vulnerability(vuln_type, confidence)
        print(f"\n{vuln_type} ({confidence}):")
        print(f"  Score: {score.base_score} ({score.severity})")
        print(f"  Vector: {score.vector_string}")
    
    print("\n[SUCCESS] CVSS Calculator working!")
