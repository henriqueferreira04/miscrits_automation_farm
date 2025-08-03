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


def capture_action():
    coor_x = 962
    coor_y = 146
    print(f"Moving to capture coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )
    
    # Perform a realistic click
    print("Clicking capture button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Capture action complete.")




def okay_action():
    coor_x = 913
    coor_y = 624
    print(f"Moving to okay coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )
    
    # Perform a realistic click
    print("Clicking okay button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Okay action complete.")


def keep_action():
    coor_x = 875
    coor_y = 682
    print(f"Moving to keep coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )

    # Perform a realistic click
    print("Clicking keep button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Keep action complete.")



def release_action():
    coor_x = 1033
    coor_y = 678
    print(f"Moving to release coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )

    # Perform a realistic click
    print("Clicking release button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Release action complete.")

    time.sleep(2)  # Wait a bit before confirming the release
    confirm_action()  # Confirm the release action


def confirm_action():
    coor_x = 903
    coor_y = 615
    print(f"Moving to confirm action coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )

    # Perform a realistic click
    print("Clicking confirm action button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Confirm action complete.")




def capture_miscrit():
    time.sleep(6)
    capture_action()
    time.sleep(6)  # Wait for the capture to process
    okay_action()
    time.sleep(6)  # Wait for the okay action to complete


if __name__ == "__main__":
    find_coordinates()  # Uncomment to find coordinates