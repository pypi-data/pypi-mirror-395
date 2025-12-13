import pytest
from PIL import Image
from ossimg.core import (
    load_image,
    adjust_brightness,
    adjust_saturation,
    adjust_sharpness,
    adjust_shadows
)


@pytest.fixture
def sample_image():
    """Create a simple test image."""
    return Image.new('RGB', (100, 100), color='red')


def test_load_image(tmp_path):
    """Test image loading."""
    # Create a temporary test image
    test_img = Image.new('RGB', (50, 50), color='blue')
    test_path = tmp_path / "test.png"
    test_img.save(test_path)
    
    # Load and verify
    loaded = load_image(str(test_path))
    assert isinstance(loaded, Image.Image)
    assert loaded.size == (50, 50)


def test_adjust_brightness(sample_image):
    """Test brightness adjustment."""
    # Test brighter
    bright = adjust_brightness(sample_image, 1.5)
    assert isinstance(bright, Image.Image)
    assert bright.size == sample_image.size
    
    # Test darker
    dark = adjust_brightness(sample_image, 0.5)
    assert isinstance(dark, Image.Image)


def test_adjust_saturation(sample_image):
    """Test saturation adjustment."""
    # Test more saturated
    vibrant = adjust_saturation(sample_image, 1.5)
    assert isinstance(vibrant, Image.Image)
    
    # Test grayscale
    gray = adjust_saturation(sample_image, 0.0)
    assert isinstance(gray, Image.Image)


def test_adjust_sharpness(sample_image):
    """Test sharpness adjustment."""
    # Test sharper
    sharp = adjust_sharpness(sample_image, 2.0)
    assert isinstance(sharp, Image.Image)
    
    # Test blurrier
    soft = adjust_sharpness(sample_image, 0.5)
    assert isinstance(soft, Image.Image)


def test_adjust_shadows(sample_image):
    """Test shadow adjustment."""
    # Test lifted shadows
    lifted = adjust_shadows(sample_image, 0.5)
    assert isinstance(lifted, Image.Image)
    
    # Test crushed shadows
    crushed = adjust_shadows(sample_image, -0.3)
    assert isinstance(crushed, Image.Image)


def test_invalid_input_brightness():
    """Test error handling for brightness."""
    with pytest.raises(TypeError):
        adjust_brightness("not an image", 1.0)


def test_invalid_input_saturation():
    """Test error handling for saturation."""
    with pytest.raises(TypeError):
        adjust_saturation(None, 1.0)


def test_invalid_input_sharpness():
    """Test error handling for sharpness."""
    with pytest.raises(TypeError):
        adjust_sharpness(123, 1.0)


def test_invalid_input_shadows():
    """Test error handling for shadows."""
    with pytest.raises(TypeError):
        adjust_shadows([1, 2, 3], 0.5)


def test_process_manual_edits(sample_image):
    from ossimg.core import process_manual_edits
    
    results = list(process_manual_edits(sample_image, 1.2, 0.3, 1.1, 1.0))
    
    # Should yield 4 steps
    assert len(results) == 4
    
    assert results[0][0] == "saturation"
    assert results[1][0] == "shadows"
    assert results[2][0] == "brightness"
    assert results[3][0] == "sharpness"
    
    # All results should be images
    for name, img in results:
        assert isinstance(img, Image.Image)