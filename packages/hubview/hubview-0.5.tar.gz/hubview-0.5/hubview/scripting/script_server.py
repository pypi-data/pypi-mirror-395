#==============================================================================#
# Imports
import argparse
import subprocess
import threading
from flask import Flask, send_from_directory, Response
import os

#==============================================================================#
# Script Runner
class ScriptRunner:
    def __init__(self, python_executable: str, script_path: str, log_file: str):
        self.python_executable = python_executable
        self.script_path = script_path
        self.log_file = log_file
        self.process = None
        self.lock = threading.Lock()
    
    def start(self):
        with self.lock:
            if self.process is not None:
                return "Already running"

            def run():
                with open(self.log_file, 'a') as log:
                    self.process = subprocess.Popen(
                        [self.python_executable, "-u", self.script_path],
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        bufsize=1,
                        close_fds=True
                    )
                    self.process.wait()
                    self.process = None

            threading.Thread(target=run, daemon=True).start()
            return "Started"

    def stop(self):
        with self.lock:
            if self.process:
                self.process.terminate()
                self.process = None
                return "Stopped"
            return "Not running"

    def get_output(self, last_n=50):
        if not os.path.exists(self.log_file):
            return ""
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
        return "".join(lines[-last_n:])

# #==============================================================================#
# # Flask Server
# class ScriptServer:
#     def __init__(self, python_executable: str, script_path: str, log_file: str, port: int = 5000):
#         self.runner = ScriptRunner(python_executable, script_path, log_file)
#         self.app = Flask(__name__)
#         self.port = port
#         self._setup_routes()

#     def _setup_routes(self):
#         @self.app.route('/')
#         def index():
#             return send_from_directory('.', 'static/index.html')

#         @self.app.route('/start', methods=['GET'])
#         def start():
#             return self.runner.start()

#         @self.app.route('/stop', methods=['GET'])
#         def stop():
#             return self.runner.stop()

#         @self.app.route('/status')
#         def status():
#             return "Running" if self.runner.process else "Stopped"

#         @self.app.route('/log', methods=['GET'])
#         def log():
#             return Response(self.runner.get_output(), mimetype='text/plain')

#     def run(self):
#         self.app.run(host="0.0.0.0", port=self.port)

#==============================================================================#
# Entry Point
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run a script server.")
#     parser.add_argument('--python', required=True, help="Python executable to use (e.g., python3)")
#     parser.add_argument('--script', required=True, help="Path to the script to run")
#     parser.add_argument('--log', required=True, help="Path to log output file")
#     parser.add_argument('--port', type=int, default=5000, help="Port to run the server on")

#     args = parser.parse_args()

#     server = ScriptServer(
#         python_executable=args.python,
#         script_path=args.script,
#         log_file=args.log,
#         port=args.port
#     )
#     server.run()

# if __name__ == "__main__":
#     py_exec = "venv/bin/python3.12"
#     py_script = "active/NetScript/netscript/netscript/tests/script_1.py"
#     app = ScriptServer(py_exec, py_script, "script_out.txt", 3000)
#     app.run()