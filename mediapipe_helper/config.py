import json
import os

# print(os.getcwd())
# Specify the file path of the JSON file
json_file_path = "mediapipe_helper/assets/lmk_template_dict.json"

# Define the ranges and corresponding values to add
ranges_values = {
    range(20, 94): 230,
    range(94, 153): 229,
    range(153, 164): 227,
    range(165, 168): 226,
    range(169, 175): 225,
    range(176, 195): 224,
    range(196, 197): 223,
    range(198, 199): 222,
    range(201, 248): 220,
    range(468, 473) : 5,
    range(3,4) : 245,
    range(7,8) : 242
    
}
        
# Load the JSON file and retrieve the dictionary
with open(json_file_path, "r") as json_file:
    lmk_template_dict = json.load(json_file)