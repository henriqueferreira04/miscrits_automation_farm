import ocr_analyser

if __name__ == "__main__":
    text = ocr_analyser.run_automated_ocr_easyocr(
                horizontal_start_percent=40, horizontal_end_percent=50,
                vertical_start_percent=30, vertical_end_percent=40
            )
    if "Congrats" in text:
        print("Capture found in text, proceeding with capture...")
        exit(1)