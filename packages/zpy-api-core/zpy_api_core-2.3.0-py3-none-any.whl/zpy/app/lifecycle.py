import signal
import sys
import traceback

# Variable interna
_shutdown_callback = None

def _sigterm_handler(signum, frame):
    """
    Robust handler for SIGTERM.
    Attempts to execute cleanup, captures any errors, and forces exit.
    """
    print(f"[ZurckzPy] SIGTERM signal received ({signum}). Starting shutdown...", flush=True)

    try:
        if _shutdown_callback:
            print(" 💥 [ZurckzPy] Executing cleanup callback...", flush=True)
            _shutdown_callback()
            print(" 💥 [ZurckzPy] Cleanup completed successfully.", flush=True)
        else:
            print("[ZurckzPy] No cleanup callback registered.", flush=True)
            
    except Exception as e:
        # Protection: If destroy() fails, we don't break the runtime.
        print(f"[ZurckzPy] ⚠️ CRITICAL ERROR during cleanup: {e}", flush=True)
        # Print full stack trace for debugging in CloudWatch
        traceback.print_exc()
        
    finally:
        # This ALWAYS executes, error or not.
        # It's vital to tell the runtime we're done.
        print("[ZurckzPy] Closing process (sys.exit).", flush=True)
        sys.exit(0)

def register_shutdown(callback):
    """
    Registers the cleanup function.
    """
    global _shutdown_callback
    _shutdown_callback = callback
    signal.signal(signal.SIGTERM, _sigterm_handler)
    # We don't print anything here to keep cold-start logs clean,
    # unless debugging is necessary.