# image2numpy
A program for bidirectional conversion between grayscale image sequences and numpy ndarrays.

## Installation
```bash
pip install image2numpy
```

## Usage
```python
import image2numpy
np_arr = image2numpy.load_png_to_3d_array("<folder_path>")           # Load all images in the folder into a 3D numpy array in lexicographical order
sub_arr = image2numpy.extract_valid_cube(np_arr)                     # Randomly extract a valid cubic subarray
image2numpy.save_3d_array_as_gray_images(sub_arr, "<target_folder>") # Save the 3D numpy array back to a sequence of grayscale images
```
