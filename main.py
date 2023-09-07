from image_handler.image_handler import ImageHandler
from vid_handler.frame_extraction import VideoMerger

v = VideoMerger("samples/videos/base.mp4", "samples/videos/secret.mp4", 1)
v.encode_video()
v.decode_video()

im = ImageHandler(2)
im.encode_image("samples/images/high_res/secret_highres.png", "samples/images/high_res/secret_yn.png")
im.decode_image("samples/images/high_res/secret_highres.png")
