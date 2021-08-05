#!/usr/bin/env python
# encoding: UTF-8

import os
import subprocess
from distutils import ccompiler

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


def _find_msbuild(plat_spec="x64"):
    # https://github.com/python/cpython/blob/master/Lib/distutils/_msvccompiler.py
    import distutils._msvccompiler as msvc

    vc_env = msvc._get_vc_env(plat_spec)
    if "vsinstalldir" not in vc_env:
        raise Exception("Unable to find any Visual Studio installation")
    return os.path.join(
        vc_env["vsinstalldir"], "MSBuild", "Current", "Bin", "MSBuild.exe"
    )


class CustomBuildPy(build_py):
    def run(self):
        if not os.path.isdir("./mozjpeg/build"):
            os.mkdir("./mozjpeg/build")

        os.chdir("./mozjpeg/build")

        if ccompiler.get_default_compiler() == "unix":
            os.environ["CFLAGS"] = "%s -fPIC" % os.environ.get("CFLAGS", "")
            subprocess.call(
                [
                    "cmake",
                    "..",
                    "-DENABLE_SHARED=FALSE",
                    "-DENABLE_STATIC=TRUE",
                    "-DPNG_SUPPORTED=FALSE",
                    "-DCMAKE_BUILD_TYPE=Release",
                ]
            )
            subprocess.call(["make"])
        elif ccompiler.get_default_compiler() == "msvc":
            # raise NotImplementedError("Windows build is not supported yet")
            msbuild = _find_msbuild()
            subprocess.call(
                [
                    "cmake",
                    "..",
                    "-DENABLE_SHARED=FALSE",
                    "-DENABLE_STATIC=TRUE",
                    "-DPNG_SUPPORTED=FALSE",
                    "-DCMAKE_BUILD_TYPE=Release",
                ]
            )
            subprocess.call([msbuild, "-p:Configuration=Release", "ALL_BUILD.vcxproj"])
        else:
            raise Exception("Unhandled platform")

        os.chdir("../..")

        build_py.run(self)


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="mozjpeg-lossless-optimization",
    version="0.9.0",
    description="Optimize JPEGs losslessly using MozJPEG",
    url="https://github.com/wanadev/mozjpeg-lossless-optimization",
    license="BSD-3-Clause",
    long_description=long_description,
    keywords="image jpeg mozjpeg jpegtran optimization cffi",
    author="Wanadev",
    author_email="contact@wanadev.fr",
    maintainer="Fabien LOISON",
    packages=find_packages(),
    setup_requires=[
        "cffi>=1.0.0",
    ],
    install_requires=[
        "cffi>=1.0.0",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
            "pytest",
        ]
    },
    cffi_modules=[
        "mozjpeg_lossless_optimization/mozjpeg_opti_build.py:ffibuilder",
    ],
    cmdclass={
        "build_py": CustomBuildPy,
    },
)
