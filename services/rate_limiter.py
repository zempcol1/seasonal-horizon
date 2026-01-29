"""
Simple in-memory rate limiter for API endpoints.
Uses sliding window algorithm.
"""

import time
from collections import defaultdict
from functools import wraps
from flask import request, jsonify
from config import config
from services.logging_service import log_event


class RateLimiter:
    """Simple sliding window rate limiter."""
    
    def __init__(self):
        # {ip: [timestamp, timestamp, ...]}
        self._requests = defaultdict(list)
        self._last_cleanup = time.time()
        self._cleanup_interval = 60  # Clean up every minute
    
    def _cleanup_old_requests(self):
        """Remove requests older than 1 minute."""
        now = time.time()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        
        cutoff = now - 60
        for ip in list(self._requests.keys()):
            self._requests[ip] = [t for t in self._requests[ip] if t > cutoff]
            if not self._requests[ip]:
                del self._requests[ip]
        
        self._last_cleanup = now
    
    def is_allowed(self, ip: str, limit: int) -> bool:
        """
        Check if request is allowed for given IP.
        
        Args:
            ip: Client IP address
            limit: Maximum requests per minute
            
        Returns:
            True if allowed, False if rate limited
        """
        self._cleanup_old_requests()
        
        now = time.time()
        cutoff = now - 60
        
        # Filter to last minute
        recent = [t for t in self._requests[ip] if t > cutoff]
        self._requests[ip] = recent
        
        if len(recent) >= limit:
            return False
        
        self._requests[ip].append(now)
        return True
    
    def get_remaining(self, ip: str, limit: int) -> int:
        """Get remaining requests for this IP."""
        cutoff = time.time() - 60
        recent = [t for t in self._requests[ip] if t > cutoff]
        return max(0, limit - len(recent))


# Global instance
_limiter = RateLimiter()


def rate_limit(limit: int):
    """
    Decorator to apply rate limiting to a route.
    
    Args:
        limit: Maximum requests per minute
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ip:
                ip = ip.split(',')[0].strip()
            
            if not _limiter.is_allowed(ip, limit):
                log_event('rate_limit', f'{ip}')
                return jsonify({
                    'success': False,
                    'error': 'Rate limit exceeded. Please wait a moment.',
                    'retry_after': 60
                }), 429
            
            return f(*args, **kwargs)
        return wrapped
    return decorator


def get_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    return _limiter
