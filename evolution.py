
import time
import actions
import ocr_analyser

def evolve_miscrit(reader):
    text = ocr_analyser.run_automated_ocr_easyocr(
                reader=reader,
                horizontal_start_percent=35, horizontal_end_percent=45,
                vertical_start_percent=20, vertical_end_percent=24
            )
    if "Evolved" in text:
        print("🟢 Evolve miscrit completed successfully!")
        actions.okay_evolve_miscrit()

        time.sleep(2)
        actions.close_train_page()
        
        return True
    else:
        print("🔴 Evolve miscrit failed.")
        return False
    
