import numpy as np


def decrypt_frame(encrypted_image: np.ndarray, bitcount: int, secret_code: int = 1) -> np.ndarray:
    """
    Retrieve the hidden `secret_image` from `encrypted_image` and decrypt it using `key`

    Returns the decrypted `secret_image`
    """
    # unhide secret image from encrypted_image by reversing the hiding process
    encrypted_image = encrypted_image & int('1'*bitcount, 2)
    encrypted_image = encrypted_image << (8 - bitcount)

    # undistort the image using the secret_code
    rng = np.random.default_rng(secret_code)
    shuffled_indices = rng.permutation(len(encrypted_image))
    encrypted_image = encrypted_image[np.argsort(shuffled_indices)]

    return encrypted_image
