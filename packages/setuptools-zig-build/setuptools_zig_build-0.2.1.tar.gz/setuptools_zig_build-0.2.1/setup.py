from setuptools import setup

setup(
    name='setuptools_zig_build',
    version="0.2.1",
    author_email='dasimmet@gmail.com',
    description='A setuptools extension, for building cpython extensions with zig build',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://codeberg.org/dasimmet/setuptools-zig-build',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3',
    py_modules=['setuptools_zig_build'],
    keywords='',
    entry_points={"distutils.setup_keywords": [
        'zig_build=setuptools_zig_build:setup_zig_build']},
)
