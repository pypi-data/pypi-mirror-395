# myos

This package contains OS practical codes with both interactive (user input) and static (demo) versions.

## Installation
```bash
pip install myos
```

## Usage
Import the package and run the functions. 
- Functions ending in `_1` are **Interactive** (require input).
- Functions ending in `_2` are **Static** (print a demo).

### Examples
```python
import os_schedules

# Run FCFS Interactive
os_schedules.p4_1_1()

# Run FCFS Static Demo
os_schedules.p4_1_2()

# Run Banker's Algorithm Static
os_schedules.p7_2()
```
