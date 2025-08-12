import pyautogui
import random
import time

def move_click(percentage_x, percentage_y, action):
    print(f"Moving to confirm {action} coordinates: ({percentage_x}, {percentage_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        percentage_x,
        percentage_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )

    # Perform a realistic click
    print(f"Clicking confirm {action} button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16))  # Hold the click briefly
    pyautogui.mouseUp()

    print(f"✅ Confirm {action} action complete.")