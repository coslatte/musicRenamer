#!/usr/bin/env python
"""
Punto de entrada principal para la aplicación Music Renamer.
Este script simplemente invoca la interfaz de línea de comandos.
"""

from core.cli import Cli

if __name__ == "__main__":
    cli = Cli()
    cli.main()
