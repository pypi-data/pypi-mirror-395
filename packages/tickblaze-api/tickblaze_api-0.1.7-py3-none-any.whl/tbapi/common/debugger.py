



import socket


class TbDebugger:
    @staticmethod
    def attach(port=5678):
        """
        Safely attach debugger to localhost on the given port.
        """
        import os

        if os.environ.get("ENABLE_TB_DEBUGGER") == "1":
            try:
                import debugpy
                if not debugpy.is_client_connected() and _is_debugger_listening(port):
                    debugpy.connect(("localhost", port))
            except Exception:
                # If debugger is not running, just continue
                pass
                
def _is_debugger_listening(port=5678, host="localhost"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.1)
        try:
            sock.connect((host, port))
            return True
        except (ConnectionRefusedError, OSError):
            return False