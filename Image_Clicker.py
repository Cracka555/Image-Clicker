print("made by Cracka555 (https://github.com/Cracka555/Image-Clicker)")
import pyautogui
import time
import cv2
import numpy as np
from PIL import Image

# Configuration
IMAGE_TEMPLATE = 'TestImage.png'  # Path to image
CLICK_DELAY = 1       # Seconds between clicks
SEARCH_INTERVAL = 5   # Seconds between search cycles
CONFIDENCE = 0.7      # Detection confidence (0.7 = 70%)

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
    print("Starting image clicker in 3 seconds... Switch to the exist image!")
    time.sleep(3)
    
    try:
        while True:
            target = find_image()
            if target:
                print(f"image found at {target}")
                pyautogui.moveTo(target[0], target[1], duration=0.5)
                pyautogui.click()
                time.sleep(CLICK_DELAY)
            else:
                print("No images found. Searching again...")
            time.sleep(SEARCH_INTERVAL)
    except KeyboardInterrupt:
        print("\nScript stopped")

if __name__ == "__main__":
    main()
