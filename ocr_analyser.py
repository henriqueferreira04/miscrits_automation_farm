import pyautogui
import easyocr
import numpy as np
import cv2
import time


# --- STEP 1: DEFINE YOUR FIXED REGION (EDIT THIS SECTION) ---
# Use percentage-based coordinates for robustness across different screen sizes.

# Horizontal capture area (e.g., from 50% to 100% for the right half)


print("Initializing EasyOCR Reader... (This may take a moment on first run)")
reader = easyocr.Reader(['en']) # Specify English language

def run_automated_ocr_easyocr(horizontal_start_percent=50, horizontal_end_percent=100,
                             vertical_start_percent=0, vertical_end_percent=20):
    """
    Performs fully automated OCR on a screen region using EasyOCR.
    """
    print(f"\n--- Starting EasyOCR at {time.strftime('%H:%M:%S')} ---")
    
    # --- 3. CALCULATE AND CAPTURE THE REGION ---
    screen_width, screen_height = pyautogui.size()
    left = int(screen_width * (horizontal_start_percent / 100)) - 30
    top = int(screen_height * (vertical_start_percent / 100))
    width = int(screen_width * ((horizontal_end_percent - horizontal_start_percent) / 100))
    height = int(screen_height * ((vertical_end_percent - vertical_start_percent) / 100))

    region_to_capture = (left, top, width, height)
    
    print(f"Capturing calculated region: {region_to_capture}")
    # Screenshot directly into a NumPy array format that EasyOCR and OpenCV use
    screenshot_np = np.array(pyautogui.screenshot(region=region_to_capture))
    # Convert from RGB (pyautogui) to BGR (OpenCV) for display purposes
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # --- 4. PERFORM OCR ---
    # EasyOCR works directly on the image array. No pre-processing needed!
    print("Performing OCR...")
    results = reader.readtext(screenshot_np)

    # --- 5. PROCESS AND DISPLAY RESULTS ---
    all_text = []
    if not results:
        print("\n❌ No text detected.")
    else:
        print("\n✅ Text Detected!")
        
        # Draw bounding boxes and text on the image for visual feedback
        for (bbox, text, prob) in results:
            # The bbox is a list of 4 points (top-left, top-right, bottom-right, bottom-left)
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            br = (int(br[0]), int(br[1]))
            
            # Draw a green rectangle around the detected text
            cv2.rectangle(screenshot_cv, tl, br, (0, 255, 0), 2)
            
            # Put the detected text and confidence score above the box
            cv2.putText(screenshot_cv, f"{text} ({prob:.2f})", (tl[0], tl[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            all_text.append(text)
            
    # Print the combined text
    final_text = " ".join(all_text)
    print("\n" + "="*40)
    print("🧠 Detected Text:")
    print(final_text)
    print("="*40)

    '''
    # Show the processed image with bounding boxes
    cv2.imshow("OCR Result", screenshot_cv)
    cv2.waitKey(3000)  # Show window for 3 seconds (3000 ms)
    cv2.destroyAllWindows()
    '''
    
    return final_text