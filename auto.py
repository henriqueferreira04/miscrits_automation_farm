
import warnings
import time
import capture
import click_bush  # Import the bush-clicking module
import attack
import actions
import health_percentage_detector
import keep_release
import ocr_analyser
import easyocr
import sys

# Suppress PyTorch MPS warnings on Apple Silicon
warnings.filterwarnings("ignore", message=".*pin_memory.*not supported on MPS.*", category=UserWarning)

def disable_print():
    sys.stdout = open('/dev/null', 'w')

def enable_print():
    sys.stdout = sys.__stdout__




# --- Main execution block ---
if __name__ == '__main__':
    disable_print()  # Disable print statements for cleaner output
    reader = easyocr.Reader(['en']) # Specify English language
    SPOT_IMAGES = ['images/shurikoon.png', 'images/shurikoon2.png', 'images/shurikoon3.png']

    while True:
        click_bush.run_spot_clicker(reader, SPOT_IMAGES)  # Run the bush-clicking function
        
        while True:
            text = ocr_analyser.run_automated_ocr_easyocr(reader=reader)

            miscrit_info = capture.is_to_capture(text)
            if not miscrit_info or miscrit_info["rarity"] != "Error":
                break


        need_to_heal = health_percentage_detector.is_health_critical()
        
        captured = False
        if miscrit_info:
            print("🟢 Capturable item detected! Proceeding with bush clicker...")
            while True: 
                text = ocr_analyser.run_automated_ocr_easyocr(reader=reader)

                if text:
                    percentage = text.split(" ")[-1][0:-1]
                    if percentage.isdigit():
                        percentage = int(percentage)
                    capture_result = capture.capture_decision(miscrit_name=miscrit_info["name"], percentage=percentage, rarity=miscrit_info["rarity"])

                    if capture_result == 1:
                        print("🟢 Capturable item detected! Proceeding with capture...")
                        actions.capture_miscrit()

                        captured = True

                    elif capture_result == 0:
                        print("🟢⚔️ Capturable item detected. Proceeding with first attack...")
                        actions.perform_attack(attack.first_attack)
                    elif capture_result == 2:
                        print("🟢⚔️ Capturable item detected! Proceeding with forth attack...")
                        actions.perform_attack(attack.forth_attack)
                else:
                    break
            
        else:
            #ctions.exit_fight_action()
            while True:
                text = ocr_analyser.run_automated_ocr_easyocr(reader=reader)   
                if text:
                    actions.perform_attack(attack.first_attack)
                else:
                    break

        actions.close_fight()

        print("🟢 Fight closed successfully.")
        time.sleep(2)

        '''
        for miscrit in captured_miscrits:
            rarity = miscrit["rarity"]
            percentage = miscrit["class"]

            if rarity == "Exotic":
                print("🟢 Exotic miscrit captured successfully!")
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

            captured_miscrits.remove(miscrit)
        '''
        if captured:
            keep_release.keep_release_miscrit(reader, miscrit_information=miscrit_info)
        
        if need_to_heal:
            print("🟢 Healing miscrit...")
            actions.heal_action()


        

