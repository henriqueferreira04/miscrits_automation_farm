import pyautogui
import time
import random
import os

import ocr_analyser

def find_and_click_spot(image_file, search_region, confidence_level=0.8):
    """
    Searches within a specific region of the screen for an image and clicks it.
    
    Args:
        image_file (str): The path to the image file to find.
        search_region (tuple): A 4-integer tuple (left, top, width, height) defining the search area.
        confidence_level (float): The confidence level for the image match.
        
    Returns:
        True if an image was found and clicked, False otherwise.
    """
    try:
        # The 'region' parameter restricts the search to the specified part of the screen
        bush_location = pyautogui.locateCenterOnScreen(
            image_file,
            confidence=confidence_level,
            region=search_region
        )
        
        if bush_location:
            print(f"Found '{image_file}' within the search region at: {bush_location}")
            
            # Move the mouse in a more human-like way
            pyautogui.moveTo(
                bush_location.x, 
                bush_location.y, 
                duration=random.uniform(0.2, 0.5), 
                tween=pyautogui.easeInOutQuad
            )
            
            # Perform a more realistic click
            print("Performing a more realistic click...")
            pyautogui.mouseDown()
            time.sleep(random.uniform(0.05, 0.15))
            pyautogui.mouseUp()
            
            print("✅ Successfully clicked on the bush.")
            return True
        else:
            return False
            
    except pyautogui.ImageNotFoundException:
        return False
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# --- Main part of the script ---
def run_spot_clicker():
    SPOT_IMAGE = 'images/alpha.png'
    CLICK_DELAY = 3.0

    print("Starting the bot...")
    
    # --- MODIFICATION: Define a region that covers the bottom 80% of the screen ---
    screen_width, screen_height = pyautogui.size()
    
    # Calculate the top starting point (20% down from the top)
    top_offset = int(screen_height * 0.20)
    
    # Define the search region: (left, top, width, height)
    search_region = (
        0,              # Start from the far left
        top_offset,     # Start 20% down from the top
        screen_width,   # Search the full width of the screen
        screen_height - top_offset # Search the remaining 80% of the height
    )
    
    print(f"Search area is restricted to the bottom 80% of the screen.")
    print(f"Region details: {search_region}")
    
    print("You have 3 seconds to switch to your game window...")
    time.sleep(3)

    count = 0
    while True:
        print(f"\nSearching for '{SPOT_IMAGE}' in the designated area...")
        
        # Call the function, passing the newly calculated search region
        was_successful = find_and_click_spot(SPOT_IMAGE, search_region, confidence_level=0.8)
        
        if was_successful:
            print(f"Action successful. Waiting for {CLICK_DELAY} seconds...")
            time.sleep(CLICK_DELAY)
        else:
            count += 1
            if count > 10:
                get_clear_view_action()
                count = 0
            text = ocr_analyser.run_automated_ocr_easyocr()
            print("*"*40)
            print(text)
            if "%" in text:
                break

   

def get_clear_view_action():
    coor_x = 921
    coor_y = 305
    print(f"Moving to clear view action coordinates: ({coor_x}, {coor_y})")

    # Move the mouse to the target with a human-like, random duration
    pyautogui.moveTo(
        coor_x,
        coor_y,
        duration=random.uniform(0.1, 0.3),
        tween=pyautogui.easeOutQuad
    )

    # Perform a realistic click
    print("Clicking clear view action button...")
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
    pyautogui.mouseUp()

    print("✅ Clear view action complete.")