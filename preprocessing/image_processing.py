import cv2 

image = cv2.imread("sample_form.jpg")

if image is not None:

    #convert to grayscale 

    grayscaled_image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    
    #crop
    #edge detection using canny function hypotenuse algo 
    
    edge = cv2.Canny(grayscaled_image , 50 , 150)
    cv2.imwrite("images/edge_detection_canny.jpg" , edge)
    

    #getting the biggest area boundary / contour
    contours , hierarchy= cv2.findContours(edge , cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE) # return tuple (contours , hierarchy)
    biggest_contour = max(contours , key=cv2.contourArea)

    x , y , w , h = cv2.boundingRect(biggest_contour)

    cropped = image[y: y+h , x : x+w ]
    cv2.imwrite("images/cropped_image.jpg" , cropped)

    print(cv2.minAreaRect(biggest_contour))