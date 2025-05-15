
from googletrans import Translator
import cv2
import numpy as np

def create_blank_image(width, height):
    return np.ones((height, width, 3), dtype=np.uint8) * 255

def cutTest2(image1_path, output_path):
    image1 = cv2.imread(image1_path)
    x1, y1 = 125, 50  
    x2, y2 = 1240, 772
    cropped_image = image1[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped_image)


def cutTest1(image1_path, output_path):
    image1 = cv2.imread(image1_path)
    x1, y1 = 115, 2 
    x2, y2 = 1870, 922
    cropped_image = image1[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped_image)


def cutTest2(image1_path, output_path):
    image1 = cv2.imread(image1_path)
    x1, y1 = 125, 50 
    x2, y2 = 1240, 772
    cropped_image = image1[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped_image)


def cutTest3(image1_path, output_path):
    image1 = cv2.imread(image1_path)
    x1, y1 = 100, 20 
    x2, y2 = 1330, 830
    cropped_image = image1[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped_image)


def cutTest4(image1_path, output_path):
    image1 = cv2.imread(image1_path)
    x1, y1 = 770, 90 
    x2, y2 = 1890, 890
    cropped_image = image1[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped_image)


def translate_text(text, target_language='vi'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text