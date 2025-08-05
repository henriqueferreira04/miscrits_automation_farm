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

# --- Detection Threshold ---
# The number of "blood red" pixels that must be present to trigger the alarm.
# TUNE THIS using the debug output. Start with a low number.
MIN_DARK_RED_PIXEL_THRESHOLD = 100

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


