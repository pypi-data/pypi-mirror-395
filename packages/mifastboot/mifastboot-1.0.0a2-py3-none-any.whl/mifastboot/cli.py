import sys
import os
import time
import subprocess
import json

def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")

def run_worker_pc(args):
    from .worker import main as worker_main
    sys.argv = ["worker.py"] + args
    try:
        worker_main()
        return 0
    except SystemExit as e:
        return e.code

def loop_termux(args):
    while True:
        try:
            out = subprocess.check_output(["termux-usb", "-l"], text=True).strip()
            
            dev_path = None
            if out.startswith("["):
                try: 
                    data = json.loads(out)
                    if data: dev_path = data[0].get("path")
                except: pass
            elif out:
                dev_path = out.splitlines()[0]

            if not dev_path:
                time.sleep(2)
                continue

            cmd = [
                "termux-usb", "-r", dev_path, 
                "-E", sys.executable, "-m", "mifastboot.worker"
            ] + args

            proc = subprocess.run(cmd, capture_output=False)
            
            if proc.returncode == 0:
                break
            elif proc.returncode == 10:
                time.sleep(2)
            else:
                time.sleep(2)

        except Exception:
            time.sleep(2)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided"}))
        return

    args = sys.argv[1:]
    
    if is_termux():
        loop_termux(args)
    else:
        while True:
            ret = run_worker_pc(args)
            if ret == 0: break
            time.sleep(2)

if __name__ == "__main__":
    main()