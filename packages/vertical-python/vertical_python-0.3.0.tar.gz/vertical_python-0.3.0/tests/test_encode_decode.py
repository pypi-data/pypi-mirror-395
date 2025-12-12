from pathlib import Path

from vertical_python import encode_py_to_vpy, rotate


def test_module_roundtrip():
    """Test that encoding and decoding the module itself produces the original."""
    module_path = Path(__file__)
    original = module_path.read_text()

    # Encode: .py -> .vpy
    encoded = encode_py_to_vpy(original)

    # Decode: .vpy -> .py
    decoded = rotate(encoded)

    # Normalize whitespace (strip trailing spaces from each line)
    original_lines = [line.rstrip() for line in original.splitlines()]
    decoded_lines = [line.rstrip() for line in decoded.splitlines()]

    assert decoded_lines == original_lines
