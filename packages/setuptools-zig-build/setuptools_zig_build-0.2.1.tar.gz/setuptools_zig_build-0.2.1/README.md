# Setuptools zig build

A setuptools extension, for building cpython extensions with zig build,
enabling simple source-only pip distributions that compile at install time.

check out [zig-zon](https://codeberg.org/dasimmet/python-zig-zon/) for a full example.

## Example 

Your project needs to have:
- `setup.py` to configure this setuptools extension to run during python's wheel build
- `build.zig` to configure the build of the shared library
- `build.zig.zon` optionally - to specify zig dependencies

```python
from setuptools import Extension
from setuptools import setup

setup(
    name='zig-zon',
    packages=[],
    zig_build={
        # stores zig's depdendency pacakges in python's sdist. This requires a call to
        # CPython.addSdistList(b); in `build.zig`
        # If set to False, potential dependencies will be downloaded by zig instead.
        "sdist": True,
        # tries to import 'ziglang' to get a zig compiler when building wheel
        "use_ziglang_python_package": True,
        # passes -Doptimize= to zig build
        "optimize": "ReleaseSmall",
        # passes -Dversion=<pip package version> to zig build
        "pass_version_option": True,
        # extra arguments to zig build. In this case we pass the `install` and `test` steps
        'extra_args': [
            "install", "test",
        ],
    },
    # Names of the libraries your `build.zig` will produce, and this module will install
    ext_modules=[Extension('zig_zon', [])],
)
```

## References

@ruamel and [setuptools-zig](https://sourceforge.net/p/setuptools-zig)
