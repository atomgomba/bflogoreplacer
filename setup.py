#!/usr/bin/env python3
import os
from setuptools import setup

if __name__ == "__main__":
    setup(name="bflogoreplacer",
          version="0.1.2",
          description="Tools for customizing the logo in a Betaflight OSD font",
          author="Károly Kiripolszky",
          author_email="karcsi@ekezet.com",
          url="https://github.com/atomgomba/bflogoreplacer",
          packages=["bflogoreplacer"],
          scripts=['scripts/bflogoreplacer'],
          license="GPLv3",
          )
