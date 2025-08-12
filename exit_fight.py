import pyautogui
import random
import time


def exit_fight_action():
    # Get the current screen resolution
    screen_width, screen_height = pyautogui.size()
    print(f"Current screen resolution: {screen_width}x{screen_height}")

    # Calculate coordinates based on percentage of the screen resolution
    # Original coordinates were (396, 891) on a 1920x1080 screen.
    coor_x = int(screen_width * 0.20625)  # 396 / 1920
    coor_y = int(screen_height * 0.825)    # 891 / 1080
    
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
    # This function call is assumed to exist elsewhere in your code
    # confirm_fight_action()


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


if __name__ == "__main__":
    exit_fight_action()