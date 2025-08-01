import pyautogui
import random
import time


def exit_fight_action():
    coor_x = 396
    coor_y = 891
    print(f"Moving to exit fight action coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )
    # Perform a realistic click
    print("Clicking exit fight action button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Exit fight action complete.")
    time.sleep(2)
    confirm_fight_action()  # Confirm the exit fight action if needed


def confirm_fight_action():
    coor_x = 888
    coor_y = 695
    print(f"Moving to confirm exit fight coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )

    # Perform a realistic click
    print("Clicking confirm exit fight button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16))  # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Confirm exit fight action complete.")