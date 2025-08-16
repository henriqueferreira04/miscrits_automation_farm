import pyautogui
import numpy as np
import cv2
import sys
import os
import time

# ==============================================================================
#  STEP 1: CONFIGURE THESE SETTINGS
# ==============================================================================

# --- Region of the Health Bar (using percentages of the screen) ---
# **TUNE THIS FIRST!** Define a box that contains the health bar.
HEALTH_BAR_REGION_PERCENT = {
    "horizontal_start": 29,  # Starts at 29% from the left edge of the screen.
    "horizontal_end":   36,  # Ends at 36% from the left edge.
    "vertical_start":   5,   # Starts at 5% from the top edge.
    "vertical_end":     7    # Ends at 7% from the top edge.
}

# --- "Blood Red" Color Range (in BGR format) ---
# **THIS IS THE MOST IMPORTANT SETTING FOR THIS SCRIPT.**
# This range should ONLY match the dark, critical "blood red" color,
# and IGNORE the normal, brighter red of a healthy bar.
# You will need to fine-tune this with the debug images.
DARK_RED_LOWER = np.array([0, 0, 80])      # Lower bound for a dark red
DARK_RED_UPPER = np.array([50, 50, 180])   # Upper bound for a dark red

# --- "Yellow" Color Range (in BGR format) ---
# This range should match the yellow color for "ready to train" status.
# Yellow in BGR format typically has high B and G values, low R value.
# ✅ PROVEN WORKING RANGE - detected 97 pixels in testing
YELLOW_LOWER = np.array([0, 100, 100])     # Working lower bound for yellow
YELLOW_UPPER = np.array([80, 255, 255])    # Working upper bound for yellow

# Alternative yellow ranges to try if the above doesn't work:
# Brighter yellow: YELLOW_LOWER = np.array([0, 200, 200]), YELLOW_UPPER = np.array([40, 255, 255])
# Wider yellow range: YELLOW_LOWER = np.array([0, 150, 150]), YELLOW_UPPER = np.array([80, 255, 255])
# HSV yellow (if converting): H=20-30, S=100-255, V=200-255

# --- Detection Threshold ---
# The number of "blood red" pixels that must be present to trigger the alarm.
# TUNE THIS using the debug output. Start with a low number.
MIN_DARK_RED_PIXEL_THRESHOLD = 100

# --- Yellow Detection Threshold ---
# The number of yellow pixels that must be present to indicate "ready to train".
# ✅ Set based on testing: detected 97 pixels, so threshold set to 30 for reliability
MIN_YELLOW_PIXEL_THRESHOLD = 30

# --- Debug Mode ---
# ALWAYS use Debug Mode to set up and test your color range and threshold.
DEBUG_MODE = True

# ==============================================================================
#  CORE LOGIC (You shouldn't need to edit below this line)
# ==============================================================================

def is_health_critical():
    """
    Checks the defined screen region for a significant number of
    specific "blood red" pixels.
    """
    try:
        # 1. Calculate the pixel region from the given percentages
        screen_width, screen_height = pyautogui.size()
        left = int(screen_width * (HEALTH_BAR_REGION_PERCENT["horizontal_start"] / 100))
        top = int(screen_height * (HEALTH_BAR_REGION_PERCENT["vertical_start"] / 100))
        width = int(screen_width * ((HEALTH_BAR_REGION_PERCENT["horizontal_end"] - HEALTH_BAR_REGION_PERCENT["horizontal_start"]) / 100))
        height = int(screen_height * ((HEALTH_BAR_REGION_PERCENT["vertical_end"] - HEALTH_BAR_REGION_PERCENT["vertical_start"]) / 100))
        region_tuple = (left, top, width, height)

        # 2. Capture the region and convert to BGR for OpenCV
        screenshot_np = np.array(pyautogui.screenshot(region=region_tuple))
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # 3. Create a mask that isolates only the DARK RED pixels
        dark_red_mask = cv2.inRange(screenshot_bgr, DARK_RED_LOWER, DARK_RED_UPPER)

        # 4. Count the number of dark red pixels found
        dark_red_pixel_count = cv2.countNonZero(dark_red_mask)

        if dark_red_pixel_count>= MIN_DARK_RED_PIXEL_THRESHOLD:
            print(f"⚠️ Health is critical! Dark red pixel count: {dark_red_pixel_count}")
        else:
            print(f"✅ Health is not critical. Dark red pixel count: {dark_red_pixel_count}")

        # 6. Return True if the count exceeds our threshold
        return dark_red_pixel_count >= MIN_DARK_RED_PIXEL_THRESHOLD

    except Exception as e:
        print(f"❌ An error occurred during health analysis: {e}")
        return False


def test_yellow_ranges(horizontal_start, horizontal_end, vertical_start, vertical_end):
    """
    Test multiple yellow color ranges to find the best one for detection.
    """
    # Define different yellow ranges to test - much more comprehensive
    yellow_ranges = [
        ("Current", np.array([0, 180, 180]), np.array([60, 255, 255])),
        ("Very Wide", np.array([0, 100, 100]), np.array([120, 255, 255])),
        ("Game Yellow 1", np.array([0, 150, 200]), np.array([80, 255, 255])),
        ("Game Yellow 2", np.array([20, 200, 200]), np.array([100, 255, 255])),
        ("Bright Yellow", np.array([0, 220, 220]), np.array([50, 255, 255])),
        ("Orange-Yellow", np.array([0, 165, 200]), np.array([50, 255, 255])),
        ("Light Text", np.array([100, 200, 200]), np.array([150, 255, 255])),
        ("Almost White", np.array([150, 200, 200]), np.array([255, 255, 255])),
        ("Golden", np.array([0, 180, 215]), np.array([60, 255, 255])),
        ("All Colors", np.array([0, 0, 0]), np.array([255, 255, 255])),
    ]
    
    try:
        # Capture the region
        screen_width, screen_height = pyautogui.size()
        left = int(screen_width * (horizontal_start / 100))
        top = int(screen_height * (vertical_start / 100))
        width = int(screen_width * ((horizontal_end - horizontal_start) / 100))
        height = int(screen_height * ((vertical_end - vertical_start) / 100))
        region_tuple = (left, top, width, height)
        
        screenshot_np = np.array(pyautogui.screenshot(region=region_tuple))
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        print("🔍 Testing different yellow ranges:")
        print("-" * 50)
        
        for name, lower, upper in yellow_ranges:
            yellow_mask = cv2.inRange(screenshot_bgr, lower, upper)
            yellow_count = cv2.countNonZero(yellow_mask)
            print(f"{name:12} | Lower: {lower} | Upper: {upper} | Count: {yellow_count}")
            
            # Show the mask for visual inspection
            cv2.imshow(f"Yellow Mask - {name}", yellow_mask)
        
        cv2.imshow("Original", screenshot_bgr)
        print("\nPress any key to close all windows...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"❌ Error in test_yellow_ranges: {e}")




def is_ready_to_train(horizontal_start, horizontal_end, vertical_start, vertical_end):
    """
    Checks the defined screen region for a significant number of
    yellow pixels indicating "ready to train" status.
    """
    try:
        # 1. Calculate the pixel region from the given percentages
        screen_width, screen_height = pyautogui.size()
        left = int(screen_width * (horizontal_start / 100))
        top = int(screen_height * (vertical_start / 100))
        width = int(screen_width * ((horizontal_end - horizontal_start) / 100))
        height = int(screen_height * ((vertical_end - vertical_start) / 100))
        region_tuple = (left, top, width, height)

        # 2. Capture the region and convert to BGR for OpenCV
        screenshot_np = np.array(pyautogui.screenshot(region=region_tuple))
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    

        # 3. Create a mask that isolates only the YELLOW pixels
        yellow_mask = cv2.inRange(screenshot_bgr, YELLOW_LOWER, YELLOW_UPPER)

        
        # Debug: Show the result of applying the mask
        yellow_result = cv2.bitwise_and(screenshot_bgr, screenshot_bgr, mask=yellow_mask)


        # 4. Count the number of yellow pixels found
        yellow_pixel_count = cv2.countNonZero(yellow_mask)

        if yellow_pixel_count >= MIN_YELLOW_PIXEL_THRESHOLD:
            print(f"✅ Ready to train! Yellow pixel count: {yellow_pixel_count}")
        else:
            print(f"⏳ Not ready to train. Yellow pixel count: {yellow_pixel_count}")

        # 5. Return True if the count exceeds our threshold
        return yellow_pixel_count >= MIN_YELLOW_PIXEL_THRESHOLD

    except Exception as e:
        print(f"❌ An error occurred during yellow detection: {e}")
        return False


