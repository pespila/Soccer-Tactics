"""CLI entry point for soccer-tactics."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click


@click.command()
@click.option("--port", default=8501, help="Port to run the Streamlit server on.")
def main(port: int) -> None:
    """Launch the Soccer Tactics Board in your browser."""
    app_path = Path(__file__).parent / "app.py"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            str(port),
        ],
        check=True,
    )
