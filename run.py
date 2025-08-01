import subprocess
import time
import sys

# ==============================================================================
#  CONFIGURATION
# ==============================================================================

# --- The filename of the script you want to run and monitor ---
SCRIPT_TO_RUN = "auto.py"  # <--- CHANGE THIS to your bot's filename

# --- How many seconds to wait before restarting the script after a crash ---
RESTART_DELAY = 5 

# ==============================================================================
#  CORE LOGIC (You shouldn't need to edit below this line)
# ==============================================================================

def run_script():
    """
    This function continuously runs the target script.
    If the script exits with an error (crashes), it waits and restarts it.
    """
    try:
        while True:
            print(f"\n{'='*20} [RUNNER] Starting '{SCRIPT_TO_RUN}' {'='*20}")
            
            # We use sys.executable to ensure we run the script with the same
            # Python interpreter that is running this runner script.
            # This avoids issues with virtual environments or multiple Python versions.
            process = subprocess.Popen([sys.executable, SCRIPT_TO_RUN])
            
            # Wait for the script to finish
            process.wait()
            
            # If we get here, the script has finished or crashed.
            # We check the return code to see what happened.
            # A return code of 0 usually means it exited cleanly.
            # Any other number means it likely crashed or had an error.
            if process.returncode != 0:
                print(f"\n{'!'*20} [RUNNER] WARNING: Script crashed or exited with an error (Code: {process.returncode}) {'!'*20}")
                print(f"[RUNNER] Restarting in {RESTART_DELAY} seconds...")
                time.sleep(RESTART_DELAY)
            else:
                print(f"\n{'='*20} [RUNNER] Script finished successfully. Exiting runner. {'='*20}")
                # If the script finishes without error, we break the loop.
                # If you want it to restart even on a successful exit,
                # you can add the same delay/restart logic here.
                break

    except KeyboardInterrupt:
        # This allows you to stop the runner script with Ctrl+C
        print("\n[RUNNER] Keyboard interrupt detected. Shutting down.")
    except FileNotFoundError:
        print(f"\n[RUNNER] ERROR: Cannot find the script '{SCRIPT_TO_RUN}'.")
        print("[RUNNER] Please make sure the filename is correct and it's in the same folder.")
    except Exception as e:
        print(f"\n[RUNNER] An unexpected error occurred in the runner: {e}")

if __name__ == "__main__":
    run_script()