
# when importing things that are not isntalled by default, you need to update requirements.txt
import cv2
import numpy as np




def computeOutline(picture, circleRadiusApproximate):
    """
    DO NOT MODIFY FUNCTION CALL
    This function finds best fit circle for the given picture
    Circle radius is given as input and is an indication of the size of the circle to be fitted.
    You should find and return correct diamter which is +/-3% of the given radius.
    The function should find the correct center of the circle and return it.
    """


    # Load grayscale image
    img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)


    radius = 10       # This is a placeholder value, replace with your computed radius
    center = (10, 10) # This is a placeholder value, replace with your computed center

    return radius, center
