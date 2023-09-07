import numpy as np


def encrypt_frame(mask_image: np.ndarray, secret_image: np.ndarray, bitcount: int, secret_code: int = 1) -> np.ndarray:
    """
    Encrypt the `secret_image` using `key` and hide it inside `mask_image`

    Returns the updated `mask_image`
    """
    # If the mask image is bigger than secret image, take a subsection (top-left corner)
    if mask_image.size > secret_image.size:
        secret_copy = secret_image.copy()
        secret_image = np.zeros(mask_image.shape, mask_image.dtype)
        secret_image[:secret_copy.shape[0], :secret_copy.shape[1], :] = secret_copy

    # distort the secret image using secret_code
    rng = np.random.default_rng(secret_code)
    shuffled_indices = rng.permutation(len(secret_image))
    secret_image = secret_image[shuffled_indices]

    # hide secret image inside mask image using bit manipulation
    secret_image = secret_image >> (8 - bitcount)
    mask_image = (mask_image >> bitcount) << bitcount
    mask_image = mask_image | secret_image

    return mask_image
