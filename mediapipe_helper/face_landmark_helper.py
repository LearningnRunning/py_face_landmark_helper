from . import config
import cv2
import numpy as np
from typing import Tuple, List, Union
from PIL import Image
import mediapipe as mp
import random



class FaceLandmarkProcessor:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh_set = self.mp_face_mesh.FaceMesh(
             static_image_mode=True,
             max_num_faces=1,
             refine_landmarks=True,
             min_detection_confidence=0.5)
        self.lmk_template_dict = config.lmk_template_dict
        self.ranges_values = config.ranges_values
        
    def operation(self, landmark, image_width, image_height) -> Tuple[int, int]:
        '''
        Performs operations on landmarks so that they stay within the image boundaries.

        :param landmark: The landmark to process.
        :param image_width: The width of the image.
        :param image_height: The height of the image.
        :return: Tuple[int, int] containing the x, y coordinates of the processed landmarks.
        '''
        return min(int(landmark.x * image_width), image_width - 1), min(int(landmark.y * image_height), image_height - 1)

    def convert_landmark(self, img_data: np.ndarray)  -> Tuple[int, int, List[Tuple[float, float, float]]]:
        '''
        Processes the input image into a face mesh model and returns face landmarks.

        Parameters:
            img_data: Input image for face mesh processing.
            img_path: Path to the input image file.

        Returns:
            Tuple containing the image width, image height, and a list of face landmarks.
        '''
        image = self.image_data_check(img_data)
        results = self.face_mesh_set.process(image)
        image_height, image_width = image.shape[:2]
        face_landmarks = results.multi_face_landmarks[0]
        face_landmarks_op = [self.operation(face_landmarks.landmark[mark], image_width, image_height) for mark in range(478)]
        return face_landmarks_op

    def image_data_check(self, img_data):
        '''
        Checks the format of input image data and returns it in a compatible format.

        Parameters:
            img_data: Input image data.
            img_path: Path to the input image file (optional).

        Returns:
            Image data in NumPy array format.

        Raises:
            ValueError: If the input image data format is not supported or invalid.
        '''
        if isinstance(img_data, str):
            image = cv2.imread(img_data)
            if image is None:
                raise ValueError("Invalid image file path")
            return image
        elif isinstance(img_data, np.ndarray):
            return img_data
        elif isinstance(img_data, Image.Image):
            return np.array(img_data)
        else:
            raise ValueError("Unsupported input type. It should be a NumPy array or a PIL image.")
    
    # Function to add the appropriate value based on the range
    def add_value(self, lmk: int) -> int:
        '''
        Returns a value associated with the given landmark index.

        Parameters:
            lmk (int): The landmark index for which to retrieve the associated value.

        Returns:
            int: The value associated with the given landmark index.
        '''
        
        for range_, value in self.ranges_values.items():
            if lmk in range_:
                return value
        return 0  # Default value if lmk is not in any range

    def invert_landmark(self, input_lmk: Union[str, int]) -> int:
        '''
        Returns the index of the symmetric point of the face landmark.

        Parameters:
            input_lmk (Union[str, int]): The input face landmark index to be inverted. 
                If provided as a string, it will be converted to an integer.
        
        Returns:
            int: The inverted face landmark index. 
                If the input is a centerline landmark or beyond the valid range, 
                it returns the input unchanged.
        '''
        
        # Elements to remove
        center_lmk_lst = self.lmk_template_dict['FACE_CENTER']

        if isinstance(input_lmk, str):
            try:
                input_lmk = int(input_lmk)
            except ValueError:
                return "Invalid input. Landmark index must be an integer."        

        if input_lmk > 468:
            return "You've gone beyond the landmark. The total range is up to 468 and the half range is up to 247."

        elif input_lmk in center_lmk_lst:
            print(f"This is a centreline landmark: {input_lmk}")
            return input_lmk

        elif isinstance(input_lmk, int):
            if input_lmk < 249:
                invert_lmk = input_lmk + self.add_value(input_lmk)
                return invert_lmk
            else:
                invert_lmk = input_lmk - self.add_value(input_lmk)
                return invert_lmk

    def invert_landmark_list(self, input_lmk_lst: List[Union[str, int]]) -> List[int]:
        '''
        Inverts a list of face landmark indices if they fall within the center landmark list.

        Parameters:
            input_lmk_lst (List[Union[str, int]]): A list of input face landmark indices to be inverted. 
                Each element can be provided as either a string or an integer.

        Returns:
            List[int]: A list containing the inverted face landmark indices. 
                If any input is a centerline landmark or beyond the valid range, 
                it returns the input unchanged.
        '''
        # Elements to remove
        center_lmk_lst = self.lmk_template_dict['FACE_CENTER']
            
        if isinstance(input_lmk_lst, list):
            # Iterate over the indices and elements of the list
            for i, lmk in enumerate(input_lmk_lst):
                # Check if the element is not an integer
                if not isinstance(lmk, int):
                    try:
                        # Try to convert the element to an integer
                        input_lmk_lst[i] = int(lmk)
                    except ValueError:
                        # Raise an error if conversion is not possible
                        raise ValueError("All elements must be convertible to integers.")

            # Convert both lists to sets
            input_lmk_set = set(input_lmk_lst)
            center_lmk_set = set(center_lmk_lst)
            
            # Find non-overlapping elements
            non_overlapping_lst = list(input_lmk_set - center_lmk_set)

            output_lmk_list = []
            
            for lmk in non_overlapping_lst:
                
                if lmk > 468:
                    return "You've gone beyond the landmark. The total range is up to 468 and the half range is up to 247."

                elif lmk < 249:
                    output_lmk_list.append(lmk + self.add_value(lmk))
                else:
                    output_lmk_list.append(lmk - self.add_value(lmk))

            return output_lmk_list
        else:
            raise ValueError("input_lmk_lst must be a list.")

            
    # Function to plot lines and points
    def plot_landmarks(self, image_tmp: np.ndarray, lmk_lst: List[int] = list(range(468)), color: Tuple[int, int, int] = (0, 255, 0), coloful_option: bool = False, draw_symmetrical_landmarks: bool = False) -> np.ndarray:
        '''
        Plots lines and points on the input image based on the provided face landmark indices.

        Parameters:
            image_tmp (np.ndarray): The input image on which to plot the landmarks. It should be a NumPy array representing the image.
            lmk_lst (List[int], optional): A list of face landmark indices to plot. Defaults to list(range(468)).
            color (Tuple[int, int, int], optional): The color to use for plotting lines and points. Defaults to (0, 255, 0) (green).
            coloful_option (bool, optional): A boolean flag indicating whether to use random colors for plotting lines and points. Defaults to False.
            draw_symmetrical_landmarks (bool, optional): A boolean flag indicating whether to draw symmetrical landmarks. Defaults to False.

        Returns:
            np.ndarray: The image with plotted lines and points.
        '''
        
        image_data = self.image_data_check(image_tmp)
        face_lmks = self.convert_landmark(image_data)
        # Extract only the index values from the list of tuples
        selected_face_lmks = [face_lmks[lmk] for lmk in lmk_lst]

        image_copy = image_data.copy()
        font_size = min(image_copy.shape[:2]) / 2800  # Adjust this factor as needed
        
        # Draw lines and points
        for landmark, lmk_idx in zip(selected_face_lmks, lmk_lst):
            # Draw lines
            # print(point1, point2)
            # Generate random BGR color
            if coloful_option:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # cv2.line(image_copy, landmark[0], landmark[1], color, thickness=line_size)
            # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            cv2.putText(image_copy, str(lmk_idx), landmark, cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 1, cv2.LINE_AA)
            cv2.circle(image_copy, landmark, 1, color, -1)
            if draw_symmetrical_landmarks:
                lmk_invert = self.invert_landmark(lmk_idx)
                face_lmks_invert = face_lmks[lmk_invert]
                cv2.putText(image_copy, str(lmk_invert), face_lmks_invert, cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 1, cv2.LINE_AA)
                
                # Draw points
                cv2.circle(image_copy, face_lmks_invert, 1, color, -1)
        img_rgb = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
        return img_rgb

    def mesh_template(self, input_key: str = 'ALL') -> Union[str, List[str]]:
        '''
        Retrieves the template list or a specific template based on the input key.

        Parameters:
            input_key (str, optional): The key of the template to retrieve. 
                Defaults to 'ALL', which retrieves the entire template list.

        Returns:
            Union[str, List[str]]: The template list or the specific template corresponding to the input key.
                Returns a list if input_key is 'ALL', otherwise returns a string.
        '''
        if input_key == 'ALL':
            template_lst = list(self.lmk_template_dict.keys())
            return f"""This is Template List, {template_lst} Usage examples: mesh_template('FACE_LIPS')"""
        
        else:
            answer = self.lmk_template_dict.get(input_key)
            if answer:
                return answer
            else:
                return f"""{input_key} does not exist, please open an issue to request it be added. 'https://github.com/LearningnRunning/py_face_landmark_helper/issues'"""
    