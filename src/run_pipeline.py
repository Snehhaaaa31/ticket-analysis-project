import subprocess
import sys

scripts = [
    "src/google_sheet.py",
    "src/classify_new_tickets.py",
    "src/load_to_mysql.py",
    "src/send_email_report.py"
]

for script in scripts:
    print(f"\nRunning: {script}")

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)