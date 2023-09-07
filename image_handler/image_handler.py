import os
from PIL import Image
import numpy as np

from decrypt.decrypt import decrypt_frame
from encrypt.encrypt import encrypt_frame

class ImageHandler:
    """ImageHandler handles hiding of one image in another with a secret key, and decoding a secret image from given image."""
    def __init__(self, secret_key) -> None:
        self.secret_key = secret_key
    
    def _check_file_exists(self, path) -> bool:
        if os.path.exists(path):
            return True
        else:
            return False

    def read_image(self, image_path) -> Image:
        if self._check_file_exists(image_path):
            image = Image.open(image_path)
            return image
        else:
            raise FileNotFoundError(f"Image at location {image_path} not found")
    
    def validate_images(self, base_image, mask_image) -> None:
        if base_image.mode != mask_image.mode:
            raise Exception(f'Image modes does not match {base_image.mode} {mask_image.mode}')
        else:
            # Image modes match, if there is an issue with sizes resize to minimum resolution
            base_image_resol = base_image.size
            mask_image_resol = mask_image.size

            if min(base_image_resol, mask_image_resol) == mask_image_resol:
                base_image = base_image.resize(mask_image_resol)
            else:
                mask_image = mask_image.resize(base_image_resol)        
        return base_image, mask_image
    
    def encode_image(self, base_image_path, mask_image_path) -> None:
        base_image = self.read_image(base_image_path)
        mask_image = self.read_image(mask_image_path)

        base_image, mask_image = self.validate_images(base_image, mask_image)
        
        base_image_ndarray = np.array(base_image)
        mask_image_ndarray = np.array(mask_image)
        
        encoded_image_array = encrypt_frame(base_image_ndarray, mask_image_ndarray, 3, self.secret_key)
        encoded_image = Image.fromarray(encoded_image_array)
        encoded_image.save("samples/output.png") 


    def decode_image(self, image_path) -> None:
        image = self.read_image(image_path)
        image_as_array = np.array(image)

        decoded_image_array = decrypt_frame(image_as_array, 3, self.secret_key)
        decoded_image = Image.fromarray(decoded_image_array)
        decoded_image.save("samples/decoded_output.png")
        
