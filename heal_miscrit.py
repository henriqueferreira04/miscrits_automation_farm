import pyautogui
import random
import time
from capture_action import confirm_action


def heal_action():
    time.sleep(2)  # Wait for the screen to stabilize before moving the mouse
    coor_x = 1200
    coor_y = 60
    print(f"Moving to heal action coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )
    # Perform a realistic click
    print("Clicking heal action button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Heal action complete.")
    confirm_action()  # Confirm the heal action if needed

