import cv2
import numpy as np
import pyautogui
import time

def find_best_match_on_screen(reference_image_path, confidence_threshold=0.7):
    """
    Finds the best match for a reference image on the screen using a robust
    multi-scale template matching approach with an alpha channel mask.

    Args:
        reference_image_path (str): The path to the reference PNG with transparency.
        confidence_threshold (float): The minimum score (0.0 to 1.0) to consider a match.

    Returns:
        dict: A dictionary with match details ('location', 'score', etc.) or None if not found.
    """
    # 1. Load the reference image, preserving the alpha (transparency) channel
    ref_rgba = cv2.imread(reference_image_path, cv2.IMREAD_UNCHANGED)
    if ref_rgba is None:
        print(f"FATAL ERROR: Could not open reference image at '{reference_image_path}'")
        return None

    # Separate the BGR channels (the template) and the Alpha channel (the mask)
    template = ref_rgba[:, :, :3]
    mask = ref_rgba[:, :, 3]

    # 2. Capture the screen just once
    print("Capturing screen...")
    screenshot_pil = pyautogui.screenshot()
    screen_bgr = cv2.cvtColor(np.array(screenshot_pil), cv2.COLOR_RGB2BGR)
    
    # 3. Perform Multi-Scale Matching
    best_match = {'score': -1, 'location': None, 'scale': 1.0, 'size': (0, 0)}
    
    # Define a range of scales to check. This makes the search flexible.
    # From 50% size up to 150% size, in steps of 10%.
    scales_to_check = np.linspace(0.5, 1.5, 11)
    
    print(f"Now searching on {len(scales_to_check)} different scales...")

    for scale in scales_to_check:
        # Resize the template and its mask according to the current scale
        w = int(template.shape[1] * scale)
        h = int(template.shape[0] * scale)
        
        if w == 0 or h == 0 or w > screen_bgr.shape[1] or h > screen_bgr.shape[0]:
            continue

        resized_template = cv2.resize(template, (w, h), interpolation=cv2.INTER_AREA)
        resized_mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_AREA)

        # Perform template matching
        result = cv2.matchTemplate(screen_bgr, resized_template, cv2.TM_CCOEFF_NORMED, mask=resized_mask)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        # If this scale gives a better score than any we've seen before, store it
        if max_val > best_match['score']:
            best_match['score'] = max_val
            best_match['location'] = max_loc
            best_match['scale'] = scale
            best_match['size'] = (w, h)

    # 4. Evaluate the single best match found across all scales
    print(f"\nSearch complete. Overall Best Match -> Score: {best_match['score']:.3f} at Scale: {best_match['scale']:.2f}x")

    if best_match['score'] >= confidence_threshold:
        print(f"SUCCESS! Match found with confidence above the threshold of {confidence_threshold}.")
        return best_match
    else:
        print("FAILURE: A match was found, but its confidence score is too low.")
        return None


if __name__ == "__main__":
    REFERENCE_IMAGE_PATH = 'images/octavio.png'  # <--- Make sure this path is correct
    CONFIDENCE_THRESHOLD = 0.7  # <--- YOU CAN TUNE THIS VALUE

    print("Starting finder in 3 seconds...")
    time.sleep(3)
    
    # Run the robust finder
    found_object = find_best_match_on_screen(REFERENCE_IMAGE_PATH, CONFIDENCE_THRESHOLD)

    # Visualize the result
    screenshot_bgr = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

    if found_object:
        top_left = found_object['location']
        w, h = found_object['size']
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        # Draw a bright green rectangle around the found object
        cv2.rectangle(screenshot_bgr, top_left, bottom_right, (0, 255, 0), 3)
        
        # Put the score and scale text on the image
        score_text = f"Score: {found_object['score']:.2f}"
        scale_text = f"Scale: {found_object['scale']:.2f}x"
        cv2.putText(screenshot_bgr, score_text, (top_left[0], top_left[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(screenshot_bgr, scale_text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
    else:
        fail_text = "Object Not Found"
        text_size, _ = cv2.getTextSize(fail_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        screen_h, screen_w, _ = screenshot_bgr.shape
        text_x = (screen_w - text_size[0]) // 2
        text_y = (screen_h + text_size[1]) // 2
        cv2.putText(screenshot_bgr, fail_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the final result
    cv2.imshow("Final Result", screenshot_bgr)
    print("\nDisplaying the final result. Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()