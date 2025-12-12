"""
rate limiting and abuse protection for inbox endpoint.

implements sliding window rate limiting per sender and per IP.
"""

import time
from collections import defaultdict, deque
from typing import Dict, Tuple


class RateLimiter:
    """
    in-memory sliding window rate limiter.
    
    tracks requests per sender and per IP address with configurable limits.
    thread-safe for single-process deployment.
    
    for multi-process deployment, replace with redis-based implementation.
    """
    
    def __init__(
        self,
        sender_limit: int = 100,
        sender_window_seconds: int = 60,
        ip_limit: int = 500,
        ip_window_seconds: int = 60,
    ):
        """
        initialize rate limiter.
        
        args:
            sender_limit: max requests per sender in window
            sender_window_seconds: time window for sender limit
            ip_limit: max requests per ip in window
            ip_window_seconds: time window for ip limit
        """
        self.sender_limit = sender_limit
        self.sender_window_seconds = sender_window_seconds
        self.ip_limit = ip_limit
        self.ip_window_seconds = ip_window_seconds
        
        # track timestamps: key -> deque of timestamps
        self._sender_requests: Dict[str, deque] = defaultdict(deque)
        self._ip_requests: Dict[str, deque] = defaultdict(deque)
    
    def _cleanup_old_entries(
        self,
        timestamps: deque,
        window_seconds: int,
        current_time: float,
    ) -> None:
        """remove timestamps outside the window."""
        cutoff = current_time - window_seconds
        while timestamps and timestamps[0] < cutoff:
            timestamps.popleft()
    
    def check_sender_limit(self, sender: str) -> Tuple[bool, int, int]:
        """
        check if sender is within rate limit.
        
        args:
            sender: agent canonical uri
            
        returns:
            tuple of (is_allowed, current_count, limit)
        """
        current_time = time.time()
        timestamps = self._sender_requests[sender]
        
        # cleanup old entries
        self._cleanup_old_entries(
            timestamps,
            self.sender_window_seconds,
            current_time,
        )
        
        # check limit
        current_count = len(timestamps)
        is_allowed = current_count < self.sender_limit
        
        return (is_allowed, current_count, self.sender_limit)
    
    def check_ip_limit(self, ip_address: str) -> Tuple[bool, int, int]:
        """
        check if ip address is within rate limit.
        
        args:
            ip_address: client ip address
            
        returns:
            tuple of (is_allowed, current_count, limit)
        """
        current_time = time.time()
        timestamps = self._ip_requests[ip_address]
        
        # cleanup old entries
        self._cleanup_old_entries(
            timestamps,
            self.ip_window_seconds,
            current_time,
        )
        
        # check limit
        current_count = len(timestamps)
        is_allowed = current_count < self.ip_limit
        
        return (is_allowed, current_count, self.ip_limit)
    
    def record_request(self, sender: str, ip_address: str) -> None:
        """
        record a request for rate limiting.
        
        args:
            sender: agent canonical uri
            ip_address: client ip address
        """
        current_time = time.time()
        
        # record sender request
        self._sender_requests[sender].append(current_time)
        
        # record ip request
        self._ip_requests[ip_address].append(current_time)
    
    def check_and_record(
        self,
        sender: str,
        ip_address: str,
    ) -> Tuple[bool, str]:
        """
        check limits and record request if allowed.
        
        args:
            sender: agent canonical uri
            ip_address: client ip address
            
        returns:
            tuple of (is_allowed, error_message)
            error_message is empty string if allowed
        """
        # check sender limit
        sender_allowed, sender_count, sender_limit = self.check_sender_limit(sender)
        if not sender_allowed:
            return (
                False,
                f"rate limit exceeded for sender {sender}: "
                f"{sender_count}/{sender_limit} requests per {self.sender_window_seconds}s",
            )
        
        # check ip limit
        ip_allowed, ip_count, ip_limit = self.check_ip_limit(ip_address)
        if not ip_allowed:
            return (
                False,
                f"rate limit exceeded for IP {ip_address}: "
                f"{ip_count}/{ip_limit} requests per {self.ip_window_seconds}s",
            )
        
        # both limits ok - record request
        self.record_request(sender, ip_address)
        return (True, "")
    
    def reset(self) -> None:
        """clear all rate limit counters (useful for testing)."""
        self._sender_requests.clear()
        self._ip_requests.clear()


# global rate limiter instance
_rate_limiter: RateLimiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """
    get global rate limiter instance.
    
    returns:
        rate limiter instance
    """
    return _rate_limiter

