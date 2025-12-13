import epsf


def test_epsf_version():
    from importlib.metadata import version

    # For editable installs, you might just need to re-install if this fails
    assert epsf.__version__ == version("epsf")
