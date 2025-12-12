import sys
import unittest
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vertical_python import encode_py_to_vpy, rotate


class TestEncodeDecode(unittest.TestCase):
    def test_module_roundtrip(self):
        """Test that encoding and decoding the module itself produces the original."""
        module_path = (
            Path(__file__).parent.parent / "src" / "vertical_python" / "__init__.py"
        )
        original = module_path.read_text()

        # Encode: .py -> .vpy
        encoded = encode_py_to_vpy(original)

        # Decode: .vpy -> .py
        decoded = rotate(encoded)

        # Normalize whitespace (strip trailing spaces from each line)
        original_lines = [line.rstrip() for line in original.splitlines()]
        decoded_lines = [line.rstrip() for line in decoded.splitlines()]

        self.assertEqual(decoded_lines, original_lines)


if __name__ == "__main__":
    unittest.main()
