# SCRIPT 1: generate_perfect_reference.py
import cv2
import numpy as np
import mss
import os
import time

def generate_perfect_reference(reference_image_path, target_monitor=1):
    """
    Finds an object using multi-scale matching and saves a new, perfectly-scaled
    reference image from the screen capture for future high-confidence matching.
    """
    try:
        # Load your original, low-resolution reference image
        reference_img_color = cv2.imread(reference_image_path, cv2.IMREAD_UNCHANGED)
        if reference_img_color is None:
            print(f"Error: Could not load reference image at {reference_image_path}")
            return

        reference_gray_orig = cv2.cvtColor(reference_img_color, cv2.COLOR_BGRA2GRAY) if reference_img_color.shape[2] == 4 else cv2.cvtColor(reference_img_color, cv2.COLOR_BGR2GRAY)

        with mss.mss() as sct:
            # Capture the screen
            monitor_physical = sct.monitors[target_monitor]
            sct_img = sct.grab(monitor_physical)
            screen_capture_color = np.array(sct_img)
            screen_gray = cv2.cvtColor(screen_capture_color, cv2.COLOR_BGRA2GRAY)

            # Find the best scale (same logic as your script)
            best_match = {'score': -1, 'location': None, 'size': (0,0)}
            scales_to_check = np.linspace(1.5, 2.5, 21) # Fine-grained search around 2.0x scale

            for scale in scales_to_check:
                w = int(reference_gray_orig.shape[1] * scale)
                h = int(reference_gray_orig.shape[0] * scale)
                if w == 0 or h == 0 or w > screen_gray.shape[1] or h > screen_gray.shape[0]: continue
                
                resized_ref = cv2.resize(reference_gray_orig, (w, h), interpolation=cv2.INTER_AREA)
                result = cv2.matchTemplate(screen_gray, resized_ref, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                
                if max_val > best_match['score']:
                    best_match.update({'score': max_val, 'location': max_loc, 'size': (w, h)})
            
            print(f"Initial low-confidence match found with score: {best_match['score']:.3f}")
            
            # Now, use the location and size of the best match to crop the PERFECT reference
            if best_match['score'] > 0.3: # Make sure we found something reasonable
                top_left = best_match['location']
                w, h = best_match['size']
                bottom_right = (top_left[0] + w, top_left[1] + h)
                
                # Crop this area from the ORIGINAL screen capture
                perfect_reference_crop = screen_capture_color[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

                # Save the new perfect reference
                save_path = "_perfect_reference.png"
                cv2.imwrite(save_path, perfect_reference_crop)
                print(f"\nSUCCESS! A new, perfectly-scaled reference image has been saved as '{save_path}'")
                print("Use this file path in your main script from now on.")

                # Save a debug image showing where we cropped from
                screen_display = cv2.cvtColor(screen_capture_color, cv2.COLOR_BGRA2BGR)
                cv2.rectangle(screen_display, top_left, bottom_right, (0, 255, 0), 2)
                cv2.imwrite("_debug_match_area.png", screen_display)
                print("Check '_debug_match_area.png' to verify the location.")
            else:
                print("Could not find a confident enough match to generate a new reference.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Use your original, low-res image path here
    ORIGINAL_IMAGE_PATH = 'images/foil_vhisp.png'
    print("Attempting to generate a perfect reference image in 3 seconds...")
    time.sleep(3)
    generate_perfect_reference(ORIGINAL_IMAGE_PATH)