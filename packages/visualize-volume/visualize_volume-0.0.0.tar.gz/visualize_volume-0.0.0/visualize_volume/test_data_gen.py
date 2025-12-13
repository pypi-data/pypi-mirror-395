import numpy as np

def create_centered_cube_3d(array_shape: tuple, cube_size: int) -> np.ndarray:
    """
    Creates a 3D NumPy array with a cube of value -1 at the exact center, and 0 elsewhere.
    
    Args:
        array_shape: The shape of the 3D array, formatted as (depth, height, width).
        cube_size: The side length of the cube (must be less than or equal to the size of each array dimension).
    
    Returns:
        A 3D ndarray with the central cube having a value of -1 and the rest being 0.
    """
    # Validate input validity
    if len(array_shape) != 3:
        raise ValueError("array_shape must be a 3D tuple (depth, height, width)")
    if cube_size <= 0 or any(cube_size > dim for dim in array_shape):
        raise ValueError(f"Cube side length {cube_size} must be greater than 0 and less than or equal to the size of each array dimension {array_shape}")
    
    # 1. Create a 3D array initialized to zeros
    volume = np.zeros(array_shape, dtype=np.int8)
    
    # 2. Calculate the center coordinates of the array (center index for each dimension)
    center_depth, center_height, center_width = (dim // 2 for dim in array_shape)
    
    # 3. Calculate the start and end indices of the cube in each dimension (ensuring the cube is centered)
    # Start Index = Center Point - Cube Size // 2
    # End Index = Start Index + Cube Size
    start_d = center_depth - cube_size // 2
    end_d = start_d + cube_size
    start_h = center_height - cube_size // 2
    end_h = start_h + cube_size
    start_w = center_width - cube_size // 2
    end_w = start_w + cube_size
    
    # 4. Assign the value -1 to the cube region
    volume[start_d:end_d, start_h:end_h, start_w:end_w] = -1
    
    return volume