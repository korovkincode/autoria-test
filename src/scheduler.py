from dotenv import dotenv_values
import schedule, time, subprocess, sys
from pathlib import Path
import utils
import os

CONFIG = dotenv_values(".env")


def run_script(path):
    try:
        subprocess.run(
            [sys.executable, str(path)],
            capture_output=True, text=True, check=True
        )

        dump_date = utils.converted_time("date").replace("/", "-")
        dump_db(
            db_name=CONFIG["PGNAME"],
            user=CONFIG["PGUSER"],
            host="localhost",
            port=5432,
            output_file=f"dumps/{dump_date}.dump"
        )
    except subprocess.CalledProcessError as e:
        print(f"Script failed with code {e.returncode}:\n{e.stderr}")


def dump_db(db_name, user, host, port, output_file):
    command = [
        "pg_dump",
        "-h", host,
        "-p", str(port),
        "-U", user,
        "-F", "c",             # custom format for dump
        "-f", output_file,
        db_name,
    ]
    env = {
        **os.environ,
        "PGPASSWORD": CONFIG["PGPASSWORD"]
    }

    subprocess.run(command, check=True, env=env)
    print(f"Database dumped to {output_file}")


if __name__ == "__main__":
    script_path = Path("main.py")
    if not script_path.is_file():
        print(f"Script not found: {script_path}")
        exit(1)

    schedule.every().day.at(CONFIG["START_TIME"]).do(run_script, path=script_path)

    while True:
        schedule.run_pending()
        time.sleep(30)