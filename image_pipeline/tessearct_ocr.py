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