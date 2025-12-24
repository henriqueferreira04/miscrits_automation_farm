# Copilot Coding Agent Instructions for Miscrits Automation Farm

## Project Overview
- This project is an automation bot for the Miscrits game, focused on hunting, capturing, and managing Miscrits using screen OCR and automated mouse/keyboard actions.
- The codebase is organized as a set of single-purpose scripts (e.g., `attack.py`, `capture.py`, `level_up.py`) coordinated by a main runner (`run.py`).
- Image assets are stored in `images/` and screenshots in `screenshots/`.
- Miscrit data and captured results are tracked in `miscrits.json` and `captured_miscrits.txt`.

## Key Workflows
- **Run the bot:** Use `python run.py` as the main entry point. This script orchestrates the automation loop.
- **Dependencies:** Install with `pip install -r requirements.txt`. Python 3.8+ is required.
- **Configuration:** Game-specific settings are in `config.py` and `config_UI.py`.
- **OCR:** Uses EasyOCR (see requirements.txt) for reading in-game text.
- **Image Matching:** Relies on OpenCV and image templates in `images/` for UI automation.

## Project Conventions & Patterns
- Each script is focused on a single automation task (e.g., `attack.py` for fighting, `capture.py` for catching Miscrits).
- Shared logic (mouse control, OCR, health detection) is factored into utility modules like `mouse.py`, `ocr_analyser.py`, and `health_percentage_detector.py`.
- Miscrit state and stats are tracked in plain text and JSON files, not a database.
- The bot is designed to be robust: scripts handle pop-ups and auto-restart on failure (`stuck_pop_ups.py`, `mission_complete.py`).
- Image and coordinate references are not hardcoded; they are loaded from config files or detected at runtime.

## Integration Points
- **External:** Requires the Miscrits game running in a compatible window. No direct API integration; all actions are via screen scraping and simulated input.
- **Dependencies:** Key packages include `opencv-python`, `pytesseract`, `easyocr`, `pyautogui`, and `Pillow`.

## Examples & References
- See `run.py` for the main automation loop and how modules are orchestrated.
- See `config.py` and `config_UI.py` for how screen regions and UI elements are defined.
- See `ocr_analyser.py` for OCR logic and text extraction patterns.
- See `captured_miscrits.txt` and `miscrits.json` for data output formats.

## Special Notes
- The bot is designed for extensibility: add new automation features by creating new scripts and integrating them in `run.py`.
- For debugging, use print statements or write logs to files; there is no centralized logging system.
- The project is cross-platform but tested primarily on macOS.

---

If you are an AI agent, follow these conventions and reference the above files for examples of project-specific logic and data handling. When in doubt, prefer modular scripts and utility functions, and avoid hardcoding UI coordinates or image paths.
