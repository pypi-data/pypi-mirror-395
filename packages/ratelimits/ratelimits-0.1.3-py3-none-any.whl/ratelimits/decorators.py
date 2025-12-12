import time
from collections import deque
from threading import Lock
from functools import wraps
from datetime import datetime as dt


class SlidingWindowRateLimiter(object):
  """
  Sliding window rate limiter decorator.
  
  Allows up to `calls` requests within a sliding `period` seconds window.
  Example: calls=30, period=60 means at most 30 calls in any rolling 60s window.
  """
  def __init__(self, calls=30, period=60, debug=False, log_message=None):
    self.calls = calls
    self.period = period
    self.wdw_call_count = deque()
    self.lock = Lock()
    self.debug = debug
    self.total_calls = 0
    self.min_interval = self.period/self.calls
    self.next_run = 0
    self.log_message = log_message 

  def __call__(self, func):
    @wraps(func)
    def wrapper(*args, **kwargs):

      with self.lock:
        now = time.monotonic()

        if now < self.next_run:
          # The thread is too early 
          self.next_run = max(now, self.next_run) + self.min_interval
          sleep_for = self.next_run - now
        else:
          # The thread is running late
          self.next_run = max(now, self.next_run) + self.min_interval
          sleep_for = 0

        if self.debug:
          self.total_calls += 1
          self.wdw_call_count.append(now)
          usage_ratio = len(self.wdw_call_count) / self.calls
          if self.log_message is None:
            print(f"{dt.now()} | WCnt={len(self.wdw_call_count)} WSize={self.calls} T={self.total_calls} U={100*usage_ratio:.0f}% W={sleep_for:.2f}s") 
          else:
            print(f"{dt.now()} | WCnt={len(self.wdw_call_count)} WSize={self.calls} T={self.total_calls} U={100*usage_ratio:.0f}% W={sleep_for:.2f}s | {self.log_message(args=args, kwargs=kwargs)}") 
        elif self.log_message is not None:
          print(self.log_message(args=args, kwargs=kwargs)) 

      # Sleep outside the lock
      time.sleep(sleep_for)

      return func(*args, **kwargs)
    return wrapper

class FixedWindowRateLimiter(object):
  """
  Fixed-window rate limiter decorator.
  Allows at most `calls` executions per `period` seconds (plus optional offsets).
  """
  
  def __init__(self, calls=30, period=60, offset_start=0, offset_end=0, debug=False, log_message=None):
    self.calls  = calls
    self.period = period
    
    # total count of calls sent
    self.total_call_count = 0
    # count of calls sent in current window
    self.wdw_call_count = 0

    # time window edges
    self.offset_end   = offset_end
    self.offset_start = offset_start

    self.lock = Lock()
    # initialize last run w dummy var
    self.last_time_run = period
    self.debug = debug
    self.log_message = log_message 

  def __call__(self, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      # try to acquire the lock to access thread safe zone
      with self.lock:
        time_run = time.time()%self.period//1

        # adjust to window start edges
        if (self.offset_start > time_run%self.period):
          time.sleep(self.offset_start - time_run%self.period//1)
        # adjust to window end edges
        if (self.offset_end > self.period - time_run%self.period):
          time.sleep(self.period - time_run%self.period + self.offset_start)
        # update state variables        
        time_run = time.time()%self.period//1

        # condition 2: check if we are running in current window by validating time increase
        if (time_run < self.last_time_run) and self.total_call_count!=0:
          self.wdw_call_count = 0
        # condition 1: check if current time window quota was exceeded, if so, then wait
        if (self.wdw_call_count==self.calls) and self.total_call_count!=0:
          time.sleep(self.period + self.offset_start - time.time()%self.period//1)
          # update state variables        
          time_run = time.time()%self.period//1
          self.wdw_call_count = 0

        # update state variables
        self.last_time_run = time_run
        self.total_call_count += 1
        self.wdw_call_count += 1

        if self.debug and self.log_message is None:
          print(f"{dt.now()} | WCnt={self.wdw_call_count} WSize={self.calls} T={self.total_call_count}")
        elif self.debug and self.log_message is not None:
          print(f"{dt.now()} | WCnt={self.wdw_call_count} WSize={self.calls} T={self.total_call_count} | {self.log_message(args=args, kwargs=kwargs)}")
        elif self.log_message is not None:
          print(self.log_message(args=args, kwargs=kwargs))

      # Make the API request
      return func(*args, **kwargs)

    return wrapper
  
# -------------------------------
# Factory / Decorator Function
# -------------------------------
def ratelimits(type: str, *args, **kwargs):
    """
    Factory + decorator for rate limiters.
    Example:
        @ratelimits("fixed", calls=10, period=30)
        def my_func(): ...
    """
    type = type.lower()
    if type == "fixed_window" or type == "bursty":
        limiter = FixedWindowRateLimiter(*args, **kwargs)
    elif type == "sliding_window" or type == "steady":
        limiter = SlidingWindowRateLimiter(*args, **kwargs)
    else:
        raise ValueError(f"Unknown rate limiter type: {type}")
    return limiter
