import ocr_analyser
import actions
import easyocr

def win_fight_popup(reader):
    text = ocr_analyser.run_automated_ocr_easyocr(
                reader=reader,
                horizontal_start_percent=30, horizontal_end_percent=40,
                vertical_start_percent=20, vertical_end_percent=26
            )
    if "You Win" in text:
        print("🟢 Rank Up successful!")
        actions.close_fight()
        return True
    else:
        print("🔴 Rank Up failed.")
        return False
    


def lose_fight_popup(reader):
    text = ocr_analyser.run_automated_ocr_easyocr(
                reader=reader,
                horizontal_start_percent=30, horizontal_end_percent=40,
                vertical_start_percent=20, vertical_end_percent=26
            )
    if "Lose" in text:
        print("🔴 Rank Down successful!")
        actions.close_fight()
        return True
    else:
        print("🟢 Rank Down failed.")
        return False


if __name__ == "__main__":
    reader = easyocr.Reader(['en'])
    win_fight_popup(reader)