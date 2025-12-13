"""Image compositing module for creating alternating row/column composites."""

from PIL import Image
import numpy as np
from typing import Literal


def create_solid_image(color: str, width: int, height: int) -> np.ndarray:
    """
    Create a solid color image array.
    
    Args:
        color: 'white' or 'black'
        width: Image width in pixels
        height: Image height in pixels
        
    Returns:
        RGB image array filled with the solid color
        
    Raises:
        ValueError: If color is not 'white' or 'black'
    """
    if color.lower() not in ('white', 'black'):
        raise ValueError(f"Color must be 'white' or 'black', got '{color}'")
    
    color_value = 255 if color.lower() == 'white' else 0
    return np.full((height, width, 3), color_value, dtype=np.uint8)


def tile_image(image_array: np.ndarray, target_height: int, target_width: int) -> np.ndarray:
    """
    Tile an image to match target dimensions.
    
    Args:
        image_array: The image array to tile
        target_height: Target height in pixels
        target_width: Target width in pixels
        
    Returns:
        Tiled image array with exact target dimensions
    """
    current_height, current_width = image_array.shape[:2]
    
    # Calculate how many times to tile in each direction
    tiles_y = (target_height + current_height - 1) // current_height
    tiles_x = (target_width + current_width - 1) // current_width
    
    # Tile the image
    if len(image_array.shape) == 3:
        tiled = np.tile(image_array, (tiles_y, tiles_x, 1))
    else:
        tiled = np.tile(image_array, (tiles_y, tiles_x))
    
    # Crop to exact target dimensions
    return tiled[:target_height, :target_width]


def validate_and_load_images(image1_path: str, image2_path: str) -> tuple:
    """
    Load two images and resize/tile them to match dimensions.
    
    If images have different dimensions, the smaller image is tiled to match
    the larger image's dimensions.
    
    Accepts image file paths or color names ('white' or 'black') for solid colors.
    
    Args:
        image1_path: Path to the first image, or 'white'/'black' for solid color
        image2_path: Path to the second image, or 'white'/'black' for solid color
        
    Returns:
        Tuple of (img1_array, img2_array) with matching dimensions
    """
    # Load or create first image
    if image1_path.lower() in ('white', 'black'):
        # Need to get dimensions from the other image first
        if image2_path.lower() in ('white', 'black'):
            raise ValueError("At least one image path must be a file (not both 'white' or 'black')")
        temp_img = Image.open(image2_path)
        width, height = temp_img.size
        img1_array = create_solid_image(image1_path, width, height)
        img1_mode = 'RGB'
    else:
        img1 = Image.open(image1_path)
        img1_mode = img1.mode
        img1_array = None
    
    # Load or create second image
    if image2_path.lower() in ('white', 'black'):
        if image1_path.lower() in ('white', 'black'):
            raise ValueError("At least one image path must be a file (not both 'white' or 'black')")
        if img1_array is None:
            temp_img = Image.open(image1_path)
            width, height = temp_img.size
        img2_array = create_solid_image(image2_path, width, height)
        img2_mode = 'RGB'
    else:
        img2 = Image.open(image2_path)
        img2_mode = img2.mode
        img2_array = None
    
    # Load first image if not already loaded
    if img1_array is None:
        img1 = Image.open(image1_path)
        img1_mode = img1.mode
    else:
        img1 = None
    
    # Load second image if not already loaded
    if img2_array is None:
        img2 = Image.open(image2_path)
        img2_mode = img2.mode
    else:
        img2 = None
    
    # Convert palette and other modes to RGB for consistency
    if img1 is not None and img1.mode in ('P', '1', 'L', 'RGBA'):
        img1 = img1.convert("RGB")
    if img2 is not None and img2.mode in ('P', '1', 'L', 'RGBA'):
        img2 = img2.convert("RGB")
    
    # Convert to same mode if different
    if img1 is not None and img2 is not None and img1.mode != img2.mode:
        img1 = img1.convert("RGB")
        img2 = img2.convert("RGB")
    
    # Get dimensions
    if img1 is not None:
        width1, height1 = img1.size
    else:
        height1, width1 = img1_array.shape[:2]
    
    if img2 is not None:
        width2, height2 = img2.size
    else:
        height2, width2 = img2_array.shape[:2]
    
    # Determine target dimensions (use the larger dimensions)
    target_height = max(height1, height2)
    target_width = max(width1, width2)
    
    # Convert to arrays if not already done
    if img1_array is None:
        img1_array = np.array(img1)
    if img2_array is None:
        img2_array = np.array(img2)
    
    # Tile images if they're smaller than the target
    if (height1, width1) != (target_height, target_width):
        img1_array = tile_image(img1_array, target_height, target_width)
    
    if (height2, width2) != (target_height, target_width):
        img2_array = tile_image(img2_array, target_height, target_width)
    
    return img1_array, img2_array


def composite_rows(image1_path: str, image2_path: str, output_path: str) -> None:
    """
    Create a composite image by interleaving rows from two images.
    
    Output structure:
    - Row 0: from image1 row 0
    - Row 1: from image2 row 0
    - Row 2: from image1 row 1
    - Row 3: from image2 row 1
    - etc.
    
    The output image height will be 2x the input height.
    
    Args:
        image1_path: Path to the first input image
        image2_path: Path to the second input image
        output_path: Path to save the output composite image
    """
    img1_array, img2_array = validate_and_load_images(image1_path, image2_path)
    
    height, width = img1_array.shape[:2]
    
    # Create output array with 2x height (interleaved rows)
    if len(img1_array.shape) == 3:
        output = np.zeros((height * 2, width, img1_array.shape[2]), dtype=img1_array.dtype)
    else:
        output = np.zeros((height * 2, width), dtype=img1_array.dtype)
    
    # Interleave rows: odd rows from img1, even rows from img2
    output[::2] = img1_array   # Rows 0, 2, 4, ... from image1
    output[1::2] = img2_array  # Rows 1, 3, 5, ... from image2
    
    # Save the result
    result_image = Image.fromarray(output)
    result_image.save(output_path)


def composite_columns(image1_path: str, image2_path: str, output_path: str) -> None:
    """
    Create a composite image by interleaving columns from two images.
    
    Output structure:
    - Column 0: from image1 column 0
    - Column 1: from image2 column 0
    - Column 2: from image1 column 1
    - Column 3: from image2 column 1
    - etc.
    
    The output image width will be 2x the input width.
    
    Args:
        image1_path: Path to the first input image
        image2_path: Path to the second input image
        output_path: Path to save the output composite image
    """
    img1_array, img2_array = validate_and_load_images(image1_path, image2_path)
    
    height, width = img1_array.shape[:2]
    
    # Create output array with 2x width (interleaved columns)
    if len(img1_array.shape) == 3:
        output = np.zeros((height, width * 2, img1_array.shape[2]), dtype=img1_array.dtype)
    else:
        output = np.zeros((height, width * 2), dtype=img1_array.dtype)
    
    # Interleave columns: odd columns from img1, even columns from img2
    output[:, ::2] = img1_array   # Columns 0, 2, 4, ... from image1
    output[:, 1::2] = img2_array  # Columns 1, 3, 5, ... from image2
    
    # Save the result
    result_image = Image.fromarray(output)
    result_image.save(output_path)


def composite(
    image1_path: str, 
    image2_path: str, 
    output_path: str, 
    mode: Literal['rows', 'columns'] = 'rows'
) -> None:
    """
    Create a composite image by alternating rows or columns from two images.
    
    Args:
        image1_path: Path to the first input image
        image2_path: Path to the second input image
        output_path: Path to save the output composite image
        mode: 'rows' to alternate rows, 'columns' to alternate columns
        
    Raises:
        ValueError: If mode is not 'rows' or 'columns', or if images don't match
    """
    if mode not in ('rows', 'columns'):
        raise ValueError(f"Mode must be 'rows' or 'columns', got '{mode}'")
    
    if mode == 'rows':
        composite_rows(image1_path, image2_path, output_path)
    else:
        composite_columns(image1_path, image2_path, output_path)


def interlace_rows(image1_path: str, image2_path: str, output_path: str) -> None:
    """
    Create a same-size interlaced image by taking alternating rows from two images.

    Behavior:
    - Output has the same height/width as the (tiled) input images
    - Output rows at even indices come from `image1`'s corresponding even rows
    - Output rows at odd indices come from `image2`'s corresponding odd rows

    Args:
        image1_path: Path to the first input image
        image2_path: Path to the second input image
        output_path: Path to save the output interlaced image
    """
    img1_array, img2_array = validate_and_load_images(image1_path, image2_path)

    height, width = img1_array.shape[:2]

    # Create output array with same shape
    if len(img1_array.shape) == 3:
        output = np.zeros((height, width, img1_array.shape[2]), dtype=img1_array.dtype)
    else:
        output = np.zeros((height, width), dtype=img1_array.dtype)

    # Interlace rows in-place using corresponding row indices
    output[::2] = img1_array[::2]
    output[1::2] = img2_array[1::2]

    result_image = Image.fromarray(output)
    result_image.save(output_path)


def interlace_columns(image1_path: str, image2_path: str, output_path: str) -> None:
    """
    Create a same-size interlaced image by taking alternating columns from two images.

    Behavior:
    - Output has the same height/width as the (tiled) input images
    - Output columns at even indices come from `image1`'s corresponding even columns
    - Output columns at odd indices come from `image2`'s corresponding odd columns
    
    Args:
        image1_path: Path to the first input image
        image2_path: Path to the second input image
        output_path: Path to save the output interlaced image
    """
    img1_array, img2_array = validate_and_load_images(image1_path, image2_path)

    height, width = img1_array.shape[:2]

    # Create output array with same shape
    if len(img1_array.shape) == 3:
        output = np.zeros((height, width, img1_array.shape[2]), dtype=img1_array.dtype)
    else:
        output = np.zeros((height, width), dtype=img1_array.dtype)

    # Interlace columns in-place using corresponding column indices
    output[:, ::2] = img1_array[:, ::2]
    output[:, 1::2] = img2_array[:, 1::2]

    result_image = Image.fromarray(output)
    result_image.save(output_path)


def interlace(
    image1_path: str, 
    image2_path: str, 
    output_path: str, 
    mode: Literal['rows', 'columns'] = 'rows'
) -> None:
    """
    Wrapper to call interlace_rows or interlace_columns based on `mode`.
    """
    if mode not in ('rows', 'columns'):
        raise ValueError(f"Mode must be 'rows' or 'columns', got '{mode}'")

    if mode == 'rows':
        interlace_rows(image1_path, image2_path, output_path)
    else:
        interlace_columns(image1_path, image2_path, output_path)
