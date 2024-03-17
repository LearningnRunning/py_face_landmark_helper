# py_face_landmark_helper
A package to help you utilise landmarks in the face_landmark feature of google open source mediapipe.



## Installation

To install the mediapipe_helper library, you can use pip:

```bash
pip install mediapipe_helper
```

or

```bash
git clone https://github.com/LearningnRunning/py_face_landmark_helper

python setup.py install
```
# Create an instance of FaceMeshProcessor

```python
from mediapipe_helper import face_landmark_helper

# Create an instance of FaceMeshProcessor
face_mesh_processor = face_landmark_helper.FaceLandmarkProcessor()
```

## convert_landmark
 Image Path or Image Object, whatever you want.<br/>

- face_landmarks is a list of 468 landmarks extracted from the facial image. Each landmark is represented as a tuple containing the x and y coordinates in pixels.

### Using Image Path
```python

img_path = 'image_path.jpg'

# Call the convert_landmark method to get the face landmarks
face_landmarks = face_mesh_processor.convert_landmark(img_path)
# OUTPUT: [(270, 492), (276, 453), (274, 464), (267, 400), (277, 439), (279, 418), (282, 362), (176, 338), (285, 318), (287, 297), (293, 223), (270, 497), (269, 503), (268, 507), (268, 515),  ...]
```

### Using Image Object

```python
import cv2

image_path = 'image_path.jpg'

# Load the image using cv2.imread()
image = cv2.imread(image_path)

# Call the convert_landmark method to get the face landmarks
face_landmarks = face_mesh_processor.convert_landmark(image)
# OUTPUT: [(270, 492), (276, 453), (274, 464), (267, 400), (277, 439), (279, 418), (282, 362), (176, 338), (285, 318), (287, 297), (293, 223), (270, 497), (269, 503), (268, 507), (268, 515),  ...]

```
## Finding symmetric indexes
Entering index tells you the index of the landmark that is symmetrical to the center line of the face.

### invert_landmark
```python
lmk_idx = 170
lmk_invert = face_mesh_processor.invert_landmark(lmk_idx)
# OUTPUT: 395
```

### invert_landmark_list
```python
lmk_idx = [170, 171, 180, 190]
lmk_invert_list = face_mesh_processor.invert_landmark_list(lmk_idx)
# OUTPUT: [395, 396, 404, 414]
```
### How to utilize indexes
```python
# Load the image using cv2.imread()
image = cv2.imread(image_path)

# Call the convert_landmark method to get the face landmarks
face_landmarks = face_mesh_processor.convert_landmark(image)

# Use the face_landmarks list to access the coordinates of the landmark at index lmk_idx
lmk_coordinates = face_landmarks[lmk_idx]
print("Coordinates of landmark at index", lmk_idx, ":", lmk_coordinates)

# Example of inverting index and accessing corresponding landmark
lmk_invert = face_mesh_processor.invert_landmark(lmk_idx)
# Use the inverted index to access the corresponding landmark
lmk_inverted_coordinates = face_landmarks[lmk_invert]
print("Coordinates of landmark at inverted index", lmk_invert, ":", lmk_inverted_coordinates)

# Coordinates of landmark at index 170 : (189, 553)
# Coordinates of landmark at inverted index 395 : (333, 562)
```

## Landmark list template by facial part

```python
#  Look up template types
face_mesh_processor.mesh_template()
# OUTPUT: This is Template List, ['FACE_CONTOURS', 'FACE_FACE_OVAL', 'FACE_IRISES', 'FACE_LEFT_EYE', 'FACE_LEFT_EYEBROW', 'FACE_LEFT_IRIS', 'FACE_LIPS', 'FACE_NOSE', 'FACE_RIGHT_EYE', 'FACE_RIGHT_EYEBROW', 'FACE_RIGHT_IRIS', 'FACE_TESSELATION', 'FACE_CENTER'] 


# Usage examples: mesh_template('FACE_LIPS')
lmd_mark = face_mesh_processor.mesh_template('FACE_LIPS')
# OUTPUT : [0, 267, 269, 270, 13, 14, 17, 402, 146, 405, 409, 415, 291, 37, 39, 40, 178, 308, 181, 310, 311, 312, 185, 314, 317, 318, 61, 191, 321, 324, 78, 80, 81, 82, 84, 87, 88, 91, 95, 375]
```


## Landmark list template by facial part
```python
image_path = 'image_path.jpg'
# Usage examples: mesh_template('FACE_LIPS')
lmd_mark = face_mesh_processor.mesh_template('FACE_LIPS')

plot_img = face_mesh_processor.plot_landmarks(img_path, lmk_lst=lmd_mark)
# OUTPUT: array([[[165, 173, 167],[164, 174, 167],[165, 174, 167)
```
plot_img
![plot_img](https://velog.velcdn.com/images/sungrok7/post/5a3a5b69-5705-4ab6-bf29-2317761f3263/image.png)

### plot_landmarks's Parameters
Parameters:<br/>
    image_tmp (np.ndarray): The input image on which to plot the landmarks. It should be a NumPy array representing the image.<br/>
    lmk_lst (List[int], optional): A list of face landmark indices to plot. Defaults to list(range(468)).<br/>
    color (Tuple[int, int, int], optional): The color to use for plotting lines and points. Defaults to (0, 255, 0) (green).<br/>
    coloful_option (bool, optional): A boolean flag indicating whether to use random colors for plotting lines and points. Defaults to False.<br/>
    draw_symmetrical_landmarks (bool, optional): A boolean flag indicating whether to draw symmetrical landmarks. Defaults to False.<br/>

```python
user_color = (122, 143, 12)
plot_img_user_color = face_mesh_processor.plot_landmarks(img_path, lmk_lst=lmd_mark, color=user_color)

plot_img_colorful_sym = face_mesh_processor.plot_landmarks(img_path, lmk_lst=lmd_mark, coloful_option=True, draw_symmetrical_landmarks=True)
```
plot_img_user_color
![plot_img_user_color](https://velog.velcdn.com/images/sungrok7/post/92446ddb-642b-43b5-b48f-64a3aaf65a42/image.png)
plot_img_colorful_sym
![plot_img_colorful_sym](https://velog.velcdn.com/images/sungrok7/post/82cd4fcd-3754-4522-ab54-33474a4795c2/image.png)

## Display the image

```python
import matplotlib.pyplot as plt

# Assuming you have an image array named plot_img
plt.axis('off')  # Remove axes
plt.imshow(plot_img)
plt.show()  # Display the image without printing anything

from PIL import Image
Image.fromarray(plot_img)
```

## License
mediapipe_helper is provided under the Apache License 2.0. 

