import numpy


def decrypt_frame(encrypted_image: numpy.ndarray, key: str = "") -> numpy.ndarray:
    """
    Retrieve the hidden `secret_image` from `encrypted_image` and decrypt it using `key`

    Returns the decrypted `secret_image`
    """

    # TODO add a function for using the key also
