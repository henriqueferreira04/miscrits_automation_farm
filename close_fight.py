# ==============================================================================
#  STEP 1: FIND YOUR COORDINATES
# ==============================================================================
import pyautogui
import time
import random


def close_fight():
    coor_x = 949
    coor_y = 838
    print(f"Moving to continue coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )
    
    # Perform a realistic click
    print("Clicking continue button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Continue action complete.")

