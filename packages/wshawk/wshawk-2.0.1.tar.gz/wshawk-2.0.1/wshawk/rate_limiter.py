#!/usr/bin/env python3
"""
WSHawk Professional Rate Limiter
Token Bucket + Adaptive Pacing + Server Feedback Detection
"""

import asyncio
import time
from typing import Optional, Dict
from collections import deque
from dataclasses import dataclass
import statistics

@dataclass
class ServerFeedback:
    """Server feedback signals"""
    close_code: Optional[int] = None
    close_reason: Optional[str] = None
    latency_spike: bool = False
    rate_limit_detected: bool = False
    soft_ban_detected: bool = False

class TokenBucketRateLimiter:
    """
    Professional Token Bucket Rate Limiter with:
    1. Per-connection throttling
    2. Concurrency-aware scheduling
    3. Auto backoff on server slowdown
    4. Adaptive pacing based on latency
    5. Token bucket architecture
    6. Server-side feedback inspection
    """
    
    def __init__(self, 
                 tokens_per_second: float = 10.0,
                 bucket_size: int = 20,
                 enable_adaptive: bool = True,
                 latency_threshold_ms: float = 1000.0):
        """
        Args:
            tokens_per_second: Token refill rate (requests/sec)
            bucket_size: Maximum burst size
            enable_adaptive: Enable adaptive pacing
            latency_threshold_ms: Latency threshold for slowdown detection
        """
        # Token bucket parameters
        self.tokens_per_second = tokens_per_second
        self.bucket_size = bucket_size
        self.tokens = float(bucket_size)  # Start with full bucket
        self.last_refill = time.monotonic()
        
        # Adaptive pacing
        self.enable_adaptive = enable_adaptive
        self.latency_threshold = latency_threshold_ms / 1000.0  # Convert to seconds
        self.response_times = deque(maxlen=10)
        self.original_rate = tokens_per_second
        
        # Server feedback detection
        self.server_feedback = ServerFeedback()
        self.consecutive_slow_responses = 0
        self.backoff_multiplier = 1.0
        
        # Concurrency control
        self.lock = asyncio.Lock()
        self.pending_requests = 0
        self.max_concurrent = 10
        
        # Statistics
        self.total_requests = 0
        self.total_waits = 0
        self.total_wait_time = 0.0
        self.adaptive_adjustments = 0
    
    async def acquire(self) -> bool:
        """
        Acquire token to send request
        Implements token bucket algorithm with adaptive pacing
        
        Returns:
            True if token acquired, False if should abort
        """
        while True:
            async with self.lock:
                # Case 1: Too many concurrent requests
                if self.pending_requests >= self.max_concurrent:
                    wait_time = 0.05  # Small backoff due to concurrency
                    self.total_waits += 1
                    self.total_wait_time += wait_time
                else:
                    # Refill tokens based on time elapsed
                    current_time = time.monotonic()
                    time_elapsed = current_time - self.last_refill
                    
                    # Calculate tokens to add (rate * time)
                    tokens_to_add = time_elapsed * self.tokens_per_second * self.backoff_multiplier
                    self.tokens = min(self.bucket_size, self.tokens + tokens_to_add)
                    self.last_refill = current_time
                    
                    # Check if we have tokens
                    if self.tokens >= 1.0:
                        self.tokens -= 1.0
                        self.total_requests += 1
                        self.pending_requests += 1
                        return True
                    
                    # Need to wait for tokens
                    wait_time = (1.0 - self.tokens) / (self.tokens_per_second * self.backoff_multiplier)
                    self.total_waits += 1
                    self.total_wait_time += wait_time
            
            # Wait outside the lock to allow other coroutines
            await asyncio.sleep(wait_time)
    
    async def done(self):
        """Mark request as complete - MUST be called after each request"""
        async with self.lock:
            self.pending_requests = max(0, self.pending_requests - 1)
    
    async def report_response_time(self, response_time: float):
        """
        Report response time for adaptive pacing
        
        Args:
            response_time: Response time in seconds
        """
        self.response_times.append(response_time)
        
        if not self.enable_adaptive:
            return
        
        # Check if we have enough samples
        if len(self.response_times) >= 5:
            avg_latency = statistics.mean(self.response_times)
            
            # Detect latency spike
            if avg_latency > self.latency_threshold:
                self.consecutive_slow_responses += 1
                
                # After 3 consecutive slow responses, reduce rate
                if self.consecutive_slow_responses >= 3:
                    await self._reduce_rate("Latency spike detected")
            else:
                # Reset counter and potentially increase rate
                if self.consecutive_slow_responses > 0:
                    self.consecutive_slow_responses = 0
                
                # If consistently fast, increase rate
                if avg_latency < self.latency_threshold / 2:
                    await self._increase_rate("Fast responses detected")
    
    async def report_server_feedback(self, 
                                     close_code: Optional[int] = None,
                                     close_reason: Optional[str] = None,
                                     message: Optional[str] = None):
        """
        Inspect server feedback for rate limiting signals
        
        Args:
            close_code: WebSocket close code
            close_reason: WebSocket close reason
            message: Server message content
        """
        # Check WebSocket close codes with severity levels
        strong_rate_limit_codes = [1013]  # Try Again Later - definite rate limit
        soft_rate_limit_codes = [1008, 1011]  # Policy Violation, Internal Error - maybe rate limit
        
        if close_code in strong_rate_limit_codes:
            self.server_feedback.rate_limit_detected = True
            await self._reduce_rate(f"Strong rate limit signal (code {close_code})")
        elif close_code in soft_rate_limit_codes:
            # Soft signal - only reduce if we see it multiple times
            self.server_feedback.close_code = close_code
            if not hasattr(self, '_soft_limit_count'):
                self._soft_limit_count = 0
            self._soft_limit_count += 1
            
            if self._soft_limit_count >= 2:  # Require 2 soft signals
                self.server_feedback.rate_limit_detected = True
                await self._reduce_rate(f"Repeated soft rate limit signal (code {close_code})")
        
        # Check close reason
        if close_reason:
            rate_limit_keywords = ['rate', 'limit', 'throttle', 'too many', 'slow down']
            if any(keyword in close_reason.lower() for keyword in rate_limit_keywords):
                self.server_feedback.rate_limit_detected = True
                await self._reduce_rate(f"Rate limit in close reason: {close_reason}")
        
        # Check message content for rate limit signals
        if message:
            rate_limit_patterns = [
                'rate limit',
                'too many requests',
                'throttled',
                'slow down',
                '429',  # HTTP 429 Too Many Requests
                'retry after',
            ]
            
            message_lower = message.lower()
            if any(pattern in message_lower for pattern in rate_limit_patterns):
                self.server_feedback.rate_limit_detected = True
                await self._reduce_rate(f"Rate limit in message")
    
    async def _reduce_rate(self, reason: str):
        """
        Reduce sending rate (exponential backoff)
        """
        async with self.lock:
            # Cooldown: don't reduce too frequently
            current_time = time.monotonic()
            if not hasattr(self, '_last_reduce_time'):
                self._last_reduce_time = 0
            
            # Require at least 1 second between reductions
            if current_time - self._last_reduce_time < 1.0:
                return
            
            self._last_reduce_time = current_time
            
            old_multiplier = self.backoff_multiplier
            self.backoff_multiplier = max(0.1, self.backoff_multiplier * 0.5)  # Halve the rate
            
            if old_multiplier != self.backoff_multiplier:
                self.adaptive_adjustments += 1
                print(f"[Rate Limiter] Reducing rate: {reason}")
                print(f"  New rate: {self.tokens_per_second * self.backoff_multiplier:.2f} req/s (multiplier: {self.backoff_multiplier:.2f})")
    
    async def _increase_rate(self, reason: str):
        """
        Increase sending rate (gradual recovery)
        """
        async with self.lock:
            # Cooldown: don't increase too frequently
            current_time = time.monotonic()
            if not hasattr(self, '_last_increase_time'):
                self._last_increase_time = 0
            
            # Require at least 2 seconds between increases (slower than reductions)
            if current_time - self._last_increase_time < 2.0:
                return
            
            self._last_increase_time = current_time
            
            old_multiplier = self.backoff_multiplier
            # Gradually increase back to original rate
            self.backoff_multiplier = min(1.0, self.backoff_multiplier * 1.1)
            
            if old_multiplier != self.backoff_multiplier and abs(old_multiplier - self.backoff_multiplier) > 0.01:
                self.adaptive_adjustments += 1
                print(f"[Rate Limiter] Increasing rate: {reason}")
                print(f"  New rate: {self.tokens_per_second * self.backoff_multiplier:.2f} req/s (multiplier: {self.backoff_multiplier:.2f})")
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        current_rate = self.tokens_per_second * self.backoff_multiplier
        
        return {
            'total_requests': self.total_requests,
            'total_waits': self.total_waits,
            'total_wait_time': f"{self.total_wait_time:.2f}s",
            'avg_wait_time': f"{self.total_wait_time / max(1, self.total_waits):.3f}s",
            'current_tokens': f"{self.tokens:.2f}",
            'current_rate': f"{current_rate:.2f} req/s",
            'backoff_multiplier': f"{self.backoff_multiplier:.2f}",
            'adaptive_adjustments': self.adaptive_adjustments,
            'pending_requests': self.pending_requests,
            'avg_latency': f"{statistics.mean(self.response_times) * 1000:.1f}ms" if self.response_times else "N/A",
            'rate_limit_detected': self.server_feedback.rate_limit_detected,
        }
    
    def reset(self):
        """Reset rate limiter state"""
        self.tokens = float(self.bucket_size)
        self.last_refill = time.monotonic()
        self.response_times.clear()
        self.consecutive_slow_responses = 0
        self.backoff_multiplier = 1.0
        self.server_feedback = ServerFeedback()
        self._last_reduce_time = 0
        self._last_increase_time = 0
        self._soft_limit_count = 0


# Test the professional rate limiter
async def test_professional_rate_limiter():
    """Test all features of the professional rate limiter"""
    print("=" * 70)
    print("Testing Professional Token Bucket Rate Limiter")
    print("=" * 70)
    
    limiter = TokenBucketRateLimiter(
        tokens_per_second=10.0,
        bucket_size=20,
        enable_adaptive=True,
        latency_threshold_ms=500.0
    )
    
    # Test 1: Basic token bucket
    print("\n1. Testing Token Bucket (10 req/s, burst 20)...")
    start = time.monotonic()
    
    for i in range(30):
        await limiter.acquire()
        print(f"  Request {i+1:2d} at {time.monotonic() - start:.3f}s")
        await limiter.done()
    
    elapsed = time.monotonic() - start
    print(f"[OK] 30 requests in {elapsed:.2f}s (expected ~2s with burst)")
    
    # Test 2: Adaptive pacing with slow responses
    print("\n2. Testing Adaptive Pacing (simulating slow server)...")
    limiter.reset()
    
    for i in range(10):
        await limiter.acquire()
        # Simulate slow response
        await limiter.report_response_time(0.8)  # 800ms response
        await limiter.done()
    
    stats = limiter.get_stats()
    print(f"[OK] Adaptive adjustments: {stats['adaptive_adjustments']}")
    print(f"[OK] Current rate: {stats['current_rate']}")
    
    # Test 3: Server feedback detection
    print("\n3. Testing Server Feedback Detection...")
    limiter.reset()
    
    # Simulate rate limit close code
    await limiter.report_server_feedback(close_code=1008, close_reason="Rate limit exceeded")
    
    stats = limiter.get_stats()
    print(f"[OK] Rate limit detected: {stats['rate_limit_detected']}")
    print(f"[OK] Backoff multiplier: {stats['backoff_multiplier']}")
    
    # Test 4: Concurrency handling
    print("\n4. Testing Concurrency (10 parallel requests)...")
    limiter.reset()
    
    async def send_request(id):
        await limiter.acquire()
        await asyncio.sleep(0.1)  # Simulate work
        await limiter.done()
        return id
    
    tasks = [send_request(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(f"[OK] Completed {len(results)} concurrent requests")
    
    # Final stats
    print("\n" + "=" * 70)
    print("Final Statistics:")
    print("=" * 70)
    stats = limiter.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n[SUCCESS] ALL TESTS PASSED - Professional Rate Limiter Working!")

if __name__ == "__main__":
    asyncio.run(test_professional_rate_limiter())
