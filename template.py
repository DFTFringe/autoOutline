
# when importing things that are not isntalled by default, you need to update requirements.txt
import cv2
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt



def computeOutline(picture, circleRadiusApproximate):
    """
    DO NOT MODIFY FUNCTION CALL
    This function finds best fit circle for the given picture
    Circle radius is given as input and is an indication of the size of the circle to be fitted.
    You should find and return correct diamter which is +/-3% of the given radius.
    The function should find the correct center of the circle and return it.
    """

    print(picture)

    # Load grayscale image
    img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)

    # Apply Sobel filter to detect edges
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=9)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=9)
    sobel = cv2.magnitude(sobelx, sobely)
    h, w = sobel.shape

    """
    ksize = 9
    # Compute variance around each pixel.
    img_float = img.astype(np.float64)
    local_mean = cv2.blur(img_float, ksize=(ksize, ksize))
    local_mean_of_squares = cv2.blur(img_float**2, ksize=(ksize, ksize))
    local_variance = local_mean_of_squares - local_mean**2
    print(sobel.dtype, local_variance.dtype)
    """

    """
    # Compute edge direction (angle) in degrees
    edge_direction = np.arctan2(sobely, sobelx) * 180 / np.pi

    # pad image to make it square
    if h > w:
        pad = ((0, 0), (0, h - w))
    elif w > h:
        pad = ((0, w - h), (0, 0))
    else:
        pad = ((0, 0), (0, 0))
    sobel_pad = np.pad(sobel, pad, mode='constant')
    # transpose image
    sobel_trans = sobel_pad.transpose()
    # try to find position by using picture and transposed picure phase correlation on amplitude of sobel filtered picture
    result = cv2.phaseCorrelate(sobel_pad, sobel_trans)
    print(result)

    sobelx_pad = np.pad(sobelx, pad, mode='constant')
    sobely_pad = np.pad(sobely, pad, mode='constant')
    edge_direction_pad = np.arctan2(sobely_pad, sobelx_pad)
    edge_direction_pad_t = np.arctan2(sobely_pad.transpose(), sobelx_pad.transpose())
    # try to find position by using picture and transposed picure phase correlation on direction of sobel filter.
    # This does not work because edge direction really depends on the fringes
    result2 = cv2.phaseCorrelate(edge_direction_pad, edge_direction_pad_t)
    print(result2)
    """

    # Generate a black image of size h x w with dtype float64
    whiteCircleOnBlack = np.zeros((h, w), dtype=np.float64)
    # Draw a white disk of radius circleRadiusApproximate in the center
    center_coordinates = (w // 2, h // 2)
    cv2.circle(whiteCircleOnBlack, center_coordinates, int(circleRadiusApproximate), 255, 1)
    result3 = cv2.phaseCorrelate(sobel, whiteCircleOnBlack)
    print(result3, w // 2, h//2, w // 2 - result3[0][0], h // 2 - result3[0][1])

    #result4 = cv2.phaseCorrelate(local_variance, whiteCircleOnBlack)
    """
    # do the phase correlation manually to be able to print output of IFFT
    # Compute 2D FFT of sobel and whiteCircleOnBlack images
    sobel_fft = np.fft.rfft2(sobel)
    whiteCircleOnBlack_fft = np.fft.rfft2(whiteCircleOnBlack)
    # comple conjugate (negative imaginary part)
    whiteCircleOnBlack_fft_conj = np.conj(whiteCircleOnBlack_fft)
    # Hadamard product (element-wise multiplication) of sobel_fft and whiteCircleOnBlack_fft_conj
    corssPowerSpectrum = sobel_fft * whiteCircleOnBlack_fft_conj / np.abs(sobel_fft * whiteCircleOnBlack_fft_conj)

    # Compute inverse FFT (IFFT) of the Hadamard product
    ifft_result = np.fft.irfft2(corssPowerSpectrum)
    """


    # Display original and filtered images using matplotlib
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(sobel, cmap='gray')
    circle = plt.Circle((w // 2 - result3[0][0], h // 2 - result3[0][1]), circleRadiusApproximate, color='red', fill=False, linewidth=1)
    plt.gca().add_patch(circle)
    plt.axis('off')

    plt.show()


    radius = circleRadiusApproximate       # This is a placeholder value, replace with your computed radius
    center = (w // 2 - result3[0][0], h // 2 - result3[0][1]) # This is a placeholder value, replace with your computed center

    return radius, center


import pathlib
import json
import time

if __name__ == '__main__':
    #picture = pathlib.Path("pictures_rr/vladimir_vladimir_139.jpg")
    #picture = pathlib.Path("pictures_other/calibre-casegrain 76_41-lissage-plein-coc-2tiers mot__DSC7174trait.JPG")
    picture = pathlib.Path("pictures_other/355 f35_141-la meme-sans poids__DSC6950trait.JPG")

    #open corresponding .oln file
    # Assuming the .old file has the same name as the picture but with a different extension
    oln_file = picture.with_suffix('.oln')

    #read oln file as json
    with open(oln_file, 'r') as file:
        data = json.load(file)
    # Extract center_x, center_y, radius_x, radius_y from the json data
    center_x = data['outside_outline']['center_x']
    center_y = data['outside_outline']['center_y']
    radius_x = data['outside_outline']['radius_x']

    circleRadiusApproximate = radius_x #* random.uniform(0.97, 1.03)  # Randomize radius by +/-3%

    # execute the code we want to test
    start_time = time.process_time()
    radius, center = computeOutline(picture, circleRadiusApproximate)
    elapsed_time = time.process_time() - start_time