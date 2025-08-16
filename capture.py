import actions
import json
import os

# Load Miscrits data from JSON file
def load_miscrits_data():
    """Load Miscrits data from the JSON configuration file."""
    json_path = os.path.join(os.path.dirname(__file__), 'miscrits.json')
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return data['miscrits_dict_rarity'], data['rarity_percentages']
    except FileNotFoundError:
        print(f"Warning: {json_path} not found. Using fallback data.")
        return {}, {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {json_path}. Using fallback data.")
        return {}, {}

# Load data at module import
miscrits_dict_rarity, rarity_percentages = load_miscrits_data()

exception_miscrits = ["Aebex", "Mistraxol", "Dark Breezycheeks", "Shurikoon", "Vhisp"]
capture_miscrits = ["Dark Breezycheeks"]


count = 0

def is_to_capture(text):
    """
    Detects and captures specific keywords from the OCR text.
    """
    miscrit_dict = {}
    global count
    for keyword, rarity in miscrits_dict_rarity.items():
        if keyword in text:
            print(f"Detected '{keyword}' with rarity: {rarity}")
            miscrit_dict["name"] = keyword
            miscrit_dict["rarity"] = rarity
            miscrit_dict["class"] = 0

            with open("captured_miscrits.txt", "a") as file:  #save in file txt the miscrits name detected with the automation
                count += 1
                if count < 20:
                    file.write(f"{miscrit_dict['name']}, \t")
                else:
                    file.write(f"{miscrit_dict['name']}, \n")
                    count = 0

            if rarity == "Common" or rarity == "Rare":
                percentage = text.split(" ")[-1]
                if "%" not in percentage:
                    miscrit_dict["rarity"] = "Error"
                    return miscrit_dict
                
                percentage = percentage[0:-1]  # Get the last word and remove the '%' sign
                
                if percentage.isdigit():
                    percentage = int(percentage)
                    miscrit_dict["class"] = percentage
                    

                    if percentage in rarity_percentages[rarity] or miscrit_dict["name"] in capture_miscrits:
                        print(f"Capture {keyword} with rarity {rarity} and percentage {percentage}%")

                        if keyword in exception_miscrits:
                            miscrit_dict["rarity"] = "Exception"
                        
                        return miscrit_dict
            
            else:       
                print(f"Capture {keyword} with rarity {rarity} (Exotic)")

                return miscrit_dict
    
    with open("captured_miscrits.txt", "a") as file:    #save in file txt the miscrits name not detected with the automation 
        file.write(f"{text}, \t")                       #trying to find if miscrit is not detecting name correctly
        count += 1
    return None


def capture_decision(miscrit_name, percentage, rarity):
    if isinstance(percentage, int):
        if rarity == "Exotic" or rarity == "Epic":
            if percentage > 85:
                return 1
            if miscrit_name in exception_miscrits:
                return 2
            if percentage > 30:
                return 2
        elif rarity == "Exception":
            if percentage > 95:
                return 1
            return 2
        
        elif rarity == "Legendary":
            if percentage > 70:
                return 1
            else:
                actions.move_left_attack_page()
                actions.move_left_attack_page()
                return 2
            
        else:
            if percentage > 95:
                return 1
            if percentage > 35:
                return 2
        

    return 0