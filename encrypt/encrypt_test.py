import encrypt

MASK_IMAGE_PATH = "samples/images/high_res/mask_highres.png"
SECRET_IMAGE_PATH = "samples/images/high_res/secret_highres.png"
SECRET_CODE = 1

encrypted_array = encrypt.encrypt_frame(MASK_IMAGE_PATH,SECRET_IMAGE_PATH,"samples\output.png")
