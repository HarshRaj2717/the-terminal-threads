from vid_handler.frame_extraction import VideoMerger

v = VideoMerger("samples/base.mp4", "samples/secret.mp4", 1)
v.encode_video()
# v.decode_video()
