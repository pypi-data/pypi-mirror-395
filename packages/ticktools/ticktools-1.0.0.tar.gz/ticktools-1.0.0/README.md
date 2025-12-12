# ChronoKit

A simple Python stopwatch/timer utility.

### Installation

```bash
pip install chronokit
```

### Usage

```python
from chronokit import stopwatch, wait, from_start

stopwatch("start")
wait(1500)
print(stopwatch("stop"))
```

Works with any capitalization:

```python
stopwatch("StArT")
stopwatch("sToP")
```
