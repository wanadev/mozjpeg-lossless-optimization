import pytest

import mozjpeg_lossless_optimization


class Test_optimize(object):
    @pytest.fixture
    def image_bytes(self):
        with open("./tests/image.jpg", "rb") as file_:
            return file_.read()

    def test_optimize_returns_bytes(self, image_bytes):
        result = mozjpeg_lossless_optimization.optimize(image_bytes)
        assert type(result) is bytes

    def test_optimize_returns_a_jpeg(self, image_bytes):
        result = mozjpeg_lossless_optimization.optimize(image_bytes)
        assert result.startswith(b"\xff\xd8\xff\xe0\x00\x10JFIF")

    def test_optimize_returns_a_smaller_jpeg(self, image_bytes):
        result = mozjpeg_lossless_optimization.optimize(image_bytes)
        assert len(result) > 0
        assert len(result) < len(image_bytes)

    def test_optimize_raise_error_with_troncated_input_jpeg(self):
        with pytest.raises(ValueError):
            mozjpeg_lossless_optimization.optimize(b"\xff\xd8\xff\xe0\x00\x10JFIF")

    def test_optimize_raise_error_with_invalid_input_data(self):
        with pytest.raises(ValueError):
            mozjpeg_lossless_optimization.optimize(b"foobar")

    def test_optimize_with_copy(self, image_bytes):
        result = mozjpeg_lossless_optimization.optimize(
            image_bytes, copy=mozjpeg_lossless_optimization.COPY_MARKERS.ALL
        )
        assert result.startswith(b"\xff\xd8\xff\xe0\x00\x10JFIF")
