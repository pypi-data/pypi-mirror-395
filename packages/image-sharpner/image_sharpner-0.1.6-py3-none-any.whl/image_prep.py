import cv2
import numpy as np

# -----------------------------------------------------------
# I. Utility Functions
# -----------------------------------------------------------

def multi_frequency_decompose_corrected(I_float):
    """
    Decompose image into Low (L), Mid (M), High (H) frequency bands
    such that L + M + H = I_float exactly. (Laplacian Pyramid style)
    """
    # Create Blurs
    blur_small = cv2.GaussianBlur(I_float, (3, 3), 1)
    blur_large = cv2.GaussianBlur(I_float, (9, 9), 2)

    # Define Bands
    H = I_float - blur_small    # High: Fine details (Original - Small Blur)
    M = blur_small - blur_large # Mid: Medium details (Small Blur - Large Blur)
    L = blur_large              # Low: Base structure (Large Blur)

    return L, M, H

def local_contrast(I_gray, k=3):
    """Compute local contrast (absolute difference from local mean)."""
    mean = cv2.blur(I_gray, (k, k))
    contrast = np.abs(I_gray - mean)
    return contrast

def noise_estimation(I_gray):
    """Estimate noise using smoothed Laplacian magnitude."""
    lap = cv2.Laplacian(I_gray, cv2.CV_64F)
    noise = np.abs(lap)
    # Smooth the noise map slightly
    noise = cv2.GaussianBlur(noise, (3,3), 1) 
    return noise

def edge_strength(I_gray):
    """Compute edge strength using Sobel magnitude."""
    gx = cv2.Sobel(I_gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(I_gray, cv2.CV_64F, 0, 1, ksize=3)
    edge = np.sqrt(gx**2 + gy**2)
    return edge

# -----------------------------------------------------------
# II. Advanced UIE Color Correction
# -----------------------------------------------------------

def color_tone_adjust_advanced(F):
    """
    Performs Red Channel Compensation, CLAHE for contrast, and Final White Balancing.
    """
    F_8bit = np.clip(F, 0, 255).astype(np.uint8)
    b, g, r = cv2.split(F_8bit)
    
    # 1. RED CHANNEL COMPENSATION
    # Boost R towards the average of G and B
    avg_g = np.mean(g)
    avg_b = np.mean(b)
    target_r_avg = (avg_g + avg_b) / 2
    gain_r = target_r_avg / (np.mean(r) + 1e-6)

    # Apply compensation with aggressive gain, but clip the gain maximum at 3.0
    r_compensated = np.clip(r.astype(np.float64) * min(gain_r * 1.5, 2.50), 0, 255).astype(np.uint8)
    F_compensated = cv2.merge((b, g, r_compensated))

    # 2. CLAHE on Luminance
    lab = cv2.cvtColor(F_compensated, cv2.COLOR_BGR2LAB)
    l, a, bb = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)

    lab_eq = cv2.merge((l_eq, a, bb))
    F_out = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

    # 3. Final White Balancing (Gray World Assumption)
    result_float = F_out.astype(np.float64)
    # Correct way to get the mean values from cv2.mean()
    avg_b_final, avg_g_final, avg_r_final, _ = cv2.mean(result_float)

    avg_max = max(avg_b_final, avg_g_final, avg_r_final)

    b_balanced = result_float[:, :, 0] * (avg_max / (avg_b_final + 1e-6))
    g_balanced = result_float[:, :, 1] * (avg_max / (avg_g_final + 1e-6))
    r_balanced = result_float[:, :, 2] * (avg_max / (avg_r_final + 1e-6))

    F_final = cv2.merge((b_balanced, g_balanced, r_balanced))
    F_final = np.clip(F_final, 0, 255).astype(np.uint8)
    F_final = cv2.bilateralFilter(F_final, 7, 50, 50)

    return np.clip(F_final, 0, 255).astype(np.uint8)

# -----------------------------------------------------------
# III. Main Adaptive Sharpening Pipeline
# -----------------------------------------------------------

def adaptive_multi_frequency_sharpen_advanced(I, wL=1.0, wM=0.5, wH=1.0):

    I_float = I.astype(np.float64)

    # 1. Frequency Decomposition
    L, M, H = multi_frequency_decompose_corrected(I_float)

    # 2. Grayscale Feature Extraction
    gray = cv2.cvtColor(I_float.astype(np.float32), cv2.COLOR_BGR2GRAY).astype(np.float64)
    C = local_contrast(gray)
    N = noise_estimation(gray)
    E = edge_strength(gray)

    # 3. Adaptive Alpha Calculation (Stable and Clipped)
    # alpha = (Contrast * Edge) / Noise
    alpha = (C * E) / (N + 1e-5)
    alpha = cv2.normalize(alpha, None, 0, 1.0, cv2.NORM_MINMAX)

    # **Critical Stability Fix**: Clip alpha to prevent noise amplification
    alpha = np.clip(alpha, 0.0, 0.8)
    alpha = cv2.GaussianBlur(alpha, (5, 5), 0)
    alpha3 = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)

    # 4. Frequency Sharpening Factors
    # Mid-frequency (M) gets the strongest adaptive boost for structure/texture
    sharp_factor_M = 1.0 + (2.5 * alpha3)
    # High-frequency (H) gets a mild boost to limit noise
    sharp_factor_H = 1.0 + (0.5 * alpha3)

    L_s = L
    M_s = M * sharp_factor_M
    H_s = H * sharp_factor_H

    # 5. Weighted Fusion
    F = (wL * L_s) + (wM * M_s) + (wH * H_s)
    F = np.clip(F, 0, 255).astype(np.uint8)

    # 6. Post-processing Advanced UIE Color Correction
    O = color_tone_adjust_advanced(F)

    return O

# -----------------------------------------------------------
# IV. Execution
# -----------------------------------------------------------
    
    
def image_sharpner(x):
    # 2. Process the image
    print("Processing image: ...")
    img = cv2.imread(f"'{x}'") 
    enhanced = adaptive_multi_frequency_sharpen_advanced(img)

    # 3. Save the result
    cv2.imwrite(f"enhanced_{x}", enhanced)
    print("Done! Enhanced image saved as 'enhanced_output.jpg'")