#Import
from PIL import Image
from .core import adjust_brightness, adjust_saturation, adjust_sharpness, adjust_shadows

#Golden Hour Template
def apply_golden_hour(img: Image.Image) -> Image.Image:
    img = adjust_saturation(img, 1.30) 
    img = adjust_shadows(img, 0.30)
    img = adjust_brightness(img, 1.15)
    img = adjust_sharpness(img, 0.80)
    return img


#Gritty Contrast Template
def apply_gritty_contrast(img: Image.Image) -> Image.Image:
    img = adjust_sharpness(img, 2.50)
    img = adjust_brightness(img, 0.90)
    img = adjust_shadows(img, -0.20)
    img = adjust_saturation(img, 0.80) 
    return img

#Pastel Matte Template
def apply_pastel_matte(img: Image.Image) -> Image.Image:
    img = adjust_saturation(img, 1.10)
    img = adjust_shadows(img, 0.70)
    img = adjust_brightness(img, 1.20)
    img = adjust_sharpness(img, 0.90)
    return img