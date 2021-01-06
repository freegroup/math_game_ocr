import pyautogui
import cv2
import pytesseract
import os
import time
import numpy as np
from utils.image import image_resize
import PIL.ImageGrab

# The order of the colors is blue, green, red
lower_color = np.array([124, 132, 80])
upper_color = np.array([182, 255, 120])

# take a screenshot of the screen and store it in memory, then
# convert the PIL/Pillow image to an OpenCV compatible NumPy array
# and finally write the image to disk
def fit_text(text):
    text = text.replace("S", "8")
    text = text.replace("s", "6")
    text = text.replace("!", "1")
    text = text.replace("I", "1")
    text = text.replace("i", "1")
    text = text.replace("t", "1")
    text = text.replace("(", "1")
    text = text.replace("{", "1")
    text = text.replace("f", "1")
    text = text.replace("|", "1")
    text = text.replace("[", "1")
    text = text.replace("l", "1")
    text = text.replace("Q", "2")
    text = text.replace("B", "8")
    text = text.replace("O", "0")
    text = text.replace("0", "0")
    text = text.replace("+ =", "=")
    text = text.replace("<=", "=")
    text = text.replace("~=", "=")
    text = text.replace("<", "=")
    #text = text.replace("=", "")
    text = text.replace("x", "*")
    text = text.replace(".", "")
    text = text.replace(" ", "")
    text = text.replace("\r", "")
    text = text.replace("\n", "")
    text = text.strip()
    return text


counter = 0
last_line = ""
while True:
    try:
        start = time.time()
        image = pyautogui.screenshot()
        #image = PIL.ImageGrab.grab()
        print("Screenshot", time.time() - start)

        start = time.time()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        (thresh, blackAndWhiteImage) = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)
        image = 255 - blackAndWhiteImage

        y = 755
        x = 2750
        h = 130
        w = 500
        question_img = image[y:y + h, x:x + w]

        y = 903
        x = 2850
        answer_img = image[y:y + h, x:x + w]

        image = image_resize(cv2.hconcat([question_img, answer_img]), height=25)
        print("Convert", time.time() - start)
        #cv2.imwrite(str(counter)+"_screen.png", image)

        counter = counter + 1

        start = time.time()
        line_ocr = pytesseract.image_to_string(image, config='--psm 10 --oem 3')
        print("OCR", time.time() - start)

        start = time.time()
        line = fit_text(line_ocr)
        line = line.replace("=", "==")
        result = str(eval(line))
        print("EVAL", time.time() - start)
        print(line + " : " + result)
        if not line == last_line:
            last_line = line
            print("click")
            if result == "True":
                pyautogui.click(x=1422, y=832)
            else:
                pyautogui.click(x=1581, y=832)
            time.sleep(0.05)
    except Exception as exc:
        pyautogui.click(x=1581, y=832)
        time.sleep(0.7)
        print(exc)
        print("------------------")
        print(line_ocr)
        print(line)
        print("------------------")
