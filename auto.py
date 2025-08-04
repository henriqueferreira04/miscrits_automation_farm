
import capture
import attack
import close_fight
import capture_action
import detect_redspeed
import exit_fight
import find_spot
import heal_miscrit
import health_percentage_detector
import ocr_analyser


# --- Main execution block ---
if __name__ == '__main__':
    while True:
        REFERENCE_IMAGE_PATH = 'images/octavio.png' 
        find_spot.run_spot_clicker(REFERENCE_IMAGE_PATH)

        while True:
            text = ocr_analyser.run_automated_ocr_easyocr()

            miscrit_info = capture.is_to_capture(text)
            if not miscrit_info or miscrit_info["rarity"] != "Error":
                break


        need_to_heal = health_percentage_detector.is_health_critical()
        captured = False  # Initialize captured status
        if miscrit_info:
            print("🟢 Capturable item detected! Proceeding with bush clicker...")
            while True: 
                text = ocr_analyser.run_automated_ocr_easyocr()

                if text:
                    percentage = text.split(" ")[-1][0:-1]
                    if percentage.isdigit():
                        percentage = int(percentage)
                    capture_result = capture.capture_decision(percentage=percentage, rarity=miscrit_info["rarity"])
                    if capture_result == 1:
                        print("🟢 Capturable item detected! Proceeding with capture...")
                        capture_action.capture_miscrit()
                        captured = True

                    elif capture_result == 0:
                        print("🟢⚔️ Capturable item detected. Proceeding with strong attack...")
                        attack.perform_attack(attack.strong_attack)
                    elif capture_result == 2:
                        print("🟢⚔️ Capturable item detected! Proceeding with basic attack...")
                        attack.perform_attack(attack.third_attack)
                else:
                    break
            
            close_fight.close_fight()  # Close the fight if needed
            
        else:
            exit_fight.exit_fight_action()
        
        print("🟢 Fight closed successfully.")

        

        if captured:
            rarity = miscrit_info["rarity"]
            percentage = miscrit_info["class"]

            if rarity == "Exotic":
                print("🟢 Exotic miscrit captured successfully!")
                capture_action.keep_action()

            elif percentage in (27, 17):
                print("🟢 Common or Rare miscrit captured successfully!")
                capture_action.keep_action()

            elif detect_redspeed.run_red_speed_detector():
                print("🟢 Red speed action completed successfully.")
                capture_action.keep_action()

            else:
                print("🔴 No red speed detected. Proceeding with release action...")
                capture_action.release_action()

        
        if need_to_heal:
            print("🟢 Healing miscrit...")
            heal_miscrit.heal_action()

