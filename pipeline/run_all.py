"""Run the full data pipeline: ingest, transform, export."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

PIPELINE = Path(__file__).parent
SCRIPTS = [
    "ingest_air.py",
    "ingest_mobility.py",
    "run_transforms.py",
    "export_json.py",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full city air quality data pipeline.")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Fetch fresh SaveEcoBot data instead of using data/raw cache",
    )
    args = parser.parse_args()

    env = os.environ.copy()
    if args.refresh:
        env["PIPELINE_REFRESH"] = "1"
        print("Refresh mode: bypassing SaveEcoBot cache")

    for script in SCRIPTS:
        print(f"\n{'=' * 60}\nRunning {script}...\n{'=' * 60}")
        result = subprocess.run(
            [sys.executable, str(PIPELINE / script)],
            cwd=str(PIPELINE),
            env=env,
        )
        if result.returncode != 0:
            sys.exit(result.returncode)
    print("\nPipeline finished successfully.")


if __name__ == "__main__":
    main()
