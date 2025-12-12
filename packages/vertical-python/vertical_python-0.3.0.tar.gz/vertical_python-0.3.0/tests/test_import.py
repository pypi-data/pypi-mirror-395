from vertical_python import codec


def test_codec_imports():
    """We should be able to import things with the vertical codec declared"""
    from tests.data import codec_eg

    codec_eg.hello_world()
