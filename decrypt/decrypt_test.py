import cv2
from PIL import Image
import decrypt

ENCRYPTED_IMAGE_PATH = "samples\\4bit.png"

encrypted_array = cv2.imread(ENCRYPTED_IMAGE_PATH, flags=1)
encrypted_array = cv2.cvtColor(encrypted_array, cv2.COLOR_BGR2RGB)

encrypted_array = decrypt.decrypt_frame(encrypted_array, 4,"")
decrypted_image = Image.fromarray(encrypted_array)
decrypted_image.save("samples\\4bit_decrypted.png")
