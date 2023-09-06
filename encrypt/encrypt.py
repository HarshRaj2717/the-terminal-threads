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


def encrypt_frame(
    mask_image: np.ndarray, secret_image: np.ndarray, bitcount: int, key: str = ""
) -> np.ndarray:
    """
    Encrypt the `secret_image` using `key` and hide it inside `mask_image`

    Returns the updated `mask_image`
    """
    # assert mask_image.size == secret_image.size, "size of mask & secret images don't match"

    # assert mask_image.shape == secret_image.shape, "shape of mask & secret images don't match"

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

    # TODO go through each pixel
    # and insert most significatnt bits of secret_image into least significant bits of mask_image

    # takes the nth most/least significant bits

    secret_bits = secret_image >> (8 - bitcount)
    mask_bits = (mask_image >> bitcount) << bitcount
    mask_image = mask_bits | secret_bits
    print(np.max(mask_image))
    # for height in range(resized_secret_image.shape[0]):
    #     for width in range(resized_secret_image.shape[1]):
    #         for channel in range(resized_secret_image.shape[2]):
    #             secret_bits = list(f"{resized_secret_image[height][width][channel]:b}")
    #             mask_bits = list(f"{mask_image[height][width][channel]:b}")

    #             while (len(secret_bits) < 8):
    #                 # making the length equal to 8 by adding zeros in starting
    #                 # so that we don't indexErrors
    #                 secret_bits = ['0'] + secret_bits
    #             while (len(mask_bits) < 8):
    #                 # making the length equal to 8 by adding zeros in starting
    #                 # so that we don't indexErrors
    #                 mask_bits = ['0'] + mask_bits
    #             # put 2 most signicant bits of secret pixels
    #             # at place of 2 least significant bits of mask pixels

    #             for i in range(bitcount):
    #                 mask_bits[7-i] = secret_bits[i]
    #             mask_image[height][width][channel] = int("".join(mask_bits), 2)

    return mask_image
