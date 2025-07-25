import cv2
import numpy as np
import matplotlib.pyplot as plt

def computeOutline(picture, circleRadiusApproximate):
    """
    DO NOT MODIFY FUNCTION CALL
    This function finds best fit circle for the given picture
    Circle radius is given as input and is an indication of the size of the circle to be fitted.
    You should find and return correct diameter which is +/-3% of the given radius.
    The function should find the correct center of the circle and return it.
    """
    # Load grayscale image
    img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    img -= np.mean(img)
    h, w = img.shape

    # FFT
    fft = np.fft.rfft2(img)
    fy = np.fft.fftfreq(h)
    fx = np.fft.rfftfreq(w)
    FX, FY = np.meshgrid(fx, fy)
    radius_freq = np.sqrt(FX**2 + FY**2)

    # Cutoff frequency normalized: choose ~ circleRadiusApproximate pixels 
    # as frequency cutoff (this can be tuned)
    cutoff_norm = circleRadiusApproximate/20 / max(h, w)
    mask = radius_freq <= cutoff_norm
    fft_filtered = fft * mask
    img_filtered = np.fft.irfft2(fft_filtered)

    # Normalize for Hough
    img_uint8 = cv2.normalize(img_filtered, None, -127, 128, cv2.NORM_MINMAX).astype(np.uint8)

    # Hough Circle detection params
    min_r = int(circleRadiusApproximate * 0.97)
    max_r = int(circleRadiusApproximate * 1.03)

    circles = cv2.HoughCircles(
        img_uint8, cv2.HOUGH_GRADIENT, dp=1.2, minDist=1000,
        param1=50, param2=30, minRadius=min_r, maxRadius=max_r
    )
    
    if circles is not None:
        # Take the first detected circle
        x, y, r = np.round(circles[0][0]).astype(int)
        center = (x, y)
        radius = r
        for x, y, r in np.round(circles[0]).astype(int):
            cv2.circle(img_uint8, (x, y), r, (0, 255, 0), 2)   # Circle outline
            cv2.circle(img_uint8, (x, y), 2, (0, 0, 255), 3)   # Center point
    else:
        # No circle detected fallback to placeholders
        radius = int(circleRadiusApproximate)
        center = (w // 2, h // 2)



    # Show
    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    plt.title("Original (mean removed)")
    plt.imshow(img, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title(f"Filtered")
    plt.imshow(img_filtered, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title("Hough Circles")
    plt.imshow(img_uint8)
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return radius, center