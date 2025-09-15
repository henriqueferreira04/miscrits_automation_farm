from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QScrollArea, QGridLayout, QDialog
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
import sys
import config

# ===============================
# Transparent click-to-select window for each screen
# ===============================
class ClickCaptureWindow(QWidget):
    def __init__(self, callback, screen_geometry):
        super().__init__()
        self.callback = callback
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.3)
        self.setStyleSheet("background-color: black;")
        self.setGeometry(screen_geometry)  # cover this screen

    def mousePressEvent(self, event):
        pos = event.globalPosition()
        x, y = int(pos.x()), int(pos.y())
        self.callback((x, y))
        # Close all overlay windows
        for w in QApplication.topLevelWidgets():
            if isinstance(w, ClickCaptureWindow):
                w.close()


# ===============================
# Config Editor UI
# ===============================
class ConfigEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Config Editor")
        self.setGeometry(100, 100, 800, 700)

        main_layout = QVBoxLayout()

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)

        self.inputs = {}
        row = 0
        for var_name, coords in config.__dict__.items():
            if isinstance(coords, (list, tuple)) and len(coords) == 2:
                self.add_coordinate_field(row, var_name, coords)
                row += 1

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Save button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        main_layout.addWidget(save_button)

        self.setLayout(main_layout)

    # -------------------------------
    # Add coordinate row
    # -------------------------------
    def add_coordinate_field(self, row, var_name, coords):
        label = QLabel(var_name)
        self.grid_layout.addWidget(label, row, 0)

        x_input = QLineEdit(str(coords[0]))
        x_input.setReadOnly(True)
        x_input.setStyleSheet("background-color: lightgrey;")
        self.grid_layout.addWidget(x_input, row, 1)

        y_input = QLineEdit(str(coords[1]))
        y_input.setReadOnly(True)
        y_input.setStyleSheet("background-color: lightgrey;")
        self.grid_layout.addWidget(y_input, row, 2)

        # Unlock button
        unlock_button = QPushButton()
        unlock_button.setIcon(QIcon.fromTheme("lock"))
        unlock_button.clicked.connect(lambda: self.unlock_fields(x_input, y_input, unlock_button))
        self.grid_layout.addWidget(unlock_button, row, 3)

        # Change Coords button
        change_button = QPushButton("Change Coords")
        change_button.clicked.connect(lambda: self.run_find_coords(var_name))
        self.grid_layout.addWidget(change_button, row, 4)

        # Eye button to view screenshot
        eye_button = QPushButton()
        eye_button.setText("👁")
        eye_button.clicked.connect(lambda: self.open_screenshot(var_name))
        self.grid_layout.addWidget(eye_button, row, 5)

        self.inputs[var_name] = (x_input, y_input, unlock_button, change_button, eye_button)

    # -------------------------------
    # Unlock fields
    # -------------------------------
    def unlock_fields(self, x_input, y_input, unlock_button):
        if x_input.isReadOnly():
            x_input.setReadOnly(False)
            y_input.setReadOnly(False)
            x_input.setStyleSheet("")
            y_input.setStyleSheet("")
            unlock_button.setIcon(QIcon.fromTheme("lock-open"))
        else:
            x_input.setReadOnly(True)
            y_input.setReadOnly(True)
            x_input.setStyleSheet("background-color: lightgrey;")
            y_input.setStyleSheet("background-color: lightgrey;")
            unlock_button.setIcon(QIcon.fromTheme("lock"))

    # -------------------------------
    # Capture coordinates with click on any screen
    # -------------------------------
    def run_find_coords(self, var_name):
        def callback(coords):
            self.set_coords(var_name, coords)

        self.click_windows = []
        for screen in QApplication.screens():
            geom = screen.geometry()
            w = ClickCaptureWindow(callback, geom)
            w.show()
            self.click_windows.append(w)

        QMessageBox.information(
            self, "Capture Coordinates",
            "Click anywhere on the screen to capture coordinates."
        )

    def set_coords(self, var_name, coords):
        x_input, y_input, _, _ = self.inputs[var_name]
        x_input.setText(str(coords[0]))
        y_input.setText(str(coords[1]))

    # -------------------------------
    # Save changes to config.py
    # -------------------------------
    def save_changes(self):
        try:
            with open("config.py", "w") as file:
                for var_name, (x_input, y_input, _, _) in self.inputs.items():
                    x = int(x_input.text())
                    y = int(y_input.text())
                    file.write(f"{var_name} = ({x}, {y})\n")
            QMessageBox.information(self, "Success", "Changes saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {e}")

    def open_screenshot(self, var_name):
        """Open the screenshot corresponding to the variable name in a new window."""
        import os
        from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QDialog
        from PySide6.QtGui import QPixmap

        screenshot_path = os.path.join("screenshots", f"{var_name}.png")
        if os.path.exists(screenshot_path):
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Screenshot: {var_name}")
            dialog.setGeometry(200, 200, 600, 400)

            layout = QVBoxLayout()

            # Display the image
            pixmap = QPixmap(screenshot_path)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)
            layout.addWidget(image_label)

            # Close button
            close_button = QPushButton("Close")
            close_button.clicked.connect(dialog.close)
            layout.addWidget(close_button)

            dialog.setLayout(layout)
            dialog.exec()
        else:
            QMessageBox.warning(self, "File Not Found", f"Screenshot not found: {screenshot_path}")


# ===============================
# Main
# ===============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigEditor()
    window.show()
    sys.exit(app.exec())