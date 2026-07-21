import cv2 
import secrets
from pathlib import Path

def image_processing(file_path):

    image = cv2.imread(file_path)
    
    if image is not None:
    
        #convert to grayscale 
    
        grayscaled_image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
        
        #crop
        #edge detection using canny function hypotenuse algo 
        
        edge = cv2.Canny(grayscaled_image , 50 , 150)

    
        #getting the biggest area boundary / contour
        contours , hierarchy= cv2.findContours(edge , cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE) # return tuple (contours , hierarchy)
        biggest_contour = max(contours , key=cv2.contourArea)
    
        center , (width , height) , angle = cv2.minAreaRect(biggest_contour) 
    
        if angle < -45:
            angle = 90 + angle 
            (height , width) = (width , height)
    
        m = cv2.getRotationMatrix2D(center , angle , 1.0)
        rotated = cv2.warpAffine(image , m , image.shape[:2][::-1])
        deskewed = cv2.getRectSubPix(rotated , (int(width) , int(height)) , center) 
    
        gray_deskewed = cv2.cvtColor(deskewed , cv2.COLOR_BGR2GRAY)
    
        denoise_image = cv2.fastNlMeansDenoising(gray_deskewed , h=5 , searchWindowSize=21, templateWindowSize=7)
    
        adaptive_threshold_image = cv2.adaptiveThreshold(denoise_image , 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C , thresholdType=cv2.THRESH_BINARY , 
            blockSize=15 , C = 2)

        secret_token = secrets.token_urlsafe()
        output_path = str(Path(__file__).parent) + "/images/" + secret_token +".png"
        cv2.imwrite(output_path  , adaptive_threshold_image)

        return output_path
  
    