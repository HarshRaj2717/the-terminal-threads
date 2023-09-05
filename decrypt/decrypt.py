import numpy as np


def decrypt_frame(encrypted_image: np.ndarray, bitcount:int, key: str = "") -> np.ndarray:
    """
    Retrieve the hidden `secret_image` from `encrypted_image` and decrypt it using `key`

    Returns the decrypted `secret_image`
    """
    # TODO add a function for using the key also

    decrypted_image = encrypted_image.copy()

    for height in range(encrypted_image.shape[0]):
        for width in range(encrypted_image.shape[1]):
            for channel in range(encrypted_image.shape[2]):
                encrypted_bits = list(f"{encrypted_image[height][width][channel]:b}")
                decrypted_bits = ["0"] * 8
                while (len(encrypted_bits) < 8):
                    # making the length equal to 8 by adding zeros in starting
                    # so that we don't indexErrors
                    encrypted_bits = ['0'] + encrypted_bits
                # put 2 least signicant bits of encrypted pixels
                # at place of 2 most significant bits of decrypted pixels
                for i in range(bitcount):
                    decrypted_bits[i] = encrypted_bits[7-i]
                # updating the decrypted image
                decrypted_image[height][width][channel] = int("".join(decrypted_bits), 2)

    return decrypted_image
