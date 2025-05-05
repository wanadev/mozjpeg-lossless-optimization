from ._mozjpeg_opti import lib, ffi

_copy_opts = {
    'none': 0,            # copy no optional markers
    'comments': 1,        # copy only comment (COM) markers
    'all': 2,             # copy all optional markers
    'all_except_icc': 3,  # copy all optional markers except APP2
    'icc': 4              # copy only ICC profile (APP2) markers
}


def optimize(input_jpeg_bytes, copy='none'):
    output_jpeg_bytes_p = ffi.new("unsigned char**")
    output_jpeg_bytes_p_gc = ffi.gc(
        output_jpeg_bytes_p, lib.mozjpeg_lossless_optimization_free_bytes
    )
    copy_option = _copy_opts.get(copy, 0)

    output_jpeg_length = lib.mozjpeg_lossless_optimization(
        input_jpeg_bytes,
        len(input_jpeg_bytes),
        output_jpeg_bytes_p_gc,
        copy_option
    )

    if output_jpeg_length == 0:
        raise ValueError("MozJPEG was not able to process the input image")

    output_jpeg = ffi.cast("unsigned char*", output_jpeg_bytes_p_gc[0])
    return bytes(ffi.unpack(output_jpeg, output_jpeg_length))
