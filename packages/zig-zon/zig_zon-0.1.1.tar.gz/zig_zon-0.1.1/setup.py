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
