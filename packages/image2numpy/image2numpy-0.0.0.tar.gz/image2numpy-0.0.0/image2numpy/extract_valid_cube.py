import numpy as np
import random

def extract_valid_cube(
    arr_3d: np.ndarray,
    min_size: int = 3,
    threshold: int = 128,
    min_ratio: float = 0.3,
    max_attempts: int = 1000
) -> np.ndarray:
    """
    Randomly extract a valid cubic subarray from a 3D numpy array
    
    Args:
        arr_3d: Input 3D numpy array
        min_size: Minimum edge length of the subarray (default: 50)
        threshold: Threshold value (default: 128)
        min_ratio: Minimum proportion (0-1) required for both categories of elements (default: 0.3, i.e., 30%)
        max_attempts: Maximum number of random attempts (default: 1000)
    
    Returns:
        A valid 3D cubic subarray that meets the criteria
    
    Raises:
        ValueError: If no valid subarray is found after maximum attempts, or if input array dimensions are insufficient
    """
    # Check the validity of the input array
    if arr_3d.ndim != 3:
        raise ValueError("Input must be a 3D numpy array")
    
    # Get the 3D dimensions of the original array
    dim1, dim2, dim3 = arr_3d.shape
    
    # Check if the original array can accommodate at least the minimum size subarray
    if min(dim1, dim2, dim3) < min_size:
        raise ValueError(f"Minimum dimension of input array ({min(dim1, dim2, dim3)}) is smaller than required minimum size ({min_size})")
    
    # Start random attempts to extract subarray
    for attempt in range(max_attempts):
        # 1. Randomly select edge length of the subarray (no less than min_size, no more than min dimension of original array)
        max_possible_size = min(dim1, dim2, dim3)
        cube_size = random.randint(min_size, max_possible_size)
        
        # 2. Calculate the range of starting indices for each dimension
        start1_max = dim1 - cube_size
        start2_max = dim2 - cube_size
        start3_max = dim3 - cube_size
        
        # 3. Randomly select starting indices for each dimension
        start1 = random.randint(0, start1_max)
        start2 = random.randint(0, start2_max)
        start3 = random.randint(0, start3_max)
        
        # 4. Extract the subarray
        sub_cube = arr_3d[
            start1:start1 + cube_size,
            start2:start2 + cube_size,
            start3:start3 + cube_size
        ]
        
        # 5. Calculate the proportion of the two categories of elements
        total_elements = cube_size **3  # Total number of elements in the cube
        count_below = np.sum(sub_cube < threshold)
        count_above_eq = np.sum(sub_cube >= threshold)
        
        ratio_below = count_below / total_elements
        ratio_above_eq = count_above_eq / total_elements
        
        # 6. Check if the proportion requirements are met
        if ratio_below >= min_ratio and ratio_above_eq >= min_ratio:
            return sub_cube
    
    # If no valid subarray is found after all attempts
    raise ValueError(f"No valid subarray found after {max_attempts} attempts. Please check the input array or adjust parameters")