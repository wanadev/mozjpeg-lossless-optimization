import os
from distutils import ccompiler

from cffi import FFI


_ROOT = os.path.abspath(os.path.dirname(__file__))
_C_FILE = os.path.join(_ROOT, "mozjpeg_opti.c")
_H_FILE = os.path.join(_ROOT, "mozjpeg_opti.h")
if ccompiler.get_default_compiler() == "unix":
    _LIBJPEG_STATIC_LIB = os.path.join(_ROOT, "..", "mozjpeg", "build", "libjpeg.a")
elif ccompiler.get_default_compiler() == "msvc":
    _LIBJPEG_STATIC_LIB = os.path.join(
        _ROOT, "..", "mozjpeg", "build", "Release", "jpeg-static.lib"
    )

if not os.path.isfile(_LIBJPEG_STATIC_LIB):
    raise Exception(
        "Unable to find libjpeg in '%s'. "
        "If you are trying to build the lib manually, you should build mozjpeg first. "
        % _LIBJPEG_STATIC_LIB
    )

ffibuilder = FFI()
ffibuilder.set_source(
    "mozjpeg_lossless_optimization._mozjpeg_opti",
    open(_C_FILE, "r").read(),
    extra_objects=[_LIBJPEG_STATIC_LIB],
    include_dirs=[
        _ROOT,
        os.path.join(_ROOT, "..", "mozjpeg"),
        os.path.join(_ROOT, "..", "mozjpeg", "build"),
    ],
)
ffibuilder.cdef(open(_H_FILE, "r").read())


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
