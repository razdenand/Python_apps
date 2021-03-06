import numpy as np
from math import *


def chose_sq(pattern, f, u, chi, p00, p01, p10, p11, threshold):
    if pattern == 0:
        pass
    elif pattern == 1:
        a1 = (p00 - threshold) / (p00 - p10)
        a4 = (p00 - threshold) / (p00 - p01)
        f += 0.5 * a1 * a4
        u += sqrt(a1 * a1 + a4 * a4)
        chi += 0.25
    elif pattern == 2:
        a1 = (p00 - threshold) / (p00 - p10)
        a2 = (p10 - threshold) / (p10 - p11)
        f += 0.5 * (1.0 - a1) * a2
        u += sqrt((1.0 - a1) * (1.0 - a1) + a2 * a2)
        chi += 0.25
    elif pattern == 3:
        a2 = (p10 - threshold) / (p10 - p11)
        a4 = (p00 - threshold) / (p00 - p01)
        f += a2 + 0.5 * (a4 - a2)
        u += sqrt(1.0 + (a4 - a2) * (a4 - a2))
    elif pattern == 4:
        a2 = (p10 - threshold) / (p10 - p11)
        a3 = (p01 - threshold) / (p01 - p11)
        f += 0.5 * (1.0 - a2) * (1.0 - a3)
        u += sqrt((1.0 - a2) * (1.0 - a2) + (1.0 - a3) * (1.0 - a3))
        chi += 0.25
    elif pattern == 5:
        a1 = (p00 - threshold) / (p00 - p10)
        a2 = (p10 - threshold) / (p10 - p11)
        a3 = (p01 - threshold) / (p01 - p11)
        a4 = (p00 - threshold) / (p00 - p01)
        f += 1.0 - 0.5 * (1.0 - a1) * a2 - 0.5 * a3 * (1.0 - a4)
        u += sqrt((1.0 - a1) * (1.0 - a1) + a2 * a2) + sqrt(a3 * a3 + (1.0 - a4) * (1.0 - a4))
        chi += 0.5
    elif pattern == 6:
        a1 = (p00 - threshold) / (p00 - p10)
        a3 = (p01 - threshold) / (p01 - p11)
        f += (1.0 - a3) + 0.5 * (a3 - a1)
        u += sqrt(1.0 + (a3 - a1) * (a3 - a1))
    elif pattern == 7:
        a3 = (p01 - threshold) / (p01 - p11)
        a4 = (p00 - threshold) / (p00 - p01)
        f += 1.0 - 0.5 * a3 * (1.0 - a4)
        u += sqrt(a3 * a3 + (1.0 - a4) * (1.0 - a4))
        chi += -0.25
    elif pattern == 8:
        a3 = (p01 - threshold) / (p01 - p11)
        a4 = (p00 - threshold) / (p00 - p01)
        f += 0.5 * a3 * (1.0 - a4)
        u += sqrt(a3 * a3 + (1.0 - a4) * (1.0 - a4))
        chi += 0.25
    elif pattern == 9:
        a1 = (p00 - threshold) / (p00 - p10)
        a3 = (p01 - threshold) / (p01 - p11)
        f += a1 + 0.5 * (a3 - a1)
        u += sqrt(1.0 + (a3 - a1) * (a3 - a1))
    elif pattern == 10:
        a1 = (p00 - threshold) / (p00 - p10)
        a2 = (p10 - threshold) / (p10 - p11)
        a3 = (p01 - threshold) / (p01 - p11)
        a4 = (p00 - threshold) / (p00 - p01)
        f += 1.0 - 0.5 * a1 * a4 + 0.5 * (1.0 - a2) * (1.0 - a3)
        u += sqrt(a1 * a1 + a4 * a4) + sqrt((1.0 - a2) * (1.0 - a2) + (1.0 - a3) * (1.0 - a3))
        chi += 0.5
    elif pattern == 11:
        a2 = (p10 - threshold) / (p10 - p11)
        a3 = (p01 - threshold) / (p01 - p11)
        f += 1.0 - 0.5 * (1.0 - a2) * (1.0 - a3)
        u += sqrt((1.0 - a2) * (1.0 - a2) + (1.0 - a3) * (1.0 - a3))
        chi += -0.25
    elif pattern == 12:
        a2 = (p10 - threshold) / (p10 - p11)
        a4 = (p00 - threshold) / (p00 - p01)
        f += (1.0 - a2) + 0.5 * (a2 - a4)
        u += sqrt(1.0 + (a2 - a4) * (a2 - a4))
    elif pattern == 13:
        a1 = (p00 - threshold) / (p00 - p10)
        a2 = (p10 - threshold) / (p10 - p11)
        f += 1.0 - 0.5 * (1.0 - a1) * a2
        u += sqrt((1.0 - a1) * (1.0 - a1) + a2 * a2)
        chi += -0.25
    elif pattern == 14:
        a1 = (p00 - threshold) / (p00 - p10)
        a4 = (p00 - threshold) / (p00 - p01)
        f += 1.0 - 0.5 * a1 * a4
        u += sqrt(a1 * a1 + a4 * a4)
        chi += -0.25
    elif pattern == 15:
        f += 1.0


def minkovsly2D(image, threshold):
    height = image.shape[0]
    width = image.shape[1]

    c_image = image.copy()

    f = 0.0
    u = 0.0
    chi = 0.0

    for y in range(height - 1):
        for x in range(width - 1):
            pattern = 0

            p00 = c_image[y, x]
            p01 = c_image[y + 1, x]
            p10 = c_image[y, x + 1]
            p11 = c_image[y + 1, x + 1]

            if p00 > threshold:
                pattern += 1
            if p10 > threshold:
                pattern += 2
            if p11 > threshold:
                pattern += 4
            if p01 > threshold:
                pattern += 8

            if pattern == 0:
                pass
            elif pattern == 1:
                a1 = (p00 - threshold) / (p00 - p10)
                a4 = (p00 - threshold) / (p00 - p01)
                f += 0.5 * a1 * a4
                u += sqrt(a1 * a1 + a4 * a4)
                chi += 0.25
            elif pattern == 2:
                a1 = (p00 - threshold) / (p00 - p10)
                a2 = (p10 - threshold) / (p10 - p11)
                f += 0.5 * (1.0 - a1) * a2
                u += sqrt((1.0 - a1) * (1.0 - a1) + a2 * a2)
                chi += 0.25
            elif pattern == 3:
                a2 = (p10 - threshold) / (p10 - p11)
                a4 = (p00 - threshold) / (p00 - p01)
                f += a2 + 0.5 * (a4 - a2)
                u += sqrt(1.0 + (a4 - a2) * (a4 - a2))
            elif pattern == 4:
                a2 = (p10 - threshold) / (p10 - p11)
                a3 = (p01 - threshold) / (p01 - p11)
                f += 0.5 * (1.0 - a2) * (1.0 - a3)
                u += sqrt((1.0 - a2) * (1.0 - a2) + (1.0 - a3) * (1.0 - a3))
                chi += 0.25
            elif pattern == 5:
                a1 = (p00 - threshold) / (p00 - p10)
                a2 = (p10 - threshold) / (p10 - p11)
                a3 = (p01 - threshold) / (p01 - p11)
                a4 = (p00 - threshold) / (p00 - p01)
                f += 1.0 - 0.5 * (1.0 - a1) * a2 - 0.5 * a3 * (1.0 - a4)
                u += sqrt((1.0 - a1) * (1.0 - a1) + a2 * a2) + sqrt(a3 * a3 + (1.0 - a4) * (1.0 - a4))
                chi += 0.5
            elif pattern == 6:
                a1 = (p00 - threshold) / (p00 - p10)
                a3 = (p01 - threshold) / (p01 - p11)
                f += (1.0 - a3) + 0.5 * (a3 - a1)
                u += sqrt(1.0 + (a3 - a1) * (a3 - a1))
            elif pattern == 7:
                a3 = (p01 - threshold) / (p01 - p11)
                a4 = (p00 - threshold) / (p00 - p01)
                f += 1.0 - 0.5 * a3 * (1.0 - a4)
                u += sqrt(a3 * a3 + (1.0 - a4) * (1.0 - a4))
                chi += -0.25
            elif pattern == 8:
                a3 = (p01 - threshold) / (p01 - p11)
                a4 = (p00 - threshold) / (p00 - p01)
                f += 0.5 * a3 * (1.0 - a4)
                u += sqrt(a3 * a3 + (1.0 - a4) * (1.0 - a4))
                chi += 0.25
            elif pattern == 9:
                a1 = (p00 - threshold) / (p00 - p10)
                a3 = (p01 - threshold) / (p01 - p11)
                f += a1 + 0.5 * (a3 - a1)
                u += sqrt(1.0 + (a3 - a1) * (a3 - a1))
            elif pattern == 10:
                a1 = (p00 - threshold) / (p00 - p10)
                a2 = (p10 - threshold) / (p10 - p11)
                a3 = (p01 - threshold) / (p01 - p11)
                a4 = (p00 - threshold) / (p00 - p01)
                f += 1.0 - 0.5 * a1 * a4 + 0.5 * (1.0 - a2) * (1.0 - a3)
                u += sqrt(a1 * a1 + a4 * a4) + sqrt((1.0 - a2) * (1.0 - a2) + (1.0 - a3) * (1.0 - a3))
                chi += 0.5
            elif pattern == 11:
                a2 = (p10 - threshold) / (p10 - p11)
                a3 = (p01 - threshold) / (p01 - p11)
                f += 1.0 - 0.5 * (1.0 - a2) * (1.0 - a3)
                u += sqrt((1.0 - a2) * (1.0 - a2) + (1.0 - a3) * (1.0 - a3))
                chi += -0.25
            elif pattern == 12:
                a2 = (p10 - threshold) / (p10 - p11)
                a4 = (p00 - threshold) / (p00 - p01)
                f += (1.0 - a2) + 0.5 * (a2 - a4)
                u += sqrt(1.0 + (a2 - a4) * (a2 - a4))
            elif pattern == 13:
                a1 = (p00 - threshold) / (p00 - p10)
                a2 = (p10 - threshold) / (p10 - p11)
                f += 1.0 - 0.5 * (1.0 - a1) * a2
                u += sqrt((1.0 - a1) * (1.0 - a1) + a2 * a2)
                chi += -0.25
            elif pattern == 14:
                a1 = (p00 - threshold) / (p00 - p10)
                a4 = (p00 - threshold) / (p00 - p01)
                f += 1.0 - 0.5 * a1 * a4
                u += sqrt(a1 * a1 + a4 * a4)
                chi += -0.25
            elif pattern == 15:
                f += 1.0

    return (f, u, chi)