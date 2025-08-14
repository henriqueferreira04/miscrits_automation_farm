import ocr_analyser
import actions


def mission_success(reader):
    text = ocr_analyser.run_automated_ocr_easyocr(
                reader=reader,
                horizontal_start_percent=30, horizontal_end_percent=50,
                vertical_start_percent=30, vertical_end_percent=40
            )
    if "Success" in text:
        print("🟢 Mission completed successfully!")
        actions.okay_success_mission()
        return True
    else:
        print("🔴 Mission failed.")
        return False


