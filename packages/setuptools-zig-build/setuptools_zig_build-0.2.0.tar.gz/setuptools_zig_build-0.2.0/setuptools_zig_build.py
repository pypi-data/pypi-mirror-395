# coding: utf-8

import sys
import os
from subprocess import run
from pathlib import Path
import shlex

from setuptools import Extension
from distutils.dist import Distribution
from setuptools.command.build_ext import build_ext as SetupToolsBuildExt
from setuptools.command.sdist import sdist as SetupToolsSdist


class ZigCompilerError(Exception):
    """Some compile/link operation failed."""


class ZigBuild:
    '''the type of the custom "zig_build" argument to setup.py'''
    OPTIMIZE = [
        "Debug",
        "ReleaseSafe",
        "ReleaseFast",
        "ReleaseSmall",
    ]

    def __init__(self,
                 use_ziglang_python_package: bool = False,
                 optimize: str = "ReleaseSafe",
                 pass_version_option: bool = False,
                 extra_args: list = [],
                 sdist: bool = False,
                 ):
        assert isinstance(use_ziglang_python_package, bool)
        self.use_ziglang_python_package = use_ziglang_python_package
        assert optimize == None or (isinstance(
            optimize, str) and optimize in self.OPTIMIZE)
        self.optimize = optimize
        assert isinstance(pass_version_option, bool)
        self.pass_version_option = pass_version_option
        assert isinstance(extra_args, list)
        for arg in extra_args:
            assert isinstance(arg, str)
        self.extra_args = extra_args
        assert isinstance(sdist, bool)
        self.sdist = sdist


class BuildExt(SetupToolsBuildExt):
    def __init__(self, dist, zig_value):
        if isinstance(zig_value, dict):
            self._zig_value = ZigBuild(**zig_value)
        elif isinstance(zig_value, ZigBuild):
            self._zig_value = zig_value
        else:
            raise ZigCompilerError('unknown type:', zig_value)

        super().__init__(dist)

    def build_extension(self, ext):
        ext: Extension
        if not self._zig_value:
            return super().build_extension(ext)

        build_zig_dir = "."
        if len(ext.sources) == 1:
            build_zig_dir = ext.sources[0]
        elif len(ext.sources) > 1:
            raise ZigCompilerError(
                "sources should only point to build.zig directory")

        target = Path(self.get_ext_fullpath(ext.name))

        output_ext = os.path.splitext(self.get_ext_filename(ext.name))[1]

        zig_out = Path(self.build_temp) / "zig-out"

        zig_exe = os.environ.get('PY_ZIG', 'zig')
        if self._zig_value.use_ziglang_python_package == True:
            import ziglang
            zig_exe = os.path.join(
                os.path.dirname(ziglang.__file__), "zig")

        bld_cmd = [zig_exe, 'build',
                   '-Dpython={}'.format(sys.executable), '--prefix', str(zig_out.absolute())]

        if self._zig_value.optimize != None:
            bld_cmd.append(
                '-Doptimize={}'.format(self._zig_value.optimize))

        if self._zig_value.pass_version_option == True:
            bld_cmd.append(
                '-Dversion={}'.format(self.distribution.get_version()))

        bld_cmd.extend(self._zig_value.extra_args)

        if self._zig_value.sdist:
            if os.path.isdir(".zig-dependencies"):
                for it in os.listdir(".zig-dependencies"):
                    dep_dir = os.path.join(".zig-dependencies", it)
                    if os.path.isdir(".zig-dependencies"):
                        fetch_cmd = [zig_exe, "fetch", dep_dir]
                        print("cmd: {}".format(shlex.join(fetch_cmd)))
                        run(fetch_cmd, check=True)

        os.makedirs(self.build_temp, exist_ok=True)
        print('\ncmd', shlex.join(bld_cmd))
        sys.stdout.flush()
        run(bld_cmd, check=True, cwd=build_zig_dir)

        output = None
        for subpath in ['', 'lib', 'bin/', 'lib/', 'bin/lib', 'lib/lib']:
            zig_output = zig_out / (subpath + ext.name + output_ext)
            if zig_output.exists():
                output = zig_output.absolute()
                break
            print('missing:', str(zig_output.absolute()), file=sys.stderr)

        if output == None:
            raise ZigCompilerError(f'expected output does not exist')

        print('found output:', str(output.absolute()),
              str(target), file=sys.stderr)

        if target.exists():
            target.unlink()
        else:
            target.parent.mkdir(exist_ok=True, parents=True)
        output.rename(target)


class Sdist(SetupToolsSdist):
    def make_release_tree(self, base_dir, files) -> None:
        import os
        import json
        self.zig_dep_sources = []

        sdistlist_name = os.path.join(base_dir, 'sdistlist.json')

        from subprocess import run
        zig_exe = "zig"
        try:
            import ziglang
            zig_exe = os.path.join(
                os.path.dirname(ziglang.__file__), "zig")
        except:
            pass

        cmd = [zig_exe, "build", "sdistlist", '--prefix', base_dir]
        print("cmd:", cmd)
        run(cmd, check=True)
        import shutil

        with open(sdistlist_name) as fd:
            sdistlist = json.load(fd)

        for deps in sdistlist['dependencies']:
            src = os.path.join(sdistlist['global_cache_dir'], 'p', deps[1])
            dst = os.path.join(base_dir, '.zig-dependencies', deps[1])
            if not os.path.isdir(src):
                print("dep not found:", deps[0], src)
                continue
            print("packaging zig dep:", deps[0], src)
            for root, _, walk_files in os.walk(src):
                if '.zig-cache' in root:
                    continue
                rel_dir = os.path.relpath(root, src)
                os.makedirs(os.path.join(dst, rel_dir), exist_ok=True)
                for f in walk_files:
                    source_file = os.path.join(root, f)
                    rel_file = os.path.normpath(
                        os.path.join(rel_dir, f))
                    dest_file = os.path.normpath(
                        os.path.join(dst, rel_dir, f))
                    shutil.copyfile(source_file, dest_file)
                    self.zig_dep_sources.append(rel_file)

        super().make_release_tree(base_dir, files)
        files.extend(self.zig_dep_sources)


class ZigBuildExtension:
    def __init__(self, value):
        self._value = value

    def __call__(self, dist):
        return BuildExt(dist, zig_value=self._value)


def setup_zig_build(dist, keyword, value):
    '''our hook into setuptools '''
    assert isinstance(dist, Distribution)
    assert keyword == 'zig_build'
    dist.cmdclass.get('build_ext')
    dist.cmdclass['build_ext'] = ZigBuildExtension(value)
    if 'sdist' in value and value['sdist'] == True:
        dist.cmdclass.get('sdist')
        dist.cmdclass['sdist'] = Sdist
