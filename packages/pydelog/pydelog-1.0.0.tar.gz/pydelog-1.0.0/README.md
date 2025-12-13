# pydelog

`pydelog` is a lightweight, colorful, and simple debug/logging utility for Python.  
It provides:

- Colored logs  
- Multiple log levels  
- A built-in timer decorator  
- Easy and clean integration  

---

## Installation
```bash
pip install pydelog
```

## Basic Usage
```bash
from pydelog import DebugUtils

DebugUtils.log_i("Information message")
DebugUtils.log_e("Error occurred!")
DebugUtils.log_w("This is a warning")
DebugUtils.log_d("Debug message")
```

## Timer Example
```bash
from pydelog import DebugUtils

@DebugUtils.timer
def sample_task():
    for _ in range(1000000):
        pass

sample_task()
```
Output: 
```bash
[DEBUG] sample_task executed in 0.123456s
```

## Disable Colors or Logs
### Disable colored output:
```bash
from pydelog import DebugUtils
DebugUtils.ENABLE_COLOR = False
```
### Disable all logs:
```bash
DebugUtils.ENABLE_LOGS = False
```

## Available Log Levels
```bash
from pydelog import DebugUtils, LogLevel

DebugUtils.log_i("Info")
DebugUtils.log_e("Error")
DebugUtils.log_d("Debug")
DebugUtils.log_f("Fatal")
DebugUtils.log_c("Critical")
DebugUtils.log_w("Warning")
DebugUtils.log_t("Trace")
DebugUtils.log_v("Verbose")
DebugUtils.log_s("System")
DebugUtils.log_a("Alert")
```