# ==============================================================================
#  STEP 1: FIND YOUR COORDINATES
# ==============================================================================

from pynput import mouse, keyboard
from pynput.keyboard import Listener, Key

# Global variable to store the recorded coordinates
recorded_coords = None

# Function to handle key presses
def on_press(key):
    global recorded_coords
    if key == Key.esc:
        #print("\nCoordinate Finder cancelled.")
        return False  # Stop the listener
    elif hasattr(key, 'char') and key.char == '0':
        #print(f"\nRecorded coordinates: {recorded_coords}")
        return False  # Stop the listener

# Function to display mouse coordinates
def find_coordinates():
    """
    An interactive tool to display the current (X, Y) coordinates of the mouse.
    Press '0' to record coordinates, 'ESC' to cancel and return None.
    """
    global recorded_coords

    try:
        with mouse.Listener(on_move=on_move) as mouse_listener, keyboard.Listener(on_press=on_press) as keyboard_listener:
            # Wait for the keyboard listener to stop
            keyboard_listener.join()

    except Exception as e:
        print(f"Error: {e}")
        return None
    
    return recorded_coords

# Function to handle mouse movement
def on_move(x, y):
    global recorded_coords
    recorded_coords = (int(x), int(y))
    position_str = f"X: {str(x).rjust(4)}  Y: {str(y).rjust(4)}"
    #print(position_str, end='\r')

if __name__ == "__main__":
    print(find_coordinates())