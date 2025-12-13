import numpy as np
import cv2
import os

def save_3d_array_as_gray_images(
    arr_3d: np.ndarray,
    save_dir: str,
    filename_format: str = "{:04d}.png"  # Default 4-digit zero-padding format, e.g., 0000.png, 0001.png
) -> None:
    """
    Save a 3D numpy array as a sequence of grayscale images by slicing along the depth dimension
    
    Args:
        arr_3d: Input 3D numpy array (dimension order: [depth, height, width])
        save_dir: Directory path for saving the images
        filename_format: Filename format string, default "{:04d}.png" means 4-digit zero-padding
    
    Raises:
        ValueError: If input is not a 3D array, or if the target directory already exists (to prevent overwriting)
        OSError: If directory creation fails or images cannot be saved
    """
    # 1. Validate input array dimensions
    if arr_3d.ndim != 3:
        raise ValueError(f"Input must be a 3D numpy array. Current dimensions: {arr_3d.ndim}")
    
    # Check if target directory already exists (prevent accidental overwriting)
    if os.path.isdir(save_dir):
        raise ValueError(f"Target directory already exists: {save_dir}. "
                         "To avoid overwriting existing files, please use a non-existent directory path.")
    
    # 2. Create save directory (if it doesn't exist)
    try:
        os.makedirs(save_dir, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create directory {save_dir}: {str(e)}")
    
    # 3. Clip array values to the range [0, 255]
    # clip function: set values ≤0 to 0, ≥255 to 255, keep intermediate values unchanged
    arr_clipped = np.clip(arr_3d, 0, 255)
    
    # 4. Convert to 8-bit unsigned integer (standard format for grayscale images)
    arr_8bit = arr_clipped.astype(np.uint8)
    
    # 5. Save each slice as a grayscale image
    total_slices = arr_8bit.shape[0]
    for slice_idx in range(total_slices):
        # Get current slice
        current_slice = arr_8bit[slice_idx, :, :]
        
        # Generate filename (following the specified format, e.g., 0000.png, 0001.png)
        filename = filename_format.format(slice_idx)
        save_path = os.path.join(save_dir, filename)
        
        # Save grayscale image (cv2.IMWRITE_PNG_COMPRESSION=0 means no compression, adjust as needed)
        success = cv2.imwrite(
            save_path,
            current_slice,
            [cv2.IMWRITE_PNG_COMPRESSION, 0]
        )
        
        if not success:
            raise OSError(f"Failed to save image to: {save_path}")