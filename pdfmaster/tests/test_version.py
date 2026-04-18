def test_version():
    import pdfmaster
    assert getattr(pdfmaster, '__version__', None) == '0.1.0'
