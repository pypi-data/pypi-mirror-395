# Installation

To install `epsf`, run `python -m pip install epsf`.

## JWST1PASS PSFs

JWST1PASS PSFs must be downloaded separately, after installing `epsf`.
The PSFs are stored online under this directory: <https://www.stsci.edu/~jayander/JWST1PASS/LIB/PSFs/STDPSFs/>.
You can either manually download the PSFs you are interested in using or download them all using the helper function below. The total data size is 128M so it is usually simpler to just download everything.
Here is the snippet to download PSFs:


```python
from epsf.utils import download_jwst1pass
download_jwst1pass()
```

By default, the PSFs are downloaded under `~/.local/share/epsf/jwst1pass`.
To change the `epsf` data directory from `~/.local/share/epsf` to something else, you can set the `EPSF_PATH` environment variable in your `~/.bashrc`. Don't forget to restart your shell or to `source ~/.bashrc` before downloading!
