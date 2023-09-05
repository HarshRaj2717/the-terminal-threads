import numpy as np


def distort_image(image: np.ndarray, key: str) -> np.ndarray:
    """
    TODO

    Helper function that distorts `image` based on provided `key`
    such that it can also be un-distorted by reversing the process with the same key only
    """
    return image


def encrypt_frame(mask_image: np.ndarray, secret_image: np.ndarray, key: str = "") -> np.ndarray:
    """
    Encrypt the `secret_image` using `key` and hide it inside `mask_image`

    Returns the updated `mask_image`
    """
    assert mask_image.size == secret_image.size, "size of mask & secret images don't match"
    assert mask_image.shape == secret_image.shape, "shape of mask & secret images don't match"

    secret_image = distort_image(secret_image, key)

    # TODO go through each pixel
    # and insert most significatnt bits of secret_image into least significant bits of mask_image
    for i in range(mask_image.shape[0]):
        for j in range(mask_image.shape[1]):
            for k in range(mask_image.shape[2]):
                secret_bits = list(f"{secret_image[i][j][k]:b}")
                mask_bits = list(f"{mask_image[i][j][k]:b}")
                while (len(secret_bits) < 8):
                    # making the length equal to 8 by adding zeros in starting
                    # so that we don't indexErrors
                    secret_bits = ['0'] + secret_bits
                while (len(mask_bits) < 8):
                    # making the length equal to 8 by adding zeros in starting
                    # so that we don't indexErrors
                    mask_bits = ['0'] + mask_bits
                mask_bits[0] = secret_bits[6]
                mask_bits[1] = secret_bits[7]

    return mask_image
