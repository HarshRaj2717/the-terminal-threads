from image_handler.image_handler import ImageHandler
from vid_handler.frame_extraction import VideoMerger

# v = VideoMerger("samples/videos/base.mp4", "samples/videos/secret.mp4", 1)
# v.encode_video()
# v.decode_video()


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
[2] Encrypt/Decrypt Videos \
(Warning: This can take up a lot of RAM hence prefer running it for shorter videos if you have low RAM)
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
            if user_choice == '1':
                mask_video_path = input("\nEnter path to mask video \
(sample mask video path: \"samples/videos/mask.mp4\" ): ")
                secret_video_path = input("\nEnter path to secret video \
(sample mask video path: \"samples/videos/secret.mp4\" ): ")
                bitcount = int(input("Enter a bitcount \
(must be an integer in inclusive range [1, 8], suggested is 4): "))
                secret_code = int(input("Enter a secret code \
(must be an integer): "))

                video_handeler = VideoMerger(secret_code, bitcount)
                video_handeler.encode_video(mask_video_path, secret_video_path)

                print("\n\n\nYayy!! Your video have been encrypted and saved to \"samples/output.avi\"")
                _ = input("Press enter to continue...")
                print("\n\n\n")

            elif user_choice == '2':
                video_path = input("\nEnter path to mask video \
(sample video path if you have encrypted any video before: \"samples/output.avi\" ): ")
                bitcount = int(input("Enter a bitcount \
(must be an integer same as the one used for encrypting for correct outputs): "))
                secret_code = int(input("Enter a secret code \
(must be an integer same as the one used for encrypting for correct outputs): "))

                video_handeler = VideoMerger(secret_code, bitcount)
                video_handeler.decode_video(video_path)

                print("\n\n\nYayy!! Your video have been decrypted and saved to \"samples/output_decrypted.avi\"")
                _ = input("Press enter to continue...")
                print("\n\n\n")


if __name__ == "__main__":
    main()
