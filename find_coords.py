# ==============================================================================
#  STEP 1: FIND YOUR COORDINATES
# ==============================================================================
import pyautogui
import time
import random

# ==============================================================================
#  STEP 1: FIND YOUR COORDINATES
# ==============================================================================
def find_coordinates():
    """
    An interactive tool to display the current (X, Y) coordinates of the mouse.
    """
    print("--- Coordinate Finder Mode ---")
    print("Move your mouse over the desired location on the screen.")
    print("Press Ctrl+C in this terminal window to stop.")
    
    try:
        while True:
            # Get and display the current mouse position
            x, y = pyautogui.position()
            position_str = f"X: {str(x).rjust(4)}  Y: {str(y).rjust(4)}"
            
            # Print the line and use '\r' to overwrite it on the next loop
            # This prevents spamming the console
            print(position_str, end='\r')
            time.sleep(0.1) # A short delay to prevent high CPU usage
            
    except KeyboardInterrupt:
        print("\n\nCoordinate Finder stopped.")
        print("Now, update the ATTACK_X and ATTACK_Y variables in the script.")


