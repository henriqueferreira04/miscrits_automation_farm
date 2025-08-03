import time
import cv2
import numpy as np
import mss
import pyautogui

def find_and_click_object(reference_image_path, confidence_threshold=0.8, target_monitor=1):
    """
    Captures the screen, finds a reference object, handles resolution scaling
    for high-DPI displays, and clicks on the object.
    """
    try:
        # 1. Load the reference image (template)
        reference_img = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
        if reference_img is None:
            print(f"Error: Could not load reference image at {reference_image_path}")
            return
        # Get the width and height of the template image
        w, h = reference_img.shape[::-1]

        with mss.mss() as sct:
            # 2. Get screen information
            monitors = sct.monitors
            if not 0 < target_monitor < len(monitors):
                print(f"Error: Monitor {target_monitor} is not available. Available monitors: {len(monitors)-1}")
                return

            # This is the monitor with PHYSICAL pixel dimensions (e.g., 2560x1600)
            monitor_physical = monitors[target_monitor]

            # Get the LOGICAL screen size that PyAutoGUI uses (e.g., 1280x800)
            logical_screen_width, logical_screen_height = pyautogui.size()

            # 3. Calculate the scaling factor
            # This is the key step for high-DPI displays
            scale_factor = monitor_physical['width'] / logical_screen_width
            print(f"Physical monitor resolution: {monitor_physical['width']}x{monitor_physical['height']}")
            print(f"Logical (PyAutoGUI) resolution: {logical_screen_width}x{logical_screen_height}")
            print(f"Detected display scale factor: {scale_factor}")

            # 4. Capture the screen
            sct_img = sct.grab(monitor_physical)
            
            # Convert to a format that OpenCV can use
            screen_capture = np.array(sct_img)
            screen_gray = cv2.cvtColor(screen_capture, cv2.COLOR_BGRA2GRAY)

            # 5. Find the object using template matching
            result = cv2.matchTemplate(screen_gray, reference_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            print(f"Searching for object... Max confidence found: {max_val:.2f}")

            if max_val >= confidence_threshold:
                # 'max_loc' is the top-left corner in PHYSICAL pixels (e.g., within 2560x1600)
                top_left_physical = max_loc
                
                # Calculate the center of the object in PHYSICAL pixels
                center_x_physical = top_left_physical[0] + w // 2
                center_y_physical = top_left_physical[1] + h // 2

                # --- FIX: Convert PHYSICAL coordinates to LOGICAL coordinates ---
                center_x_logical = center_x_physical / 2
                center_y_logical = center_y_physical / 2
                # --- END FIX ---
                
                print(f"\nObject FOUND!")
                print(f"  > Physical Location (in screenshot): ({center_x_physical}, {center_y_physical})")
                print(f"  > Logical Location (for click): ({int(center_x_logical)}, {int(center_y_logical)})")

                # 6. Perform the click using the corrected LOGICAL coordinates
                pyautogui.moveTo(center_x_logical, center_y_logical, duration=0.25)
                pyautogui.click()
                print("Clicked on the object.")

                # --- Visualization (Optional) ---
                # Draw a rectangle on the captured image for visual confirmation
                bottom_right_physical = (top_left_physical[0] + w, top_left_physical[1] + h)
                # We need to convert the BGR-A screenshot to BGR for drawing
                screen_display = cv2.cvtColor(screen_capture, cv2.COLOR_BGRA2BGR)
                cv2.rectangle(screen_display, top_left_physical, bottom_right_physical, (0, 255, 0), 3)
                cv2.imshow('Result - Object Found', screen_display)
                cv2.waitKey(2000) # Display for 2 seconds

            else:
                print("Object not found on screen.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure all OpenCV windows are closed
        cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Starting in 3 seconds. Please switch to your target window.")
    time.sleep(3)
    
    # Define the path to your reference image
    REFERENCE_IMAGE_PATH = 'images/foil_vhisp.png' 
    
    # Run the function with a confidence threshold
    # You may need to lower this if the object isn't found
    find_and_click_object(REFERENCE_IMAGE_PATH, confidence_threshold=0.7)