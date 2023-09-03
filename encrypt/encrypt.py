import numpy


def encrypt_frame(mask_image: numpy.ndarray, secret_image: numpy.ndarray, key: str = "") -> numpy.ndarray:
    """
    Encrypt the `secret_image` using `key` and hide it inside `mask_image`

    Returns the updated `mask_image`
    """
    ...
