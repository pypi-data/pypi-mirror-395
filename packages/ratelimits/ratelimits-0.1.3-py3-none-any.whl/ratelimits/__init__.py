
'''
Function decorator for bursty and steady rate limiting

This module provides a functon decorator that can be used to wrap a function
such that it will raise an exception if the number of calls to that function
exceeds a maximum within a specified time window.
'''
from .decorators import SlidingWindowRateLimiter, FixedWindowRateLimiter, ratelimits
from .utilities import batch_generator

fixed_rate = FixedWindowRateLimiter
sliding_rate = SlidingWindowRateLimiter
ratelimits = ratelimits

__all__ = [
  'fixed_rate',
  'sliding_rate',
  'batch_generator',
  'ratelimits',
]

__version__ = '0.1.1'
