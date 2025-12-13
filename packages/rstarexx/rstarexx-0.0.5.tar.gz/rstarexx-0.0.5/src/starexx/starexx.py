#!/usr/bin/env python3
import subprocess, shlex
import signal, sys, threading, time
from flask import Flask, request, jsonify

app = Flask(__name__)

def cleanup(signum, frame):
    sys.exit(0)

@app.route("/", methods=["POST"])
def run_command():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No json data found"}), 400
        
        cmd = data.get("cmd", "")
        if not cmd:
            return jsonify({"error": "No command provided"}), 400
        
        try:
            result = subprocess.run(
                shlex.split(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=30
            )
            return jsonify({
                "output": result.stdout,
                "returncode": result.returncode
            })
        except subprocess.TimeoutExpired:
            return jsonify({"error": "execution timeout"}), 408
        except Exception as e:
            return jsonify({"error": f"execution failed: {str(e)}"}), 500
            
    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500

def run_server():
    app.run(
        host="0.0.0.0",
        port=7676,
        debug=False,
        threaded=True,
        use_reloader=False
    )

def main():
    print("Termux permission accepted.")
    
    signal.signal(signal.SIGINT, cleanup)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()