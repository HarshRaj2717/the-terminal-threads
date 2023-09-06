import cv2
import numpy as np
from PIL import Image


def distort_image(image: np.ndarray, key: str) -> np.ndarray:
    """
    TODO

    Helper function that distorts `image` based on provided `key`
    such that it can also be un-distorted by reversing the process with the same key only
    """
    return image


def encrypt_frame(mask_image: np.ndarray, secret_image: np.ndarray, bitcount: int, key: str = "") -> np.ndarray:
    """
    Encrypt the `secret_image` using `key` and hide it inside `mask_image`

    Returns the updated `mask_image`
    """
    # If the mask image is bigger than secret image, take a subsection (top-left corner)
    if mask_image.size > secret_image.size:
        (y, x) = secret_image.shape[:2]
        resized_secret_image = cv2.copyMakeBorder(
            secret_image,
            0,
            mask_image.shape[0] - y,
            0,
            mask_image.shape[1] - x,
            cv2.BORDER_CONSTANT,
            0,
        )
        Image.fromarray(resized_secret_image).save("samples\\resized.png")
    else:
        resized_secret_image = secret_image

    resized_secret_image = distort_image(resized_secret_image, key)

    secret_bits = resized_secret_image >> (8 - bitcount)
    mask_bits = (mask_image >> bitcount) << bitcount
    mask_image = mask_bits | secret_bits

    return mask_image
