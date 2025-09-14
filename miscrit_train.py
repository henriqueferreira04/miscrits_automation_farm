
from time import time, sleep
import actions
import health_percentage_detector


def check_need_to_train(is_miscrit2_to_train, is_miscrit3_to_train, is_miscrit4_to_train):
    miscrit2 = 0
    miscrit3 = 0
    miscrit4 = 0

    if is_miscrit2_to_train:
        miscrit2 = health_percentage_detector.is_ready_to_train(horizontal_start=40, horizontal_end=48, vertical_start=40, vertical_end=42)
    if is_miscrit3_to_train:
        miscrit3 = health_percentage_detector.is_ready_to_train(horizontal_start=30, horizontal_end=38, vertical_start=52, vertical_end=54)
    if is_miscrit4_to_train:
        miscrit4 = health_percentage_detector.is_ready_to_train(horizontal_start=40, horizontal_end=48, vertical_start=52, vertical_end=54)

    return (miscrit2, miscrit3, miscrit4)


if __name__ == "__main__":
    check_need_to_train()