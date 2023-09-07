import cv2

import encrypt

MASK_IMAGE_PATH = "samples/mask_highres.png"
SECRET_IMAGE_PATH = "samples/secret_highres.png"
SECRET_CODE = 1

mask_array = cv2.imread(MASK_IMAGE_PATH, flags=1)
secret_array = cv2.imread(SECRET_IMAGE_PATH, flags=1)

encrypted_array = encrypt.encrypt_frame(mask_array, secret_array, 4, SECRET_CODE)
cv2.imwrite("samples/output.png", encrypted_array)
