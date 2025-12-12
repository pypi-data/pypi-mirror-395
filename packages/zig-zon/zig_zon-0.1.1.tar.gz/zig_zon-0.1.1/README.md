# Python Zig Zon Parser

A native python extension built with zig to parse zig-object-notation strings
into python objects.

On PyPi it is only distributed in source, and built during install.
It therefore needs to download the `ziglang` python package.

## Usage

install:

```bash
python3 -m pip install zig-zon
```

running:

```python
import zig_zon
parsed = zig_zon.parse('.{.allyourcode = .are_belong_to_us, .asd = 123}')
print(parsed)
```

or, look at the [test](https://gitlab.com/dasimmet/python-zig-zon/-/blob/main/src/test_zig_zon.py)

## How it works

When you run pip install, the source distribution is downloaded, and since
this package depends on the `ziglang` as well as my setuptools helper package:
[setuptools-zig-build](https://codeberg.org/dasimmet/setuptools-zig-build)

to execute `zig build` and put the resulting library in the wheel. 

## Developing

as opposed to other solutions, i want to develop using:

```
zig build test --watch
```

so [setuptools-zig-build](https://codeberg.org/dasimmet/setuptools-zig-build)
runs a python script that imports the cpython headers into zig's cache.
When the module is built using `pip`, zig will get a `-Dpython=` option pointing to the right executable,
otherwise system python in `PATH` is used.
pip installation also uses a `-Dversion=` option for the pip package version.
