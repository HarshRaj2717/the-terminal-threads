from image_handler.image_handler import ImageHandler

# v = VideoMerger("samples/videos/base.mp4", "samples/videos/secret.mp4", 1)
# v.encode_video()
# v.decode_video()

# im = ImageHandler(2)
# im.encode_image("samples/images/high_res/secret_highres.png", "samples/images/high_res/mask_highres.png")
# im.decode_image("samples/output.png")


def take_user_choice(max_choices: int, msg: str) -> str:
    """Take user choice and keeping asking untill a valid choice is given by user"""
    available_choices = [str(i) for i in range(1, max_choices + 1)]

    print(f'\n{msg}')
    user_choice = input("Enter a number as your choice: ")
    while user_choice not in available_choices:
        print(f'\n{msg}')
        user_choice = input("Please enter a valid choice: ")

    return user_choice


def main():
    """Main funtion"""
    print("Welcome to the-terminal-thread's project !!\nLet us guide you through this...\n")
    script_running = True
    while script_running:
        user_choice = take_user_choice(3, '''What would you like to do now?

[1] Encrypt/Decrypt Images
[2] Encrypt/Decrypt Videos
[3] Quit!''')

        if user_choice == '3':
            break

        elif user_choice == '1':
            user_choice = take_user_choice(3, '''\nWhat would you like to do now?
[1] Encrypt Image
[2] Decrypt Image
[3] Go Back!''')
            if user_choice == '1':
                mask_image_path = input("\nEnter path to mask image \
(sample mask image path: \"samples/images/high_res/mask_highres.png\" ): ")
                secret_image_path = input("\nEnter path to secret image \
(sample mask image path: \"samples/images/high_res/secret_highres.png\" ): ")
                bitcount = int(input("Enter a bitcount \
(must be an integer in inclusive range [1, 8], suggested is 4): "))
                secret_code = int(input("Enter a secret code \
(must be an integer): "))

                im_handeler = ImageHandler(secret_code, bitcount)
                im_handeler.encode_image(secret_image_path, mask_image_path)

                print("\n\n\nYayy!! Your image have been encrypted and saved to \"samples/output.png\"")
                _ = input("Press enter to continue...")
                print("\n\n\n")

            elif user_choice == '2':
                image_path = input("\nEnter path to image for decoding \
(sample image path if you have encrypted any image before: \"samples/output.png\" ): ")
                bitcount = int(input("Enter a bitcount \
(must be an integer same as the one used for encrypting for correct outputs): "))
                secret_code = int(input("Enter a secret code \
(must be an integer same as the one used for encrypting for correct outputs): "))

                im_handeler = ImageHandler(secret_code, bitcount)
                im_handeler.decode_image(image_path)

                print("\n\n\nYayy!! Your image have been deencrypted and saved to \"samples/output_decrypted.png\"")
                _ = input("Press enter to continue...")
                print("\n\n\n")

        elif user_choice == '2':
            user_choice = take_user_choice(3, '''\nWhat would you like to do now?
[1] Encrypt Video
[2] Decrypt Video
[3] Go Back!''')
            # TODO


if __name__ == "__main__":
    main()
