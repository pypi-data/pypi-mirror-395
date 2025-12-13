#Import
from PIL import Image, ImageEnhance
import math
from typing import Generator, Tuple


def load_image(path: str) -> Image.Image:
    return Image.open(path)

#Brightness
def adjust_brightness(img: Image.Image, factor: float) -> Image.Image:
    if not isinstance(img, Image.Image):
        raise TypeError("Input must be a PIL Image object.")
    
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

#Saturation
def adjust_saturation(img: Image.Image, factor: float) -> Image.Image:
    """
    Adjusts the intensity of colors (saturation).
    
    Args:
        img: Input PIL Image object
        factor: Saturation adjustment factor
            - 1.0 = original
            - 0.0 = grayscale
            - > 1.0 = more vibrant colors
            
    Returns:
        PIL.Image.Image: Saturation-adjusted image
        
    Raises:
        TypeError: If img is not a PIL Image object
        
    Example:
        >>> vibrant = adjust_saturation(img, 1.4)  # 40% more saturated
        >>> grayscale = adjust_saturation(img, 0.0)  # Black & white
    """
    if not isinstance(img, Image.Image):
        raise TypeError("Input must be a PIL Image object.")
        
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)

#Sharpness
def adjust_sharpness(img: Image.Image, factor: float) -> Image.Image:
    """
    Adjusts the image sharpness.
    
    Args:
        img: Input PIL Image object
        factor: Sharpness adjustment factor
            - 1.0 = original
            - > 1.0 = sharper
            - < 1.0 = blurrier
            
    Returns:
        PIL.Image.Image: Sharpness-adjusted image
        
    Raises:
        TypeError: If img is not a PIL Image object
        
    Example:
        >>> sharp = adjust_sharpness(img, 2.0)  # Very sharp
        >>> soft = adjust_sharpness(img, 0.5)  # Soft focus
    """
    if not isinstance(img, Image.Image):
        raise TypeError("Input must be a PIL Image object.")
        
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)


#Shadows
def adjust_shadows(img: Image.Image, amount: float) -> Image.Image:
    if not isinstance(img, Image.Image):
        raise TypeError("Input must be a PIL Image object.")
        
    img = img.convert("RGB")
    
    def shadow_curve(x):
        """Applies a gamma-like curve only to dark pixels."""
        x_norm = x / 255.0
        # Ensure the amount is clipped to prevent extreme gamma values
        gamma_exponent = max(-2.0, min(2.0, -amount))
        gamma = math.pow(2, gamma_exponent) 
        result_norm = math.pow(x_norm, gamma)
        return int(result_norm * 255)

    lut = [shadow_curve(i) for i in range(256)]
    
    # Apply the custom lookup table to all three RGB channels
    return img.point(lut * 3)

#Manual
def process_manual_edits(
    img: Image.Image, 
    saturation_factor: float, 
    shadows_amount: float, 
    brightness_factor: float, 
    sharpness_factor: float
) -> Generator[Tuple[str, Image.Image], None, None]:

    current_img = img.copy()

    # Step 1: SATURATION
    current_img = adjust_saturation(current_img, saturation_factor)
    yield ("saturation", current_img)

    # Step 2: SHADOWS
    current_img = adjust_shadows(current_img, shadows_amount)
    yield ("shadows", current_img)

    # Step 3: BRIGHTNESS
    current_img = adjust_brightness(current_img, brightness_factor)
    yield ("brightness", current_img)

    # Step 4: SHARPNESS
    current_img = adjust_sharpness(current_img, sharpness_factor)
    yield ("sharpness", current_img)
