import pytesseract as pt
import cv2
import re

def getOcrResult(output_path) -> str:
    
    file_path = output_path
    preprocessed_image = cv2.imread(file_path , cv2.IMREAD_UNCHANGED)
    
    config = r'--psm 6'
    flat_string = pt.image_to_string(preprocessed_image , config = config).split("\n")
    filtered_list = [line for line in flat_string if re.search(r'[a-zA-Z0-9]' , line)]        
    result_list = "\n".join(filtered_list)

    return result_list