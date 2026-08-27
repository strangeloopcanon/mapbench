"""Regression tests for the MapBench release validator."""

from __future__ import annotations

import struct
import tempfile
import unittest
from pathlib import Path

from scripts import validate_release


class ValidatorTests(unittest.TestCase):
    def test_require_raises_explicit_error(self) -> None:
        with self.assertRaisesRegex(validate_release.ValidationError, "broken invariant"):
            validate_release.require(False, "broken invariant")

    def test_score_bands_include_boundaries(self) -> None:
        cases = {
            100: "excellent",
            90: "excellent",
            89.5: "good",
            75: "good",
            74: "usable_draft",
            60: "usable_draft",
            59: "misleading",
            40: "misleading",
            39: "substantive_failure",
            21: "substantive_failure",
            20: "not_usable",
            0: "not_usable",
        }
        for score, expected in cases.items():
            with self.subTest(score=score):
                self.assertEqual(validate_release.band(score), expected)

    def test_image_info_reads_png_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.png"
            path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + struct.pack(">I", 13)
                + b"IHDR"
                + struct.pack(">II", 640, 480)
            )
            self.assertEqual(validate_release.image_info(path), ("image/png", 640, 480))

    def test_image_info_rejects_unknown_encoding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.png"
            path.write_bytes(b"not an image")
            with self.assertRaisesRegex(validate_release.ValidationError, "unsupported image encoding"):
                validate_release.image_info(path)


if __name__ == "__main__":
    unittest.main()
