from PIL import Image
import pytesseract
import cv2

def ocr_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

if __name__ == "__main__":
    path = input("Enter path to image: ")
    print("\nExtracted Text:\n", ocr_from_image(path))
