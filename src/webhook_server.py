from flask import Flask, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_pipeline():

    print("REQUEST RECEIVED FROM N8N")

    project_dir = r"C:\Users\Lenovo\Desktop\ticket-analysis-project"

    subprocess.Popen(
        [sys.executable, os.path.join(project_dir, "src", "run_pipeline.py")],
        cwd=project_dir
    )

    return jsonify({
        "status": "started"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)