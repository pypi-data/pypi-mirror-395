#!/usr/bin/env python3
"""
WSHawk Server Fingerprinting Module
Detects backend technology, framework, and database
"""

import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass

@dataclass
class ServerFingerprint:
    """Server fingerprint information"""
    language: Optional[str] = None
    framework: Optional[str] = None
    database: Optional[str] = None
    libraries: List[str] = None
    confidence: float = 0.0
    
    def __post_init__(self):
        if self.libraries is None:
            self.libraries = []

class ServerFingerprinter:
    """
    Fingerprint backend technology from WebSocket responses
    """
    
    # Language signatures
    LANGUAGE_SIGNATURES = {
        'python': [
            r'Traceback \(most recent call last\)',
            r'File ".*\.py", line',
            r'django',
            r'flask',
            r'tornado',
            r'aiohttp',
        ],
        'nodejs': [
            r'at .*\(.*\.js:\d+:\d+\)',
            r'Error: .*\n\s+at',
            r'express',
            r'socket\.io',
            r'ws\.WebSocket',
        ],
        'java': [
            r'at .*\(.*\.java:\d+\)',
            r'Exception in thread',
            r'java\.',
            r'javax\.',
            r'springframework',
        ],
        'php': [
            r'Fatal error:',
            r'Warning:.*in /.*\.php',
            r'Notice:.*in /.*\.php',
            r'Parse error:',
        ],
        'ruby': [
            r'\.rb:\d+:in',
            r'from .*\.rb:\d+',
            r'ActionController',
            r'ActiveRecord',
        ],
        'go': [
            r'goroutine \d+',
            r'panic:',
            r'runtime\.',
            r'\.go:\d+',
        ],
        'csharp': [
            r'at .*\.cs:line \d+',
            r'System\.',
            r'Microsoft\.',
            r'\.NET',
        ],
    }
    
    # Framework signatures
    FRAMEWORK_SIGNATURES = {
        'express': [r'express', r'X-Powered-By: Express'],
        'socket.io': [r'socket\.io', r'"sid":', r'"upgrades":\["websocket"\]'],
        'django': [r'django', r'csrftoken', r'sessionid'],
        'flask': [r'flask', r'Werkzeug'],
        'spring': [r'springframework', r'spring'],
        'rails': [r'ActionController', r'ActiveRecord'],
        'sockjs': [r'sockjs', r'"websocket":true'],
        'tornado': [r'tornado'],
        'fastapi': [r'fastapi', r'starlette'],
    }
    
    # Database signatures
    DATABASE_SIGNATURES = {
        'mysql': [
            r'mysql',
            r'You have an error in your SQL syntax.*MySQL',
            r'MySQLSyntaxErrorException',
        ],
        'postgresql': [
            r'postgresql',
            r'PostgreSQL.*ERROR',
            r'pg_',
            r'psycopg',
        ],
        'mongodb': [
            r'mongodb',
            r'MongoError',
            r'bson',
            r'"_id":{"$oid"',
        ],
        'redis': [
            r'redis',
            r'WRONGTYPE',
            r'ERR unknown command',
        ],
        'mssql': [
            r'SQL Server',
            r'Microsoft SQL',
            r'mssql',
        ],
        'oracle': [
            r'ORA-\d+',
            r'Oracle',
            r'OracleDriver',
        ],
        'sqlite': [
            r'sqlite',
            r'SQLite',
        ],
    }
    
    def __init__(self):
        self.responses = []
        self.detected_language = None
        self.detected_framework = None
        self.detected_database = None
        self.confidence_scores = {}
    
    def add_response(self, response: str):
        """Add response for analysis"""
        self.responses.append(response)
    
    def fingerprint(self) -> ServerFingerprint:
        """
        Perform fingerprinting based on collected responses
        """
        all_text = '\n'.join(self.responses)
        
        # Detect language
        language_scores = self._score_signatures(all_text, self.LANGUAGE_SIGNATURES)
        detected_language = max(language_scores, key=language_scores.get) if language_scores else None
        
        # Detect framework
        framework_scores = self._score_signatures(all_text, self.FRAMEWORK_SIGNATURES)
        detected_framework = max(framework_scores, key=framework_scores.get) if framework_scores else None
        
        # Detect database
        database_scores = self._score_signatures(all_text, self.DATABASE_SIGNATURES)
        detected_database = max(database_scores, key=database_scores.get) if database_scores else None
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(
            language_scores, framework_scores, database_scores
        )
        
        # Detect libraries
        libraries = self._detect_libraries(all_text)
        
        return ServerFingerprint(
            language=detected_language,
            framework=detected_framework,
            database=detected_database,
            libraries=libraries,
            confidence=confidence
        )
    
    def _score_signatures(self, text: str, signatures: Dict[str, List[str]]) -> Dict[str, int]:
        """
        Score each technology based on signature matches
        """
        scores = {}
        
        for tech, patterns in signatures.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1
            
            if score > 0:
                scores[tech] = score
        
        return scores
    
    def _calculate_confidence(self, *score_dicts) -> float:
        """
        Calculate overall confidence based on multiple score dictionaries
        """
        total_matches = sum(sum(scores.values()) for scores in score_dicts)
        max_possible = sum(len(d) for d in score_dicts)
        
        if max_possible == 0:
            return 0.0
        
        return min(total_matches / max_possible, 1.0)
    
    def _detect_libraries(self, text: str) -> List[str]:
        """
        Detect specific libraries mentioned in responses
        """
        library_patterns = {
            'express': r'express',
            'socket.io': r'socket\.io',
            'django': r'django',
            'flask': r'flask',
            'spring': r'spring',
            'hibernate': r'hibernate',
            'mongoose': r'mongoose',
            'sequelize': r'sequelize',
            'sqlalchemy': r'sqlalchemy',
            'prisma': r'prisma',
        }
        
        detected = []
        for lib, pattern in library_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(lib)
        
        return detected
    
    def get_recommended_payloads(self, fingerprint: ServerFingerprint) -> Dict[str, List[str]]:
        """
        Recommend payload types based on fingerprint
        """
        recommendations = {
            'sql': [],
            'nosql': [],
            'command': [],
            'template': [],
        }
        
        # SQL payloads based on database
        if fingerprint.database:
            db_payloads = {
                'mysql': ['SLEEP(5)', 'BENCHMARK()', "' OR '1'='1"],
                'postgresql': ['pg_sleep(5)', "'; --", "' OR 1=1 --"],
                'mssql': ["WAITFOR DELAY '00:00:05'", "'; EXEC xp_cmdshell"],
                'mongodb': ['{"$ne": null}', '{"$gt": ""}'],
            }
            recommendations['sql'] = db_payloads.get(fingerprint.database, [])
        
        # NoSQL payloads
        if fingerprint.database in ['mongodb', 'redis']:
            recommendations['nosql'] = [
                '{"$ne": null}',
                '{"$gt": ""}',
                '{"$where": "sleep(5000)"}',
            ]
        
        # Command injection based on language
        if fingerprint.language:
            lang_commands = {
                'python': ['__import__("os").system("id")', 'eval()'],
                'nodejs': ['require("child_process").exec("id")', 'eval()'],
                'php': ['system("id")', 'exec("id")', 'shell_exec("id")'],
                'ruby': ['system("id")', '`id`'],
            }
            recommendations['command'] = lang_commands.get(fingerprint.language, [])
        
        # Template injection based on framework
        if fingerprint.framework:
            template_payloads = {
                'flask': ['{{7*7}}', '{{config}}', '{{request}}'],
                'django': ['{{7*7}}', '{% debug %}'],
                'express': ['${7*7}', '#{7*7}'],
            }
            recommendations['template'] = template_payloads.get(fingerprint.framework, [])
        
        return recommendations
    
    def get_info(self) -> Dict:
        """
        Get fingerprinting information
        """
        fingerprint = self.fingerprint()
        
        return {
            'language': fingerprint.language,
            'framework': fingerprint.framework,
            'database': fingerprint.database,
            'libraries': fingerprint.libraries,
            'confidence': f"{fingerprint.confidence * 100:.1f}%",
            'responses_analyzed': len(self.responses),
            'recommended_payloads': self.get_recommended_payloads(fingerprint),
        }
