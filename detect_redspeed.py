import pyautogui
import time
import sys
import os
from PIL import ImageDraw
pyautogui.draw = ImageDraw

# ==============================================================================
#  CONFIGURATION
# ==============================================================================

# --- Anchor Configuration ---
# The image of the static part of the element (the lightning bolt)
ANCHOR_IMAGE = 'images/speed_icon.png'
# Confidence level for finding the anchor. Lower if not found, raise if too many false positives.
CONFIDENCE_LEVEL = 0.85 

# --- Region of Interest (ROI) Configuration ---
# After finding the anchor, we'll check a box to its right for the red number.
# These values are offsets from the TOP-LEFT corner of the found anchor image.
# *** USE THE 'debug_roi.png' FILE TO HELP YOU ADJUST THESE VALUES! ***
ROI_OFFSET_X = 50  # How many pixels to the RIGHT of the anchor's corner to start.
ROI_OFFSET_Y = 5   # How many pixels DOWN from the anchor's corner to start.
ROI_WIDTH = 25     # The width of the box to check for red pixels.
ROI_HEIGHT = 25    # The height of the box to check for red pixels.

# --- Color Detection Configuration ---
# Define what counts as "red". (Valid values are 0-255)
RED_MIN_R = 150  # Minimum Red value for a pixel to be considered "red"
RED_MAX_G = 70   # Maximum Green value
RED_MAX_B = 70   # Maximum Blue value

# Minimum number of red pixels we need to find in the ROI to confirm a match.
MIN_RED_PIXEL_COUNT = 20

# --- Script Behavior ---
# Time to wait between each search attempt
SCAN_INTERVAL = 1.0 

# ==============================================================================
#  CORE LOGIC (You shouldn't need to edit below this line)
# ==============================================================================

def analyze_roi_for_red(anchor_box):
    """
    Checks the region next to the anchor for a significant number of red pixels.
    """
    try:
        # 1. Define the Region of Interest (ROI) based on the anchor's position
        roi_left = anchor_box.left + ROI_OFFSET_X
        roi_top = anchor_box.top + ROI_OFFSET_Y
        roi = (roi_left, roi_top, ROI_WIDTH, ROI_HEIGHT)
        
        # 2. Take a screenshot of ONLY the ROI for fast analysis
        roi_screenshot = pyautogui.screenshot(region=roi)
        
        # 3. Count the number of "red" pixels in the screenshot
        red_pixel_count = 0
        width, height = roi_screenshot.size
        for x in range(width):
            for y in range(height):
                pixel = roi_screenshot.getpixel((x, y))
                # FIX: Check the first 3 values (R, G, B) and ignore the 4th (Alpha)
                # This works for both RGB and RGBA images.
                if pixel[0] > RED_MIN_R and pixel[1] < RED_MAX_G and pixel[2] < RED_MAX_B:
                    red_pixel_count += 1
        
        print(f"  -> Found {red_pixel_count} red pixels in the ROI. (Need >= {MIN_RED_PIXEL_COUNT})")
        return red_pixel_count >= MIN_RED_PIXEL_COUNT

    except Exception as e:
        print(f"  -> An error occurred during color analysis: {e}")
        return False

def create_debug_image(anchor_box):
    """
    Takes a screenshot and draws the anchor and ROI boxes for easy debugging.
    """
    try:
        # Take a screenshot of a larger area around the anchor
        screenshot_area = (anchor_box.left - 50, anchor_box.top - 50, anchor_box.width + 150, anchor_box.height + 100)
        full_screenshot = pyautogui.screenshot(region=screenshot_area)
        
        # Draw a green box around the found anchor
        pyautogui.draw.rectangle(
            full_screenshot,
            (anchor_box.left - screenshot_area[0], anchor_box.top - screenshot_area[1]),
            (anchor_box.left - screenshot_area[0] + anchor_box.width, anchor_box.top - screenshot_area[1] + anchor_box.height),
            outline="lime",
            width=2
        )
        
        # Draw a red box for the ROI we are analyzing
        roi_left_rel = anchor_box.left - screenshot_area[0] + ROI_OFFSET_X
        roi_top_rel = anchor_box.top - screenshot_area[1] + ROI_OFFSET_Y
        pyautogui.draw.rectangle(
            full_screenshot,
            (roi_left_rel, roi_top_rel),
            (roi_left_rel + ROI_WIDTH, roi_top_rel + ROI_HEIGHT),
            outline="red",
            width=2
        )

        filepath = os.path.abspath("debug_roi.png")
        full_screenshot.save(filepath)
        print(f"\n📸 Saved debug image with ROI box to: {filepath}")
        print("   Use this image to check if your ROI settings are correct.\n")
    except Exception as e:
        print(f"Could not create debug image: {e}")


def run_red_speed_detector():
    """
    Main loop to find the anchor and check for the red number.
    """
    print("--- Red Number Detector ---")
    
    # --- One-time debug image generation ---
    print("Performing initial scan to create debug image...")
    try:
        initial_anchor = pyautogui.locateOnScreen(ANCHOR_IMAGE, confidence=CONFIDENCE_LEVEL)
        if initial_anchor:
            create_debug_image(initial_anchor)
        else:
            print(f"❌ Could not find anchor image '{ANCHOR_IMAGE}' on screen to create debug image.")
    except pyautogui.PyAutoGUIException as e:
        print(f"An OS-level error occurred trying to find the image: {e}")

    # --- Main operational loop ---
    print("--- Starting main loop. Press Ctrl+C to stop. ---")
    try:
        while True:
            # IMPROVEMENT: Use locateOnScreen to find just the first, best match.
            anchor_box = pyautogui.locateOnScreen(ANCHOR_IMAGE, confidence=CONFIDENCE_LEVEL)
            
            if anchor_box:
                print(f"Found anchor at {anchor_box}.")
                # If anchor is found, check for the red number next to it
                if analyze_roi_for_red(anchor_box):
                    print("✅ SUCCESS: Found an anchor with a red number!")
                    
                    #
                    # <<<<< YOUR ACTION GOES HERE >>>>>
                    # For example, click your attack button
                    # pyautogui.click(1250, 800) 
                    #
                    
                    print("Action complete. Pausing before resuming scan...")
                    time.sleep(SCAN_INTERVAL * 2) # Longer pause after a successful action
                    return True
                else:
                    print("❌ Anchor found, but number is not red. Continuing scan...")
                    return False
            else:
                print("❌ Anchor not found on screen. Retrying...", end='\r')

            time.sleep(SCAN_INTERVAL)

    except FileNotFoundError:
        print(f"\n❌ ERROR: Cannot find the anchor image '{ANCHOR_IMAGE}'.")
        print("Please make sure it is in the same folder as the script.")
    except KeyboardInterrupt:
        print("\nScript stopped by user. Goodbye!")

if __name__ == "__main__":
    

    run_red_speed_detector()