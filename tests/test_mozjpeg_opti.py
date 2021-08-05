import pytest

import mozjpeg_lossless_optimization


class Test_optimize(object):
    @pytest.fixture
    def image_bytes(self):
        with open("./tests/image.jpg", "rb") as file_:
            return file_.read()

    def test_optimize_returns_bytes(self, image_bytes):
        result = mozjpeg_lossless_optimization.optimize(image_bytes)
        assert type(result) == bytes

    def test_optimize_returns_a_jpeg(self, image_bytes):
        result = mozjpeg_lossless_optimization.optimize(image_bytes)
        assert result.startswith(b"\xFF\xD8\xFF\xE0\x00\x10JFIF")

    def test_optimize_returns_a_smaller_jpeg(self, image_bytes):
        result = mozjpeg_lossless_optimization.optimize(image_bytes)
        assert len(result) > 0
        assert len(result) < len(image_bytes)
