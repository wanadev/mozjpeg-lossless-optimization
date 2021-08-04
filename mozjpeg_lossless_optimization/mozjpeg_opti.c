#include "../mozjpeg/cdjpeg.h"
#include "./mozjpeg_opti.h"


unsigned long mozjpeg_lossless_optimization(
    unsigned char *input_jpeg_bytes,
    unsigned long input_jpeg_length,
    unsigned char **output_jpeg_bytes
) {
    // Initialize the JPEG decompression object with default error handling.
    struct jpeg_decompress_struct srcinfo;
    struct jpeg_error_mgr jsrcerr;
    srcinfo.err = jpeg_std_error(&jsrcerr);
    jpeg_create_decompress(&srcinfo);

    // Initialize the JPEG compression object with default error handling.
    struct jpeg_compress_struct dstinfo;
    struct jpeg_error_mgr jdsterr;
    dstinfo.err = jpeg_std_error(&jdsterr);
    jpeg_create_compress(&dstinfo);

    // Set compression options
    dstinfo.optimize_coding = TRUE;
    jpeg_simple_progression(&dstinfo);

    // Read the input JPEG
    jpeg_mem_src(&srcinfo, input_jpeg_bytes, input_jpeg_length);
    jpeg_read_header(&srcinfo, TRUE);
    jvirt_barray_ptr *src_coef_arrays = jpeg_read_coefficients(&srcinfo);

    // prepare output
    unsigned long output_jpeg_length = 0;
    jpeg_mem_dest(&dstinfo, output_jpeg_bytes, &output_jpeg_length);

    // Compress
    jpeg_copy_critical_parameters(&srcinfo, &dstinfo);
    jpeg_write_coefficients(&dstinfo, src_coef_arrays);
    jpeg_finish_compress(&dstinfo);

    // Cleanup
    jpeg_destroy_compress(&dstinfo);
    jpeg_finish_decompress(&srcinfo);
    jpeg_destroy_decompress(&srcinfo);

    return output_jpeg_length;
}


void mozjpeg_lossless_optimization_free_bytes(unsigned char **bytes) {
    free(*bytes);
}
