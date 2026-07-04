"""Run dbt-lite SQL transforms against DuckDB."""

from config import TRANSFORM
from utils import get_connection, run_sql_files


def main() -> None:
    conn = get_connection()
    print("Running staging transforms...")
    run_sql_files(conn, TRANSFORM / "staging")
    print("Running mart transforms...")
    run_sql_files(conn, TRANSFORM / "marts")
    conn.close()
    print("Transforms complete.")


if __name__ == "__main__":
    main()
