#!/usr/bin/env python
# encoding: UTF-8

import os
import subprocess

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext


def _find_msbuild(plat_spec="x64"):
    from setuptools import msvc

    if hasattr(msvc, "msvc14_get_vc_env"):
        vc_env = msvc.msvc14_get_vc_env(plat_spec)
        if "vsinstalldir" in vc_env:
            msbuild_path = os.path.join(
                vc_env["vsinstalldir"], "MSBuild", "Current", "Bin", "MSBuild.exe"
            )
            if os.path.isfile(msbuild_path):
                return msbuild_path

    for path in msvc.EnvironmentInfo(plat_spec).VCTools:
        if "\\VC\\" not in path:
            continue
        msbuild_path = os.path.join(
            path[: path.index("\\VC\\")], "MSBuild", "Current", "Bin", "MSBuild.exe"
        )
        if os.path.isfile(msbuild_path):
            return msbuild_path

    raise Exception("Unable to find any Visual Studio installation")


class CustomBuildExt(build_ext):
    def build_extensions(self):
        if not os.path.isdir("./mozjpeg/build"):
            os.mkdir("./mozjpeg/build")

        os.chdir("./mozjpeg/build")
        cmake_command = [
            "cmake",
            "..",
            "-B",
            ".",
            "-DBUILD_SHARED_LIBS=FALSE",
            "-DPNG_SUPPORTED=FALSE",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        if self.compiler.compiler_type == "unix":
            os.environ["CFLAGS"] = "%s -fPIC" % os.environ.get("CFLAGS", "")
            subprocess.call(cmake_command)
            subprocess.call(["make"])
        elif self.compiler.compiler_type == "msvc":
            msbuild = _find_msbuild()
            subprocess.call(cmake_command)
            subprocess.call([msbuild, "-p:Configuration=Release", "ALL_BUILD.vcxproj"])
        else:
            raise Exception("Unsupported platform")

        os.chdir("../..")

        build_ext.build_extensions(self)


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="mozjpeg-lossless-optimization",
    version="1.3.0",
    project_urls={
        "Source Code": "https://github.com/wanadev/mozjpeg-lossless-optimization",
        "Documentation": "https://github.com/wanadev/mozjpeg-lossless-optimization#usage",
        "Changelog": "https://github.com/wanadev/mozjpeg-lossless-optimization#changelog",
        "Issues": "https://github.com/wanadev/mozjpeg-lossless-optimization/issues",
        "Chat": "https://discord.gg/BmUkEdMuFp",
    },
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
        "build_ext": CustomBuildExt,
    },
)
