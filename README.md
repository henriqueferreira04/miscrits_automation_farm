# 🎮 Miscrits Automation Farm

An intelligent automation bot for the Miscrits game that automatically hunts, captures, and manages Miscrits based on their rarity and stats.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- **🔍 Automated Hunting**: Automatically clicks bushes to find Miscrits
- **📸 OCR Recognition**: Uses EasyOCR to read Miscrit names and stats from screen
- **🎯 Smart Capture Logic**: Captures based on rarity (Common, Rare, Exotic) and health percentage
- **⚡ Speed Detection**: Detects red speed stats for valuable Miscrits
- **🏥 Health Management**: Automatically heals Miscrits when health is critical
- **🔄 Auto-Restart**: Continues running even if the script crashes
- **🎮 Multi-Image Support**: Supports multiple variations of Miscrit images

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- macOS, Windows, or Linux
- Display resolution suitable for the game interface

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/henriqueferreira04/miscrits_automation_farm.git
   cd miscrits_automation_farm
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the automation**

   ```bash
   python run.py
   ```
