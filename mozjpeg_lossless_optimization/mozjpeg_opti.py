from ._mozjpeg_opti import lib, ffi


def optimize(input_jpeg_bytes):
    output_jpeg_bytes_p = ffi.new("unsigned char**")
    output_jpeg_bytes_p_gc = ffi.gc(
        output_jpeg_bytes_p, lib.mozjpeg_lossless_optimization_free_bytes
    )

    output_jpeg_length = lib.mozjpeg_lossless_optimization(
        input_jpeg_bytes,
        len(input_jpeg_bytes),
        output_jpeg_bytes_p_gc,
    )

    if output_jpeg_length == 0:
        raise ValueError("MozJPEG was not able to process the input image")

    output_jpeg = ffi.cast("unsigned char*", output_jpeg_bytes_p_gc[0])
    return bytes(ffi.unpack(output_jpeg, output_jpeg_length))
