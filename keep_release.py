import ocr_analyser
import actions
import detect_redspeed
import easyocr
import time

def keep_release_miscrit(reader, miscrit_information=None):
    text = ocr_analyser.run_automated_ocr_easyocr(
                reader=reader,
                horizontal_start_percent=46, horizontal_end_percent=58,
                vertical_start_percent=35, vertical_end_percent=40
            )
    if "Captured" in text:
        if not miscrit_information:
            print("No miscrit information provided, proceeding with keep action...")
            actions.keep_action()
            return
        
        rarity = miscrit_information["rarity"]
        percentage = miscrit_information["class"]

        if rarity == "Exotic" or rarity == "Epic" or rarity == "Legendary":
            print("🟢 Exotic, Epic, or Legendary miscrit captured successfully!")
            actions.keep_action()

        elif percentage in (27, 17):
            print("🟢 Common or Rare miscrit captured successfully!")
            actions.keep_action()

        elif detect_redspeed.run_red_speed_detector():
            print("🟢 Red speed action completed successfully.")
            actions.keep_action()

        else:
            print("🔴 No red speed detected. Proceeding with release action...")
            actions.release_action()

        time.sleep(2)
        
        return True

    else:
        return False


    

if __name__ == "__main__":
    # Example usage
    reader = easyocr.Reader(['en'])
    miscrit_info = {"rarity": "Common", "class": 30}  # Example miscrit information
    keep_release_miscrit(reader, miscrit_information=miscrit_info)
