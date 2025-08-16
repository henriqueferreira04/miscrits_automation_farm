
from time import time, sleep
import actions
import health_percentage_detector
'''
def is_ready_to_train(reader):
    miscrit2 = ocr_analyser.run_automated_ocr_easyocr(reader=reader, horizontal_start_percent=41, horizontal_end_percent=50,
                             vertical_start_percent=40, vertical_end_percent=42)
    
    miscrit3 = ocr_analyser.run_automated_ocr_easyocr(reader=reader, horizontal_start_percent=31, horizontal_end_percent=40,
                             vertical_start_percent=52, vertical_end_percent=54)

    miscrit4 = ocr_analyser.run_automated_ocr_easyocr(reader=reader, horizontal_start_percent=41, horizontal_end_percent=50,
                             vertical_start_percent=52, vertical_end_percent=54)
'''



def check_need_to_train():
    miscrit2 = health_percentage_detector.is_ready_to_train(horizontal_start=40, horizontal_end=48, vertical_start=40, vertical_end=42)
    miscrit3 = health_percentage_detector.is_ready_to_train(horizontal_start=30, horizontal_end=38, vertical_start=52, vertical_end=54)
    miscrit4 = health_percentage_detector.is_ready_to_train(horizontal_start=40, horizontal_end=48, vertical_start=52, vertical_end=54)

    return (miscrit2, miscrit3, miscrit4)


if __name__ == "__main__":
    check_need_to_train()