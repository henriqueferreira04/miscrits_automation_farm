
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
    "Dark Squibee": "Rare",
    "Frostmite": "Common",
    "Dark Kiloray": "Rare",
    "Cadbunny": "Exotic",
    "Mistraxol": "Common",
    "Orbling": "Common",
    "Zappup": "Common",
    "Dark Arigato": "Rare",
    "Bubbles": "Common",
    "Lavarila": "Common",
    "Shellbee": "Common",
    "Elefauna": "Common",
    "Flameling": "Common",
    "Quirk": "Common",
    "Lil Bubs": "Rare",
    "Dark Lavarila": "Rare",
    "Dark Tulipinny": "Epic",
    "Echino": "Common",
    "Wavesling": "Common",
    "Sparkitten": "Common",
    "Arigato": "Common",
    "Hippoke": "Common",
    "Ignios": "Rare",
    "Dark Sparkitten": "Rare",
    "Pamboo": "Rare",
    "Light Crickin": "Exotic",
    "Dark Frostmite": "Rare",
    "Freezet": "Common",
    "Frozy": "Common",
    "Dark Breezycheeks": "Rare",
    "Wooly": "Legendary",
    "Statikat": "Common",
    "Equestrion": "Common",
    "Drilldent": "Common",
    "Kiloray": "Common",
    "Breezycheeks": "Common",
    "Mumbah": "Common",
    "Octavio": "Epic",
    "Opigum": "Rare",
    "Luna": "Rare",
    "Poltergust": "Rare",
    "Wooly": "Legendary",
    "Wooly": "Legendary",
}

rarity_percentages = {
    "Common": [27, 30, 31],
    "Rare": [17, 20, 21],
    "Exotic": [0],
    "Epic": [0],
    "Legendary": [0],
}

exception_miscrits = ["Aebex", "Mistraxol"]

capture_miscrits = ["Dark Breezycheeks"]




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
                    

                    if percentage in rarity_percentages[rarity] or miscrit_dict["name"] in capture_miscrits:
                        print(f"Capture {keyword} with rarity {rarity} and percentage {percentage}%")

                        if keyword in exception_miscrits:
                            miscrit_dict["rarity"] = "Exception"
                        
                        return miscrit_dict
            
            else:
                print(f"Capture {keyword} with rarity {rarity} (Exotic)")
                return miscrit_dict
    return None


def capture_decision(percentage, rarity):
    if isinstance(percentage, int):
        
        if rarity == "Exotic" or rarity == "Epic" or rarity == "Legendary":
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