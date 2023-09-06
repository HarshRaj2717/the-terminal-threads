import numpy as np


def decrypt_frame(encrypted_image: np.ndarray, bitcount: int, key: str = "") -> np.ndarray:
    """
    Retrieve the hidden `secret_image` from `encrypted_image` and decrypt it using `key`

    Returns the decrypted `secret_image`
    """
    # TODO add a function for using the key also

    decrypted_image = encrypted_image.copy()

    decrypted_image = decrypted_image & int('1'*bitcount, 2)
    decrypted_image = decrypted_image << (8 - bitcount)

    return decrypted_image
