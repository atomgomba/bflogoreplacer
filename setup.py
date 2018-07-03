#!/usr/bin/env python3
from setuptools import setup

from bflogoreplacer import __version__, __author__, __email__, __license__

if __name__ == "__main__":
    setup(name="bflogoreplacer",
          version=__version__,
          description="Tools for customizing the logo in a Betaflight OSD font",
          author=__author__,
          author_email=__email__,
          url="https://github.com/atomgomba/bflogoreplacer",
          packages=["bflogoreplacer"],
          scripts=['scripts/bflogoreplacer'],
          license=__license__,
          )
