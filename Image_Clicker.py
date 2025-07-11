print("made by Cracka555 (https://github.com/Cracka555/Image-Clicker)")
import pyautogui
import time
import cv2
import numpy as np
from PIL import Image
import keyboard  # For key detection

# Configuration
IMAGE_TEMPLATE = 'Test_Image.png'  # Path to image
CLICK_DELAY = 1       # Seconds between clicks
SEARCH_INTERVAL = 5   # Seconds between search cycles
CONFIDENCE = 0.7      # Detection confidence (0.7 = 70%)
STATUS_UPDATE_INTERVAL = 0.5  # Status check interval during waits

# Added on/off state with visual feedback
clicking_active = True
last_status_message = ""

def show_status():
    """Show current status with visual indicator"""
    status = "ACTIVE" if clicking_active else "PAUSED"
    color = "\033[92m" if clicking_active else "\033[93m"  # Green for active, yellow for paused
    reset = "\033[0m"
    return f"{color}● {status}{reset}"

def update_status(message):
    """Update status message with visual indicator"""
    global last_status_message
    status = show_status()
    full_message = f"[{status}] {message}"
    # Only print if message has changed
    if full_message != last_status_message:
        print(full_message)
        last_status_message = full_message

def find_image():
    try:
        # Capture screen
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        # Load template
        template = cv2.imread(IMAGE_TEMPLATE, 0)
        if template is None:
            raise FileNotFoundError("Template image not found")
        
        # Match template
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        # Check confidence
        if max_val >= CONFIDENCE:
            image_width, image_height = template.shape[::-1]
            center_x = max_loc[0] + image_width // 2
            center_y = max_loc[1] + image_height // 2
            return (center_x, center_y)
        return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    global clicking_active
    
    print("Starting image clicker... Switch to the target window!")
    print("Press 'Z' to pause/resume clicking")
    time.sleep(3)
    
    try:
        while True:
            # Handle pause/resume toggle
            if keyboard.is_pressed('Z'):
                clicking_active = not clicking_active
                status = "PAUSED" if not clicking_active else "RESUMED"
                print(f"\nClicking {status}! Press 'P' to {'resume' if not clicking_active else 'pause'}")
                # Wait until key is released
                while keyboard.is_pressed('Z'):
                    time.sleep(0.1)
            
            # Perform image search
            target = find_image()
            
            if target:
                action = "CLICKING" if clicking_active else "Found (PAUSED)"
                update_status(f"Image found at {target} - {action}")
                
                if clicking_active:
                    pyautogui.moveTo(target[0], target[1], duration=0.3)
                    pyautogui.click()
                
                # Wait with status updates
                start_time = time.time()
                while time.time() - start_time < CLICK_DELAY:
                    update_status(f"Waiting before next click ({CLICK_DELAY - (time.time() - start_time):.1f}s)")
                    time.sleep(STATUS_UPDATE_INTERVAL)
            else:
                update_status("No images found. Searching again...")
                
                # Wait with status updates
                start_time = time.time()
                while time.time() - start_time < SEARCH_INTERVAL:
                    status_note = " (PAUSED)" if not clicking_active else ""
                    update_status(f"Next search in {SEARCH_INTERVAL - (time.time() - start_time):.1f}s{status_note}")
                    time.sleep(STATUS_UPDATE_INTERVAL)
    except KeyboardInterrupt:
        print("\nScript stopped")

if __name__ == "__main__":
    main()
