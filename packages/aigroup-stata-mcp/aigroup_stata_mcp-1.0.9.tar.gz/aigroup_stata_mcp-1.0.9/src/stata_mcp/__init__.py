#!/usr/bin/python3
# -*- coding: utf-8 -*-


from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("aigroup-stata-mcp")
except PackageNotFoundError:
    # Fallback for development mode when package is not installed
    __version__ = "1.0.9"

__author__ = "jackdark425 <jackdark425@gmail.com>"
__team__ = "aigroup"


if __name__ == "__main__":
    print(f"Hello aigroup-stata-mcp@version{__version__}")