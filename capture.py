
miscrits_dict_rarity = {
    "Nessy": "Common",
    "Stalkra": "Common",
    "Mech": "Common",
    "Rexie": "Common",
    "Warrian": "Common",
    "Aebex": "Common",
    "Charix": "Rare",
    "Alpha": "Exotic",
    "Dark Steamguin": "Rare",
    "Dark Squibee": "Rare"
}

rarity_percentages = {
    "Common": [27, 30, 31],
    "Rare": [17, 20, 21],
    "Exotic": [0]
}

exception_miscrits = ["Aebex"]




def is_to_capture(text):
    """
    Detects and captures specific keywords from the OCR text.
    """
    miscrit_dict = {}
    for keyword, rarity in miscrits_dict_rarity.items():
        if keyword in text:
            print(f"Detected '{keyword}' with rarity: {rarity}")
            miscrit_dict["name"] = keyword
            miscrit_dict["rarity"] = rarity
            miscrit_dict["class"] = 0
            
            if rarity != "Exotic":
                percentage = text.split(" ")[-1]
                if "%" not in percentage:
                    miscrit_dict["rarity"] = "Error"
                    return miscrit_dict
                
                percentage = percentage[0:-1]  # Get the last word and remove the '%' sign
                
                if percentage.isdigit():
                    percentage = int(percentage)
                    miscrit_dict["class"] = percentage

                    if percentage in rarity_percentages[rarity]:
                        print(f"Capture {keyword} with rarity {rarity} and percentage {percentage}%")

                        if keyword in exception_miscrits:
                            miscrit_dict["rarity"] = "Exception"
                        
                        return miscrit_dict
            
            else:
                print(f"Capture {keyword} with rarity {rarity} (Exotic)")
                return miscrit_dict
    return None


def capture_decision(percentage, rarity):
    if rarity == "Exotic":
        if percentage > 85:
            return 1
        if percentage > 30:
            return 2
    elif rarity == "Exception":
        if percentage > 95:
            return 1
        return 2
    else:
        if percentage > 95:
            return 1
        if percentage > 35:
            return 2

    return 0