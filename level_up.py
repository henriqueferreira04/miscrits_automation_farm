import ocr_analyser
import actions


def rank_up_character(reader):
    text = ocr_analyser.run_automated_ocr_easyocr(
                reader=reader,
                horizontal_start_percent=43, horizontal_end_percent=55,
                vertical_start_percent=28, vertical_end_percent=35
            )
    if "Rank Up" in text:
        print("🟢 Rank Up successful!")
        actions.okay_rank_up()
        return True
    else:
        print("🔴 Rank Up failed.")
        return False

