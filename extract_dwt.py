import cv2
import numpy as np
import pywt

def bits_to_text(bits):
    """Convert binary string back to text."""
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def extract_watermark_dwt(watermarked_path, watermark_length, alpha=0.05):
    """
    Extract watermark from a color image using DWT.
    Args:
        watermarked_path: path to watermarked image
        watermark_length: length of watermark in characters
        alpha: same embedding strength used during embedding
    """
    img = cv2.imread(watermarked_path)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y_channel = np.float32(ycrcb[:, :, 0]) / 255.0

    # DWT decomposition
    coeffs = pywt.dwt2(y_channel, 'haar')
    LL, (LH, HL, HH) = coeffs

    flat_LH = LH.flatten()
    bits = ""
    for i in range(watermark_length * 8):
        if i >= len(flat_LH):
            break
        bits += '1' if flat_LH[i] > 0 else '0'

    return bits_to_text(bits)

