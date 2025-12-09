import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract
import tempfile
import os
import pytesseract
import PyPDF2
import platform

# Set up Tesseract OCR path based on platform
# For Streamlit Cloud (Linux), Tesseract is installed via packages.txt
# For local Windows development, use the Windows path
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"
# For Linux/Cloud deployment, tesseract is in PATH, no need to set explicitly


def capture_image():
    """Capture an image using webcam and save it."""
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise Exception("Could not access the webcam. Make sure it's connected and not used by another app.")

    while True:
        ret, frame = camera.read()
        if not ret:
            raise Exception("Failed to capture image from webcam.")
        
        cv2.imshow("Press 'D' to Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('d'):
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, frame)
            break
    
    camera.release()
    cv2.destroyAllWindows()
    
    return image_path


def extract_text(image_path, lang='eng'):
    """Extract text from an image using Tesseract OCR.
    
    Args:
        image_path: Path to the image file
        lang: Language code for OCR (default: 'eng')
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
    
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error loading image. The file may be corrupted or not a valid image format.")
    
    text = pytesseract.image_to_string(image, lang=lang)
    return text


def extract_text_from_pdf(pdf_file, lang='eng'):
    """Extract text from a PDF file.
    
    Args:
        pdf_file: PDF file object
        lang: Language code for OCR (default: 'eng')
    """
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
