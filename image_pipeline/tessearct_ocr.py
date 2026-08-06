# import pytesseract as pt
import cv2
from PIL import Image


def getOcrResult(output_path , model , image_processor , easyocr_reader) -> str:



    #OLD TESSERACT CODE 
    # ----------------------------------------------------------
    
    # file_path = output_path
    # preprocessed_image = cv2.imread(file_path , cv2.IMREAD_UNCHANGED)
    
    # config = r'--psm 6'
    # flat_string = pt.image_to_string(preprocessed_image , config = config).split("\n")
    # filtered_list = [line for line in flat_string if re.search(r'[a-zA-Z0-9]' , line)]        
    # result_list = "\n".join(filtered_list)

    # return result_list

    # ----------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------
    #NEW OCR CODE 
    

    file_path = output_path
    preprocessed_image = cv2.imread(file_path , cv2.IMREAD_UNCHANGED)
    
    result = easyocr_reader.detect(preprocessed_image)

    horizontal_list = result[0][0]

    img_test = preprocessed_image.copy()

    visited_list = []
    finished_groups = []
    stack = []

    for box in horizontal_list:
        if box in visited_list:
            continue 
        else:

            stack.append(box)
            brand_new_group = []

            while len(stack) != 0:

                main_box = stack.pop()

                if main_box not    in visited_list:
                    visited_list.append(main_box)

                    brand_new_group.append(main_box)

                x_min_main , x_max_main , y_min_main , y_max_main = main_box
                threshold = (y_max_main + y_min_main)/2
                

                for another_box in horizontal_list:
                    _ , _ , y_min_another , y_max_another = another_box
                    another_threshold = (y_max_another + y_min_another)/2
                    if another_box not in visited_list and ((y_min_another <= threshold and y_max_another >= threshold) or (y_min_main <= another_threshold and y_max_main >= another_threshold)):
                        brand_new_group.append(another_box)
                        stack.append(another_box)
                        visited_list.append(another_box)
            
            finished_groups.append(brand_new_group)

    for group in finished_groups:
        group.sort(key = lambda x : x[0])

    finished_groups.sort(key = lambda group : max([item[3] for item in group])) 


    results_array = []
    
    for group in finished_groups:

        group_text = []
        
        for box in group:
            x_min , x_max , y_min , y_max = box
            img = img_test[y_min : y_max , x_min : x_max].copy()

            converted_image = Image.fromarray(cv2.cvtColor(img , cv2.COLOR_BGR2RGB))
          
            inputs = image_processor(images=converted_image, return_tensors="pt").to(model.device)
            outputs = model(**inputs)
            results = image_processor.post_process_text_recognition(outputs)
      
            group_text.append(results[0]["text"])
        
        results_array.append(" ".join(group_text))       
        
        
    

    return "\n".join(results_array)
        
        
    
# ----------------------------------------------------------------------------------










# file = cv2.imread("real_sample_handwritten.jpg")
# result = pt.image_to_data(file , output_type=pt.pytesseract.Output.DICT)
# dict_words = {}

# for i in range(len(result["level"])):
#     if result["level"][i] == 5 and result["text"][i] != '':
#         key = (result["block_num"][i] , result["par_num"][i] , result["line_num"][i])

#         if key not in dict_words:
#             dict_words[key] = []

#         dict_words[key].append({"text" : result["text"][i] , "left" : result["left"][i] , "top" : result["top"][i] , 
#             "width" : result["width"][i] , "height" : result["height"][i]})

# for key in dict_words.keys():

#     min_left = dict_words[key][0]["left"]
#     min_top = dict_words[key][0]["top"]
#     max_left_plus_width = dict_words[key][0]["left"] + dict_words[key][0]["width"]
#     max_top_plus_height = dict_words[key][0]["top"] + dict_words[key][0]["height"]
#     list_text = []
     
#     for entry in dict_words[key]:
#         min_left = min(entry["left"] , min_left)
#         min_top = min(entry["top"] , min_top)
#         max_left_plus_width = max(entry["left"] + entry["width"] , max_left_plus_width)
#         max_top_plus_height = max(entry["top"] + entry["height"] , max_top_plus_height)
#         list_text.append(entry["text"])

#     dict_words[key] = {"text_list" : list_text , "min_left" : min_left , "min_top" : min_top , "max_left_plus_width" : max_left_plus_width , "max_top_plus_height" : max_top_plus_height , "extended_right" : file.shape[1]}
    
# for key in dict_words.keys():
#     dict_words[key]["image"] = file[dict_words[key]["min_top"] : dict_words[key]["max_top_plus_height"] , dict_words[key]["min_left"] : dict_words[key]["extended_right"]]

# print(dict_words)