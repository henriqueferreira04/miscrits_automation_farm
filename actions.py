import mouse
import pyautogui
import time


def exit_fight_action():
    # Calculate coordinates based on percentage of the screen resolution
    # Original coordinates were (396, 891) on a 1920x1080 screen.
    coor_x = int(pyautogui.size().width * (396 / 1920)) 
    coor_y = int(pyautogui.size().height * (891 / 1080))  

    mouse.move_click(coor_x, coor_y, "exit fight")

    time.sleep(2)  # Wait a bit before confirming the exit
    confirm_fight_action()  # Confirm the exit action


def confirm_fight_action():
    coor_x = int(pyautogui.size().width * (888 / 1920)) 
    coor_y = int(pyautogui.size().height * (695 / 1080)) 

    mouse.move_click(coor_x, coor_y, "confirm exit fight")
    

def close_fight():
    coor_x = int(pyautogui.size().width * (949 / 1920)) 
    coor_y = int(pyautogui.size().height * (838 / 1080)) 

    mouse.move_click(coor_x, coor_y, "close fight")


def capture_action():
    # Original coordinates: (962, 146) on 1920x1080
    coor_x = int(pyautogui.size().width * (962 / 1920))
    coor_y = int(pyautogui.size().height * (146 / 1080))

    mouse.move_click(coor_x, coor_y, "capture action")


def okay_action():
    # Original coordinates: (913, 624) on 1920x1080
    coor_x = int(pyautogui.size().width * (913 / 1920))
    coor_y = int(pyautogui.size().height * (624 / 1080))

    mouse.move_click(coor_x, coor_y, "okay action")


def keep_action():
    # Original coordinates: (875, 682) on 1920x1080
    coor_x = int(pyautogui.size().width * (875 / 1920))
    coor_y = int(pyautogui.size().height * (682 / 1080))

    mouse.move_click(coor_x, coor_y, "keep action")


def release_action():
    # Original coordinates: (1033, 678) on 1920x1080
    coor_x = int(pyautogui.size().width * (1033 / 1920))
    coor_y = int(pyautogui.size().height * (678 / 1080))

    mouse.move_click(coor_x, coor_y, "release action")
    time.sleep(2)  # Wait before confirming
    confirm_action()


def confirm_action():
    # Original coordinates: (903, 615) on 1920x1080
    coor_x = int(pyautogui.size().width * (903 / 1920))
    coor_y = int(pyautogui.size().height * (615 / 1080))

    mouse.move_click(coor_x, coor_y, "confirm release action")


def heal_action():
    time.sleep(2)  # Wait for screen to stabilize
    # Original coordinates: (1200, 60) on 1920x1080
    coor_x = int(pyautogui.size().width * (1200 / 1920))
    coor_y = int(pyautogui.size().height * (60 / 1080))

    mouse.move_click(coor_x, coor_y, "heal action")
    time.sleep(2)  # Wait for heal action to process
    confirm_action()

def get_clear_view_action():
    coor_x = int(pyautogui.size().width * (921/1920))
    coor_y = int(pyautogui.size().height * (305/1080))

    mouse.move_click(coor_x, coor_y, "clear view action")


def perform_attack(attack_coordinates):
    coor_x = int(pyautogui.size().width * (attack_coordinates[0] / 1920))
    coor_y = int(pyautogui.size().height * (attack_coordinates[1] / 1080))
    
    mouse.move_click(coor_x, coor_y, "attack")


def move_left_attack_page():
    coor_x = int(pyautogui.size().width * (1519/1920))
    coor_y = int(pyautogui.size().height * (1010/1080))

    mouse.move_click(coor_x, coor_y, "move left attack page")


def okay_success_mission():
    coor_x = int(pyautogui.size().width * (949/1920))
    coor_y = int(pyautogui.size().height * (666/1080))

    mouse.move_click(coor_x, coor_y, "okay success mission")

def okay_rank_up():
    coor_x = int(pyautogui.size().width * (955/1920))
    coor_y = int(pyautogui.size().height * (739/1080))

    mouse.move_click(coor_x, coor_y, "okay rank up")


def train_miscrit2():
    coor_x = int(pyautogui.size().width * (604/1920))
    coor_y = int(pyautogui.size().height * (50/1080))

    mouse.move_click(coor_x, coor_y, "train miscrit2 button")

def train_miscrit3():
    coor_x = int(pyautogui.size().width * (663/1920))
    coor_y = int(pyautogui.size().height * (50/1080))

    mouse.move_click(coor_x, coor_y, "train miscrit3 button")

def train_miscrit4():
    coor_x = int(pyautogui.size().width * (722/1920))
    coor_y = int(pyautogui.size().height * (50/1080))

    mouse.move_click(coor_x, coor_y, "train miscrit4 button")

def train_now_action():
    coor_x = int(pyautogui.size().width * (982/1920))
    coor_y = int(pyautogui.size().height * (218/1080))

    mouse.move_click(coor_x, coor_y, "train action")

def platinum_action():
    coor_x = int(pyautogui.size().width * (898/1920))
    coor_y = int(pyautogui.size().height * (898/1080))

    mouse.move_click(coor_x, coor_y, "platinum action")


def continue_train_action():
    coor_x = int(pyautogui.size().width * (1150/1920))
    coor_y = int(pyautogui.size().height * (894/1080))

    mouse.move_click(coor_x, coor_y, "continue train action")

def continue_plat_train_action():
    coor_x = int(pyautogui.size().width * (962/1920))
    coor_y = int(pyautogui.size().height * (896/1080))

    mouse.move_click(coor_x, coor_y, "continue platinum train action")

def new_attack_continue():
    coor_x = int(pyautogui.size().width * (1115/1920))
    coor_y = int(pyautogui.size().height * (697/1080))

    mouse.move_click(coor_x, coor_y, "new attack continue")

def close_train_page():
    coor_x = int(pyautogui.size().width * (1381/1920))
    coor_y = int(pyautogui.size().height * (177/1080))

    mouse.move_click(coor_x, coor_y, "close train page")

def capture_miscrit():
    time.sleep(2)
    capture_action()
    time.sleep(6)  # Wait for the capture to process
    okay_action()
    time.sleep(6)  # Wait for the okay action to complete


def train_miscrit(miscrit, is_plat_train):
    if miscrit == 2:
        train_miscrit2()
    elif miscrit == 3:
        train_miscrit3()
    elif miscrit == 4:
        train_miscrit4()

    time.sleep(1)  # Wait for the train action to process
    train_now_action()

    time.sleep(1)  # Wait for the train now action to complete
    if is_plat_train:
        platinum_action()
        time.sleep(1)
        continue_plat_train_action()
    else:
        continue_train_action()
        time.sleep(1)
        continue_train_action()

    time.sleep(1)  # Wait for the continue action to complete
    new_attack_continue()
    time.sleep(1)  # Wait for the new attack continue action to complete
    close_train_page()

if __name__ == "__main__":
    close_fight()