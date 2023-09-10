import numpy as np
import cv2

def encrypt_frame(mask_array: np.ndarray, secret_array: np.ndarray,secret_code: int = 1, bitcount: int = 4) -> np.ndarray:
    """
    Encrypt the `secret_image` using `key` and hide it inside `mask_image`

    Returns the updated `mask_image`
    """

    # If the mask image is bigger than secret image, take a subsection (top-left corner)
    if mask_array.size > secret_array.size:
        secret_copy = secret_array.copy()
        secret_array = np.zeros(mask_array.shape, mask_array.dtype)
        secret_array[:secret_copy.shape[0], :secret_copy.shape[1], :] = secret_copy

    # distort the secret image using secret_code
    rng = np.random.default_rng(secret_code)
    shuffled_indices = rng.permutation(len(secret_array))
    secret_array = secret_array[shuffled_indices]

    # hide secret image inside mask image using bit manipulation
    secret_array = secret_array >> (8 - bitcount)
    mask_array = (mask_array >> bitcount) << bitcount
    mask_array = mask_array | secret_array

    return mask_array


