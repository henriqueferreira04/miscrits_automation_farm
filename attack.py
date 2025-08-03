import pyautogui
import time
import random
import sys

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


# ==============================================================================
#  STEP 2: PERFORM THE ATTACK
# ==============================================================================

strong_attack = [564, 1020]
basic_attack = [1334, 1020]
third_attack = [1093, 1003]
def perform_attack(attack_coordinates):
    """
    Moves to the specified coordinates and performs a realistic click.
    """
    x, y = attack_coordinates
    print(f"Moving to attack coordinates: ({x}, {y})")
    
    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        x, 
        y, 
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )
    
    # Perform a realistic click
    print("Clicking attack button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()
    
    print("✅ Attack complete.")

