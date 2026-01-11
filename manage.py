#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


# =========================
# LOAD .ENV EXPLICITAMENTE
# =========================

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / "env" / ".env"

load_dotenv(dotenv_path=ENV_PATH)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    load_dotenv()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
