import cv2
from PIL import Image

import decrypt

ENCRYPTED_IMAGE_PATH = "samples/output.png"
SECRET_CODE = 1

encrypted_array = cv2.imread(ENCRYPTED_IMAGE_PATH, flags=1)
encrypted_array = cv2.cvtColor(encrypted_array, cv2.COLOR_BGR2RGB)

decrypted_array = decrypt.decrypt_frame(encrypted_array, 4, SECRET_CODE)
decrypted_image = Image.fromarray(decrypted_array)
decrypted_image.save("samples/output_decrypted.png")
