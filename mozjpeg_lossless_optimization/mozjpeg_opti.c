#include <setjmp.h>
#include "../mozjpeg/cdjpeg.h"
#include "../mozjpeg/transupp.h"
#include "./mozjpeg_opti.h"


struct custom_jpeg_error_mgr {
    struct jpeg_error_mgr pub;
    jmp_buf setjmp_buffer;
};


void mozjpeg_lossless_optimization_error_exit(j_common_ptr cinfo) {
    struct custom_jpeg_error_mgr* err = (struct custom_jpeg_error_mgr*) cinfo->err;
    longjmp(err->setjmp_buffer, 1);
}


void mozjpeg_lossless_optimization_emit_message(j_common_ptr cinfo, int msg_level) {
    // Suppress message writing on stderr...
}


unsigned long mozjpeg_lossless_optimization(
    unsigned char *input_jpeg_bytes,
    unsigned long input_jpeg_length,
    unsigned char **output_jpeg_bytes,
    int copyoption
) {
    // Initialize the JPEG decompression object with custom error handling
    struct jpeg_decompress_struct srcinfo;

    struct custom_jpeg_error_mgr cjsrcerr;
    srcinfo.err = jpeg_std_error(&cjsrcerr.pub);
    cjsrcerr.pub.error_exit = &mozjpeg_lossless_optimization_error_exit;
    cjsrcerr.pub.emit_message = &mozjpeg_lossless_optimization_emit_message;

    jpeg_create_decompress(&srcinfo);

    // Enable saving of extra markers that we want to copy
    jcopy_markers_setup(&srcinfo, copyoption);

    // Initialize the JPEG compression object with default error handling
    struct jpeg_compress_struct dstinfo;

    struct jpeg_error_mgr jdsterr;
    dstinfo.err = jpeg_std_error(&jdsterr);

    jpeg_create_compress(&dstinfo);

    // Handle decompression errors
    if (setjmp(cjsrcerr.setjmp_buffer)) {
        jpeg_destroy_compress(&dstinfo);
        jpeg_destroy_decompress(&srcinfo);
        return 0;
    }

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

    // Copy to the output file any extra markers that we want to preserve */
    jcopy_markers_execute(&srcinfo, &dstinfo, copyoption);

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
