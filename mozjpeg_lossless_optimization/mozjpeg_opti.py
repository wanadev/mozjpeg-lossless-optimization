from enum import IntEnum

from ._mozjpeg_opti import lib, ffi


class COPY_MARKERS(IntEnum):
    """Metadata copy options."""

    #: copy no optional markers
    NONE = 0

    #: copy only comment (COM) markers
    COMMENTS = 1

    #: copy all optional markers
    ALL = 2

    #: copy all optional markers except APP2
    ALL_EXCEPT_ICC = 3

    #: copy only ICC profile (APP2) markers
    ICC = 4


def optimize(input_jpeg_bytes, copy=COPY_MARKERS.NONE):
    """Optimize a JPEG.

    :param bytes input_jpeg_bytes: The input JPEG.
    :param COPY copy: Metadata copy options (optional, default ``COPY_MARKERS.NONE``).

    :raises ValueError: If MozJPG was not able to process the input image.

    :rtype: bytes
    :returns: The optimized JPEG.
    """
    output_jpeg_bytes_p = ffi.new("unsigned char**")
    output_jpeg_bytes_p_gc = ffi.gc(
        output_jpeg_bytes_p, lib.mozjpeg_lossless_optimization_free_bytes
    )
    copy_option = COPY_MARKERS(copy).value

    output_jpeg_length = lib.mozjpeg_lossless_optimization(
        input_jpeg_bytes,
        len(input_jpeg_bytes),
        output_jpeg_bytes_p_gc,
        copy_option,
    )

    if output_jpeg_length == 0:
        raise ValueError("MozJPEG was not able to process the input image")

    output_jpeg = ffi.cast("unsigned char*", output_jpeg_bytes_p_gc[0])
    return bytes(ffi.unpack(output_jpeg, output_jpeg_length))
