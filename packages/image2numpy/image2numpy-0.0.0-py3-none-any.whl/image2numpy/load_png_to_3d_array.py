import os
import numpy as np
from PIL import Image
from typing import List

def load_png_to_3d_array(folder_path: str) -> np.ndarray:
    """
    Read all PNG files from the specified folder, convert them to L-mode grayscale images, 
    and concatenate them into a 3D numpy array

    Args:
        folder_path: Path to the folder containing PNG files

    Returns:
        3D numpy array with shape (number of images, height, width)

    Raises: 
        FileNotFoundError: If the folder does not exist
        ValueError: If no PNG files are found in the folder / Image dimensions are inconsistent
        IOError: If image files are corrupted or cannot be read
    """
    
    # 1. Verify if the folder exists
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")
    
    # 2. Get all PNG files in the folder (sorted by filename)
    png_files = [
        os.path.join(folder_path, f)
        for f in sorted(os.listdir(folder_path))  # Sort by filename to ensure order
        if f.lower().endswith('.png')  # Case-insensitive (supports .PNG/.png)
    ]
    
    # 3. Verify if there are any PNG files
    if not png_files:
        raise ValueError(f"No PNG files found in folder {folder_path}")
    
    # 4. Read and process all PNG files
    img_2d_arrays: List[np.ndarray] = []
    target_shape = None  # Store the reference image dimensions (height, width)
    
    for idx, img_path in enumerate(png_files):
        try:
            # Open the image and convert to L-mode (8-bit grayscale)
            with Image.open(img_path) as img:
                # Convert to L-mode grayscale image
                gray_img = img.convert('L')
                # Convert to 2D numpy array
                img_array = np.array(gray_img)
                
                # 5. Verify image dimensions
                if target_shape is None:
                    # Use the first image as the reference dimension
                    target_shape = img_array.shape
                else:
                    if img_array.shape != target_shape:
                        raise ValueError(
                            f"Inconsistent image dimensions!\n"
                            f"Reference image (1st image) dimensions: {target_shape} (height × width)\n"
                            f"Abnormal image ({idx+1}th image): {img_path}, dimensions: {img_array.shape}"
                        )
                
                img_2d_arrays.append(img_array)
        
        except IOError as e:
            raise IOError(f"Failed to read image: {img_path}, error message: {str(e)}")
    
    # 6. Concatenate into a 3D numpy array (shape: (count, height, width))
    img_3d_array = np.stack(img_2d_arrays, axis=0)
    return img_3d_array