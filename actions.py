import mouse
import pyautogui
import time

import config


def exit_fight_action():
    # Calculate coordinates based on percentage of the screen resolution
    # Original coordinates were (396, 891) on a 1920x1080 screen.
    coor_x = config.exit_fight_coord[0]
    coor_y = config.exit_fight_coord[1]

    mouse.move_click(coor_x, coor_y, "exit fight")

    time.sleep(2)  # Wait a bit before confirming the exit
    confirm_fight_action()  # Confirm the exit action


def confirm_fight_action():
    coor_x = config.confirm_fight_coord[0]
    coor_y = config.confirm_fight_coord[1]

    mouse.move_click(coor_x, coor_y, "confirm exit fight")
    

def close_fight():
    coor_x = config.close_fight_coord[0]
    coor_y = config.close_fight_coord[1]

    mouse.move_click(coor_x, coor_y, "close fight")


def capture_action():
    # Original coordinates: (962, 146) on 1920x1080
    time.sleep(2)  # Wait for the screen to stabilize
    coor_x = config.capture_action_coord[0]
    coor_y = config.capture_action_coord[1]

    mouse.move_click(coor_x, coor_y, "capture action")


def okay_action():
    # Original coordinates: (913, 624) on 1920x1080
    coor_x = config.okay_action_coord[0]
    coor_y = config.okay_action_coord[1]

    mouse.move_click(coor_x, coor_y, "okay action")


def keep_action():
    # Original coordinates: (875, 682) on 1920x1080
    coor_x = config.keep_action_coord[0]
    coor_y = config.keep_action_coord[1]

    mouse.move_click(coor_x, coor_y, "keep action")


def release_action():
    # Original coordinates: (1033, 678) on 1920x1080
    coor_x = config.release_action_coord[0]
    coor_y = config.release_action_coord[1]

    mouse.move_click(coor_x, coor_y, "release action")
    time.sleep(2)  # Wait before confirming
    confirm_action()


def confirm_action():
    # Original coordinates: (903, 615) on 1920x1080
    coor_x = config.confirm_action_coord[0]
    coor_y = config.confirm_action_coord[1]

    mouse.move_click(coor_x, coor_y, "confirm release action")


def heal_action():
    time.sleep(2)  # Wait for screen to stabilize
    # Original coordinates: (1200, 60) on 1920x1080
    coor_x = config.heal_action_coord[0]
    coor_y = config.heal_action_coord[1]

    mouse.move_click(coor_x, coor_y, "heal action")
    time.sleep(2)  # Wait for heal action to process
    confirm_action()

def get_clear_view_action():
    coor_x = config.get_clear_view_coord[0]
    coor_y = config.get_clear_view_coord[1]

    mouse.move_click(coor_x, coor_y, "clear view action")


def perform_attack(attack_coordinates):
    coor_x = attack_coordinates[0]
    coor_y = attack_coordinates[1]

    mouse.move_click(coor_x, coor_y, "attack")


def move_left_attack_page():
    coor_x = config.move_left_attack_page_coord[0]
    coor_y = config.move_left_attack_page_coord[1]

    mouse.move_click(coor_x, coor_y, "move left attack page")


def okay_success_mission():
    coor_x = config.okay_success_coord[0]
    coor_y = config.okay_success_coord[1]

    mouse.move_click(coor_x, coor_y, "okay success mission")

def okay_rank_up():
    coor_x = config.okay_rank_up_coord[0]
    coor_y = config.okay_rank_up_coord[1]

    mouse.move_click(coor_x, coor_y, "okay rank up")


def train_miscrit2():
    coor_x = config.train_miscrit2_coord[0]
    coor_y = config.train_miscrit2_coord[1]

    mouse.move_click(coor_x, coor_y, "train miscrit2 button")

def train_miscrit3():
    coor_x = config.train_miscrit3_coord[0]
    coor_y = config.train_miscrit3_coord[1]

    mouse.move_click(coor_x, coor_y, "train miscrit3 button")

def train_miscrit4():
    coor_x = config.train_miscrit4_coord[0]
    coor_y = config.train_miscrit4_coord[1]

    mouse.move_click(coor_x, coor_y, "train miscrit4 button")

def train_now_action():
    coor_x = config.train_now_coord[0]
    coor_y = config.train_now_coord[1]

    mouse.move_click(coor_x, coor_y, "train action")

def platinum_action():
    coor_x = config.platinum_action_coord[0]
    coor_y = config.platinum_action_coord[1]

    mouse.move_click(coor_x, coor_y, "platinum action")


def continue_train_action():
    coor_x = config.continue_action_coord[0]
    coor_y = config.continue_action_coord[1]

    mouse.move_click(coor_x, coor_y, "continue train action")

def continue_plat_train_action():
    coor_x = config.continue_plat_train_action_coord[0]
    coor_y = config.continue_plat_train_action_coord[1]

    mouse.move_click(coor_x, coor_y, "continue platinum train action")

def new_attack_continue():
    coor_x = config.new_attack_continue_coord[0]
    coor_y = config.new_attack_continue_coord[1]

    mouse.move_click(coor_x, coor_y, "new attack continue")

def close_train_page():
    coor_x = config.close_train_page_coord[0]
    coor_y = config.close_train_page_coord[1]

    mouse.move_click(coor_x, coor_y, "close train page")


def okay_evolve_miscrit():
    coor_x = config.okay_evolve_miscrit_coord[0]
    coor_y = config.okay_evolve_miscrit_coord[1]

    mouse.move_click(coor_x, coor_y, "okay evolve miscrit")


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