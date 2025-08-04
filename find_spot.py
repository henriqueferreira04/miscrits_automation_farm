import cv2
import numpy as np
import pyautogui
import time
import random

def get_contours_from_image(input_image):
    """
    Streamlined pipeline to take a BGR image and return its contours.
    This version does not show intermediate steps.
    """
    if input_image is None or input_image.size == 0:
        return []

    # Pipeline: Grayscale -> Blur -> Canny -> Dilate -> Find Contours
    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image, (3, 3), 0)
    canny_edges = cv2.Canny(blurred_image, 50, 150)
    kernel = np.ones((3, 3), np.uint8) # Use a slightly larger kernel for better connection
    dilated_edges = cv2.dilate(canny_edges, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours


if __name__ == "__main__":
    # ==========================================================
    # PART 1: PROCESS THE REFERENCE IMAGE
    # ==========================================================
    REFERENCE_IMAGE_PATH = 'images/foil_vhisp.png' # Make sure this path is correct
    reference_rgba = cv2.imread(REFERENCE_IMAGE_PATH, cv2.IMREAD_UNCHANGED)

    if reference_rgba is None:
        print(f"FATAL ERROR: Could not open reference image at '{REFERENCE_IMAGE_PATH}'")
        exit()

    # Isolate the object using its alpha channel
    alpha_channel = reference_rgba[:, :, 3]
    reference_bgr = reference_rgba[:, :, :3]
    black_background = np.zeros_like(reference_bgr)
    isolated_bgr = np.where(alpha_channel[..., None] > 0, reference_bgr, black_background)

    # Get the contours from our perfectly isolated reference object
    ref_contours = get_contours_from_image(isolated_bgr)

    if not ref_contours:
        print("FATAL ERROR: No contours found in the reference image. Check the image and pipeline settings.")
        exit()

    # Combine all reference contours into a single one for matching
    # This creates a master shape of the entire object
    master_ref_contour = np.vstack([c for c in ref_contours])
    print(f"Reference image processed successfully. Found {len(ref_contours)} parts and combined them into one master shape.")

    # ==========================================================
    # PART 2: PROCESS THE SCREEN AND MATCH
    # ==========================================================
    print("\nStarting screen capture and matching in 3 seconds...")
    time.sleep(3)
    
    screenshot_pil = pyautogui.screenshot()
    screen_bgr = cv2.cvtColor(np.array(screenshot_pil), cv2.COLOR_RGB2BGR)

    # Get all contours from the live screen capture
    print("Processing screen to find all contours...")
    screen_contours = get_contours_from_image(screen_bgr)
    print(f"Found {len(screen_contours)} potential contours on the screen.")

    # ==========================================================
    # PART 3: FIND THE BEST MATCH
    # ==========================================================
    print("\nComparing reference shape to all screen shapes...")
    
    best_match_score = float('inf')  # Start with an infinitely bad score
    best_match_contour = None
    
    # Loop through every contour found on the screen
    for screen_contour in screen_contours:
        # Compare the screen contour to our master reference contour
        # cv2.CONTOURS_MATCH_I1 is one of the most reliable matching methods
        match_score = cv2.matchShapes(master_ref_contour, screen_contour, cv2.CONTOURS_MATCH_I1, 0.0)
        
        # If this contour is a better match than any we've seen before, store it
        if match_score < best_match_score:
            best_match_score = match_score
            best_match_contour = screen_contour

    # ==========================================================
    # PART 4: VISUALIZE THE FINAL RESULT
    # ==========================================================
    
    # Define a threshold for what you consider a "good" match.
    # This value requires tuning! Lower is stricter. Start with 0.5.
    MATCH_THRESHOLD = 0.5 

    if best_match_contour is not None and best_match_score < MATCH_THRESHOLD:
        print(f"\nSUCCESS! Found a good match.")
        print(f"  -> Best match score: {best_match_score:.4f} (lower is better)")
        
        # Get the bounding box of the best matching contour
        x, y, w, h = cv2.boundingRect(best_match_contour)
        
        # Draw a red rectangle around the found object on the original screenshot
        cv2.rectangle(screen_bgr, (x, y), (x + w, y + h), (0, 0, 255), 3)
        
        # Put the score text on the image
        text = f"Match Score: {best_match_score:.2f}"
        cv2.putText(screen_bgr, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        coor_x = x + w // 2
        coor_y = y + h // 2
        pyautogui.moveTo(
            coor_x,
            coor_y,
            duration=random.uniform(0.1, 0.3),
            tween=pyautogui.easeOutQuad
        )
        
        # Perform a realistic click
        print("Clicking capture button...")
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.06, 0.16)) # Hold the click briefly
        pyautogui.mouseUp()
        
    else:
        print(f"\nFAILURE: No suitable match found on screen.")
        print(f"  -> The best score found was {best_match_score:.4f}, which is above the threshold of {MATCH_THRESHOLD}.")

    # Display the final image
    cv2.imshow("Final Result", screen_bgr)
    print("\nDisplaying the final result. Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()