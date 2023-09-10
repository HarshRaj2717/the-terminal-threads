import os

import numpy as np
from PIL import Image

from decrypt.decrypt import decrypt_frame
from encrypt.encrypt import encrypt_frame


class ImageHandler:
    """
    ImageHandler handles hiding of one image in another with a secret key,

    and decoding a secret image from given image.
    """

    def __init__(self, secret_key) -> None:
        self.secret_key = secret_key

    def _check_file_exists(self, path) -> bool:
        if os.path.exists(path):
            return True
        else:
            return False

    def read_image(self, image_path) -> Image:
        """Reads image from given path and returns it"""
        if self._check_file_exists(image_path):
            image = Image.open(image_path)
            return image
        else:
            raise FileNotFoundError(f"Image at location {image_path} not found")

    def validate_images(self, secret_image, mask_image) -> None:
        """Validates images."""
        if secret_image.mode != mask_image.mode:
            raise Exception(f'Image modes does not match {secret_image.mode} {mask_image.mode}')
        else:
            # Image modes match, if there is an issue with sizes resize to minimum resolution
            secret_image_resol = secret_image.size
            mask_image_resol = mask_image.size

            if min(secret_image_resol, mask_image_resol) == mask_image_resol:
                secret_image = secret_image.resize(mask_image_resol)
            else:
                mask_image = mask_image.resize(secret_image_resol)
        return secret_image, mask_image

    def encode_image(self, secret_image_path, mask_image_path) -> None:
        """Encodes image"""
        secret_image = self.read_image(secret_image_path)
        mask_image = self.read_image(mask_image_path)

        secret_image, mask_image = self.validate_images(secret_image, mask_image)

        secret_image_ndarray = np.array(secret_image)
        mask_image_ndarray = np.array(mask_image)

        encoded_image_array = encrypt_frame(mask_image_ndarray, secret_image_ndarray, 4, self.secret_key)
        encoded_image = Image.fromarray(encoded_image_array)
        encoded_image.save("samples/output.png")

    def decode_image(self, image_path) -> None:
        """Decodes image"""
        image = self.read_image(image_path)
        image_as_array = np.array(image)

        decoded_image_array = decrypt_frame(image_as_array, 4, self.secret_key)
        decoded_image = Image.fromarray(decoded_image_array)
        decoded_image.save("samples/decoded_output.png")
