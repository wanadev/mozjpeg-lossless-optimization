unsigned long mozjpeg_lossless_optimization(
    unsigned char *input_jpeg_bytes,
    unsigned long input_jpeg_length,
    unsigned char **output_jpeg_bytes,
    int copyoption
);

void mozjpeg_lossless_optimization_free_bytes(unsigned char **bytes);
