import time
import cv2
import numpy as np
import mss
import pyautogui
import random
import ocr_analyser  # Assuming this is a module for OCR analysis

def find_and_click_object_multiscale(reference_image_path, confidence_threshold=0.8, target_monitor=1):
    """
    Finds an object using template matching across multiple scales to handle
    display scaling issues (e.g., on Retina/High-DPI screens).
    """
    try:
        # 1. Load the reference image (template)
        reference_img_color = cv2.imread(reference_image_path, cv2.IMREAD_UNCHANGED)
        if reference_img_color is None:
            print(f"Error: Could not load reference image at {reference_image_path}")
            return False

        # --- Get base properties from the original reference image ---
        if reference_img_color.shape[2] == 4:
            reference_gray_orig = cv2.cvtColor(reference_img_color, cv2.COLOR_BGRA2GRAY)
            _, mask_orig = cv2.threshold(reference_img_color[:, :, 3], 1, 255, cv2.THRESH_BINARY)
        else:
            reference_gray_orig = cv2.cvtColor(reference_img_color, cv2.COLOR_BGR2GRAY)
            mask_orig = None

        with mss.mss() as sct:
            # 2. Get screen and system scaling information
            monitor_physical = sct.monitors[target_monitor]
            logical_screen_width, _ = pyautogui.size()
            system_scale_factor = monitor_physical['width'] / logical_screen_width
            print(f"System-wide display scale factor detected: {system_scale_factor:.2f}x")

            # 3. Capture the screen just once
            sct_img = sct.grab(monitor_physical)
            screen_capture_color = np.array(sct_img)
            screen_gray = cv2.cvtColor(screen_capture_color, cv2.COLOR_BGRA2GRAY)

            # 4. Multi-scale matching loop
            best_match = {'score': -1, 'location': None, 'scale': 1.0, 'size': (0,0)}
            
            # Define scales to check. Start with the detected system scale.
            # Then check scales around it in case of minor variations.
            scales_to_check = [system_scale_factor, 1.0, 0.9, 1.1, 0.8, 1.2, 2.0] # Add 2.0 for retina
            scales_to_check = sorted(list(set(scales_to_check)), reverse=True) # Remove duplicates and sort

            print(f"Now searching on scales: {scales_to_check}")

            for scale in scales_to_check:
                # Resize reference image and its mask
                w = int(reference_gray_orig.shape[1] * scale)
                h = int(reference_gray_orig.shape[0] * scale)
                
                # Prevent resizing to 0x0
                if w == 0 or h == 0:
                    continue

                resized_ref = cv2.resize(reference_gray_orig, (w, h), interpolation=cv2.INTER_AREA)
                resized_mask = cv2.resize(mask_orig, (w, h), interpolation=cv2.INTER_NEAREST) if mask_orig is not None else None
                
                # Don't search if the template is now bigger than the screen
                if resized_ref.shape[0] > screen_gray.shape[0] or resized_ref.shape[1] > screen_gray.shape[1]:
                    continue

                result = cv2.matchTemplate(screen_gray, resized_ref, cv2.TM_CCOEFF_NORMED, mask=resized_mask)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                
                # print(f"  - Scale {scale:.2f}: Max confidence = {max_val:.3f}") # Uncomment for deep debugging

                # If this scale gives a better score, store all its info
                if max_val > best_match['score']:
                    best_match['score'] = max_val
                    best_match['location'] = max_loc
                    best_match['scale'] = scale
                    best_match['size'] = (w, h)

            # 5. After checking all scales, evaluate the single best match found
            print(f"\nOverall Best Match Found -> Score: {best_match['score']:.3f} at Scale: {best_match['scale']:.2f}")

            if best_match['score'] >= confidence_threshold:
                print("Object FOUND!")
                
                top_left_physical = best_match['location']
                w, h = best_match['size']
                center_x_physical = top_left_physical[0] + w // 2
                center_y_physical = top_left_physical[1] + h // 2

                # Convert to LOGICAL coordinates for click
                center_x_logical = center_x_physical / system_scale_factor
                center_y_logical = center_y_physical / system_scale_factor
                
                pyautogui.moveTo(
                    center_x_logical, 
                    center_y_logical, 
                    duration=random.uniform(0.2, 0.5), 
                    tween=pyautogui.easeInOutQuad
                )
                
                # Perform a more realistic click
                print("Performing a more realistic click...")
                pyautogui.mouseDown()
                time.sleep(random.uniform(0.05, 0.15))
                pyautogui.mouseUp()
                print("Clicked on the object.")
                
                '''
                # Visualization
                bottom_right_physical = (top_left_physical[0] + w, top_left_physical[1] + h)
                screen_display = cv2.cvtColor(screen_capture_color, cv2.COLOR_BGRA2BGR)
                cv2.rectangle(screen_display, top_left_physical, bottom_right_physical, (0, 255, 0), 2)
                cv2.imshow('Result - Found', screen_display)
                cv2.waitKey(1000)
                '''
                return True
            else:
                print("Object not found on screen at any tested scale.")
                return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        cv2.destroyAllWindows()





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


def run_spot_clicker(image_path):
    print("Starting in 3 seconds. Please switch to your target window.")
    time.sleep(3)
    
    # Define the path to your reference image
    CLICK_DELAY = 3.0

    count = 0
    while True:
        print(f"\nSearching for '{image_path}' in the designated area...")

        # Call the function, passing the newly calculated search region
        was_successful = find_and_click_object_multiscale(image_path, confidence_threshold=0.4)

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
    


if __name__ == "__main__":
    # Example usage
    REFERENCE_IMAGE_PATH = 'images/foil_vhisp.png'  # Update with your image path
    find_and_click_object_multiscale(REFERENCE_IMAGE_PATH, confidence_threshold=0.5)
