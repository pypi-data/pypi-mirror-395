
import cv2
import numpy as np
# -----------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------

def multi_frequency_decompose(I_float):
    """Decompose image into Low, Mid, High frequency bands."""
    # I_float must be float type

    # Low Frequency (L): Large Gaussian Blur
    I_blur_L = cv2.GaussianBlur(I_float, (9, 9), 2)
    L = I_blur_L

    # Mid Frequency (M): Small Blur Residual
    I_blur_M = cv2.GaussianBlur(I_float, (3, 3), 1)
    M = I_float - I_blur_M    # mid-frequency residual

    # High Frequency (H): Large Blur Residual
    H = I_float - I_blur_L  # high-frequency

    return L, M, H


def local_contrast(I_float, k=4):
    """Compute local contrast using local variance."""
    # Ensure conversion to single-channel (grayscale) for local feature extraction
    # cv2.cvtColor expects 3-channel input to be 3D.
    # We must ensure the input is float before splitting or converting.
    if I_float.ndim == 3:
        gray = cv2.cvtColor(I_float.astype(np.float32), cv2.COLOR_BGR2GRAY)
    else:
        gray = I_float.astype(np.float32)

    mean = cv2.blur(gray, (k, k))
    contrast = np.abs(gray - mean)
    # Normalizing is essential as it is used in the alpha calculation
    return contrast / (contrast.max() + 1e-6)


def noise_estimation(I_float):
    """Estimate noise using Laplacian variance."""
    if I_float.ndim == 3:
        # Convert to float32 for cvtColor, then to grayscale, then cast to float64
        gray = cv2.cvtColor(I_float.astype(np.float32), cv2.COLOR_BGR2GRAY)
        gray = gray.astype(np.float64)
    else:
        # If already grayscale, just ensure it's float64
        gray = I_float.astype(np.float64)

    # Laplacian is highly sensitive to noise/fine details
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    noise = np.abs(lap)
    return noise / (noise.max() + 1e-6)


def edge_strength(I_float):
    """Compute edge strength using Sobel."""
    if I_float.ndim == 3:
        # Convert to float32 for cvtColor, then to grayscale, then cast to float64
        gray = cv2.cvtColor(I_float.astype(np.float32), cv2.COLOR_BGR2GRAY)
        gray = gray.astype(np.float64)
    else:
        # If already grayscale, just ensure it's float64
        gray = I_float.astype(np.float64)

    # Sobel for edge gradient
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    edge = np.sqrt(gx**2 + gy**2)
    return edge / (edge.max() + 1e-6)


def highpass(F):
    """High-pass filter."""
    # F is expected to be float
    return F - cv2.GaussianBlur(F, (3, 3), 1)


# -----------------------------------------------------------
# Simple Color & Tone Adjustment
# -----------------------------------------------------------

def color_tone_adjust(F):
    """Simple color correction for underwater images."""
    # Convert back to 8-bit for histogram equalization
    F_8bit = np.clip(F, 0, 255).astype(np.uint8)

    b, g, r = cv2.split(F_8bit)

    # Histogram equalization for ALL channels to boost contrast/color more uniformly
    b_eq = cv2.equalizeHist(b)
    g_eq = cv2.equalizeHist(g)
    r_eq = cv2.equalizeHist(r)

    F2 = cv2.merge([b_eq, g_eq, r_eq])

    # Bilateral filter for edge-preserving smoothing
    F2 = cv2.bilateralFilter(F2, 7, 50, 50)
    return F2


# -----------------------------------------------------------
# Main Sharpening Pipeline
# -----------------------------------------------------------

def adaptive_multi_frequency_sharpen(I, wL=0.3, wM=0.3, wH=0.4):

    # **Critical Fix 1: Convert to float for accurate arithmetic operations**
    # Original image I is assumed to be np.uint8 (0-255)
    I_float = I.astype(np.float64)

    # Step 1: Frequency Decomposition
    L, M, H = multi_frequency_decompose(I_float)

    # Step 2: Local contrast, noise, edge estimation
    # These return single-channel (grayscale) float arrays
    C = local_contrast(I_float)
    N = noise_estimation(I_float)
    E = edge_strength(I_float)

    # Adaptive modulation factor α
    # N must be non-zero (1e-6 added)
    alpha = (C * E) / (N + 1e-6)

    # Smooth alpha (original code used a small sigma, which is fine)
    alpha = cv2.GaussianBlur(alpha.astype(np.float32), (5, 5), 1)

    # **Critical Fix 2: Ensure alpha is the same size as the frequency bands**
    # Expand to 3 channels (Broadcasting rule)
    alpha3 = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)

    # Step 3: Adaptive Sharpening (L, M, H, alpha3 are all float/float64)
    # Increased coefficients for sharpening to make the image clearer
    L_s = L + 0.4 * alpha3 * highpass(L)
    M_s = M + 0.8 * alpha3 * highpass(M)
    H_s = H + 1.2 * alpha3 * highpass(H)

    # Step 4: Weighted Fusion
    F = wL * L_s + wM * M_s + wH * H_s

    # **Intermediate Step: Clipping and converting to uint8 is deferred**
    # Only the final color adjust function handles the conversion to uint8

    # Step 5: Color tone correction
    O = color_tone_adjust(F)

    return O


# -----------------------------------------------------------
# Example Usage
# -----------------------------------------------------------
def cheek():
    print('ok')
    
    
def image_sharpner(img):
    # 2. Process the image
    print("Processing image: ...")
    enhanced = adaptive_multi_frequency_sharpen(img)

    # 3. Save the result
    cv2.imwrite("enhanced_output.jpg", enhanced)
    print("Done! Enhanced image saved as 'enhanced_output.jpg'")