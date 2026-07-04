"""Run the full data pipeline: ingest, transform, export."""

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
    for script in SCRIPTS:
        print(f"\n{'=' * 60}\nRunning {script}...\n{'=' * 60}")
        result = subprocess.run(
            [sys.executable, str(PIPELINE / script)],
            cwd=str(PIPELINE),
        )
        if result.returncode != 0:
            sys.exit(result.returncode)
    print("\nPipeline finished successfully.")


if __name__ == "__main__":
    main()
