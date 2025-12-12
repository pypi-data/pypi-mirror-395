# ratelimiter

A small Python library that provides simple function decorators for rate limiting using either a fixed-window (bursty) or a sliding-window (steady) strategy.


Example — Fixed window (bursty)
```
from ratelimits import ratelimits
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime as dt

@ratelimits("fixed_window", calls=10, period=20)
def my_task(x):
    print(f"[{dt.now()}] task", x)

with ThreadPoolExecutor(max_workers=None) as executor:
    executor.map(my_task, range(20))
```

Example — Sliding window (steady, evenly spaced)
```
from ratelimits import ratelimits
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime as dt

@ratelimits(
  type   = "sliding_window", 
  calls  = 10, 
  period = 60,
  debug  = True,
  log_message = lambda args, kwargs: f"Running with args {args} and kwargs {kwargs}"
)
def my_task(x):
    print(f"[{dt.now()}] task", x)

with ThreadPoolExecutor(max_workers=None) as executor:
    executor.map(my_task, range(20))
```

### Parameters Summary

| Parameter | Type | Description |
|------------|------|-------------|
| **calls** | `int` | Maximum number of calls allowed per window. |
| **period** | `int` \| `float` | Duration of the window in seconds. |
| **offset_start** / **offset_end** | *(FixedWindow only)* | Optional adjustments for the start and end edges of the window. |
| **debug** | `bool` | Enables verbose logging to stdout for debugging and tracing sleep intervals. |
| **log_message** | `text` | Optional print statement to track execution parameters. |
