import cv2
from PIL import Image

from encrypt import encrypt

MASK_IMAGE_PATH = "samples/mask.png"
SECRET_IMAGE_PATH = "samples/secret.png"

mask_array = cv2.imread(MASK_IMAGE_PATH, flags=1)
mask_array = cv2.cvtColor(mask_array, cv2.COLOR_BGR2RGB)

secret_array = cv2.imread(SECRET_IMAGE_PATH, flags=1)
secret_array = cv2.cvtColor(secret_array, cv2.COLOR_BGR2RGB)


encrypted_array = encrypt.encrypt_frame(mask_array, secret_array, "")
encrypted_image = Image.fromarray(encrypted_array)
encrypted_image.save("samples/output.png")
