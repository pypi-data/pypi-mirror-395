Artefacts X-Ray
===============

Resource tracker for process trees rooted in a Python process.


Usage
-----

The tracker is a context manager:

```python
from axray import resource_tracking

with resource_tracking():
    work()
```

By default it tracks the process tree executed in the context, here everything that happens inside `work()`.


Comprehensive Demo
------------------

A demo script in this repository can report on a range of situations:

* Single process CPU only usage
* Single process memory only usage
* Single process CPU and memory usage
* Multi process CPU only usage
* Multi process memory only usage
* Multi process CPU and memory only usage

With some extras like reporting the time overhead of tracking (but indicative only, not statistically confirmed).

Assuming the `uv` tool is available:

```shell
./bin/demo
```

In the absence of `uv` the script requires Numpy and can be run with `python bin/demo`.


Test Suite
----------

The test suite uses PyTest and tries to cover relevant situations in resource tracking (over time it should go beyond what `bin/demo` covers).

Some tests are *slow* because they try to validate somewhat realistic situations (child processes not *too* short), as well as statistical relevance of reporting. Most tests can be run with:

```
uv run pytest -m "not slowest"   # Remove `uv run` if `pytest` available
```

This runs excluding the really slow tests. As the project progresses, other tests get marked as slow/slower/slowest to try to find good balance and configurability.

