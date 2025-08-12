
import capture
import click_bush  # Import the bush-clicking module
import attack
import detect_redspeed
import actions
import health_percentage_detector
import ocr_analyser



# --- Main execution block ---
if __name__ == '__main__':
    captured_miscrits = []  # Initialize captured status
    while True:
        click_bush.run_spot_clicker()  # Run the bush-clicking function
        
        while True:
            text = ocr_analyser.run_automated_ocr_easyocr()

            miscrit_info = capture.is_to_capture(text)
            if not miscrit_info or miscrit_info["rarity"] != "Error":
                break


        need_to_heal = health_percentage_detector.is_health_critical()
        

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
                        actions.capture_miscrit()
                        captured_miscrits.append(miscrit_info)

                    elif capture_result == 0:
                        print("🟢⚔️ Capturable item detected. Proceeding with strong attack...")
                        attack.perform_attack(attack.strong_attack)
                    elif capture_result == 2:
                        print("🟢⚔️ Capturable item detected! Proceeding with basic attack...")
                        attack.perform_attack(attack.basic_attack)
                else:
                    break
            
            actions.close_fight()
            
        else:
            actions.exit_fight_action()
        
        print("🟢 Fight closed successfully.")

        
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
        
        if need_to_heal:
            print("🟢 Healing miscrit...")
            actions.heal_action()


        

