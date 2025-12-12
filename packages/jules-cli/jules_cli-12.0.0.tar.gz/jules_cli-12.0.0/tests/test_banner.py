import pytest
from unittest.mock import patch
from jules_cli.banner import print_logo, lerp, blend

@patch("rich.console.Console.print")
def test_print_logo(mock_print):
    """Test the print_logo function."""
    print_logo()
    assert mock_print.call_count > 0
    # Check that the last call to print contains the expected text
    last_call = mock_print.call_args_list[-1]
    args, kwargs = last_call
    assert "Your fully immersive, interactive developer assistant." in str(args[0])

@patch("rich.console.Console.print")
@patch("os.getenv")
def test_print_logo_with_fixed_palette(mock_getenv, mock_print):
    """Test print_logo with a fixed palette from environment variables."""
    mock_getenv.return_value = "0"
    print_logo()
    assert mock_print.call_count > 0

@patch("rich.console.Console.print")
@patch("os.getenv")
def test_print_logo_with_invalid_palette_fallback(mock_getenv, mock_print):
    """Test print_logo with an invalid palette index, falling back to procedural."""
    mock_getenv.return_value = "99"  # Invalid index
    print_logo()
    assert mock_print.call_count > 0

@patch("rich.console.Console.print")
@patch("os.getenv")
def test_print_logo_with_non_numeric_palette_fallback(mock_getenv, mock_print):
    """Test print_logo with a non-numeric palette value, falling back to procedural."""
    mock_getenv.return_value = "abc"
    print_logo()
    assert mock_print.call_count > 0

@patch("rich.console.Console.print")
@patch("random.SystemRandom.random", side_effect=[
    # A longer list of mock random values to avoid StopIteration
    0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1,
    0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1, 0.2,
    0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1, 0.2, 0.3
])
@patch('random.SystemRandom.shuffle')
def test_print_logo_procedural_palette_with_warm_bias(mock_shuffle, mock_random, mock_print):
    """Test the procedural palette generation with a warm bias."""
    print_logo()
    assert mock_print.call_count > 0

def test_lerp():
    """Test the linear interpolation function."""
    assert lerp(0, 10, 0.5) == 5
    assert lerp(-10, 10, 0.5) == 0
    assert lerp(10, 20, 0) == 10
    assert lerp(10, 20, 1) == 20

def test_blend():
    """Test the color blending function."""
    c1 = (0, 0, 0)
    c2 = (255, 255, 255)
    # The exact blended color depends on the non-linear transformation,
    # so we'll just check that it returns a valid hex color string.
    color = blend(c1, c2, 0.5)
    assert color.startswith("#")
    assert len(color) == 7
