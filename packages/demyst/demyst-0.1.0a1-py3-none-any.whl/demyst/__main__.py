#!/usr/bin/env python3
"""
Demyst: The Scientific Integrity Platform

This module provides the entry point for running demyst as a module:
    python -m demyst

It delegates to the main CLI interface.
"""

import sys

from demyst.cli import main

if __name__ == "__main__":
    sys.exit(main())
