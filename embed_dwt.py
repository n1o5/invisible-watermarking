import cv2
import numpy as np
import pywt

def text_to_bits(text):
    """Convert text string to binary bits."""
    return ''.join(format(ord(c), '08b') for c in text)

def embed_watermark_dwt(image_path, watermark_text, output_path, alpha=0.05):
    """
    Embed a watermark into the Y channel of a color image using DWT.
    Args:
        image_path: path to original image
        watermark_text: string watermark
        output_path: path to save watermarked image
        alpha: watermark strength
    """
    # Load image and convert to YCrCb
    img = cv2.imread(image_path)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y_channel = np.float32(ycrcb[:, :, 0]) / 255.0

    # Convert watermark to bits
    watermark_text = "WM:" + watermark_text
    bits = text_to_bits(watermark_text)

    # DWT decomposition
    coeffs = pywt.dwt2(y_channel, 'haar')
    LL, (LH, HL, HH) = coeffs

    # Flatten LH and embed watermark bits
    flat_LH = LH.flatten()
    for i in range(min(len(bits), len(flat_LH))):
        bit = int(bits[i])
        flat_LH[i] += alpha * (2*bit - 1)  # slightly increase/decrease

    LH_emb = flat_LH.reshape(LH.shape)

    # Reconstruct Y channel
    y_emb = pywt.idwt2((LL, (LH_emb, HL, HH)), 'haar')
    y_emb = np.uint8(np.clip(y_emb * 255, 0, 255))

    # Replace Y channel and convert back to BGR
    ycrcb[:, :, 0] = y_emb
    watermarked = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    cv2.imwrite(output_path, watermarked)
    print(f"Watermarked image saved as {output_path}")

