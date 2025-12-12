# Setuptools zig build

A setuptools extension, for building cpython extensions with zig build,
enabling simple source-only pip distributions that compile at install time.

check out [zig-zon](https://gitlab.com/dasimmet/python-zig-zon) for an example

## Example `setup.py`

```python
from setuptools import Extension
from setuptools import setup

setup(
    name='zig-zon',
    packages=[],
    zig_build={
        # stores zig's depdendencies in python's sdist. requires a call to
        # CPython.addSdistList(b); in `build.zig`
        "sdist": True,
        # tries to import 'ziglang' to get a zig compiler when building wheel
        "use_ziglang_python_package": True,
        # passes -Doptimize= to zig build
        "optimize": "ReleaseSmall",
        # passes -Dversion=<pip package version> to zig build
        "pass_version_option": True,
        # extra arguments to zig build
        'extra_args': [
            "install", "test",
        ],
    },
    ext_modules=[Extension('zig_zon', [])],
)
```

## References

@ruamel and [setuptools-zig](https://sourceforge.net/p/setuptools-zig)
