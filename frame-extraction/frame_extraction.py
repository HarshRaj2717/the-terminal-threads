import os

import cv2


class VideoExtractor(object):
    """Function of this class is to extract frames from a video"""

    def __init__(self, path) -> None:
        self.path = path
        self.frames = []

    def _check_file_exists(self) -> bool:
        if os.path.exists(self.path):
            return True
        else:
            return False

    def get_width(self) -> None:
        """Get the width of video"""
        self.width = int(self.videoObj.get(cv2.CAP_PROP_FRAME_WIDTH))

    def get_height(self) -> None:
        """Get the height of video"""
        self.height = int(self.videoObj.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frames_per_second(self) -> None:
        """Get the Frames per second of video"""
        self.fps = int(self.videoObj.get(cv2.CAP_PROP_FPS))

    def get_frame_count(self) -> None:
        """Get the frame count of video"""
        self.frame_count = int(self.videoObj.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_data(self) -> None:
        """Get the required data of video"""
        self.get_width()
        self.get_height()
        self.get_frame_count()
        self.get_frames_per_second()

    def extract_frames(self) -> None:
        """Extracts and saves frames of video so that they can be used for further processing."""
        if self._check_file_exists():
            self.videoObj = cv2.VideoCapture(self.path)

            self.get_data()

            frame_number = 0
            frame_extraction_successful = True

            while frame_number != self.frame_count and frame_extraction_successful:
                frame_extraction_successful, current_mask_frame = self.videoObj.read()

                if frame_extraction_successful:
                    self.frames.append(current_mask_frame)

                else:
                    print('Failed to read current frame')
                    raise Exception('Issue while reading a frame ' + str(frame_number))
                frame_number += 1
            self.videoObj.release()

        else:
            raise FileNotFoundError("File with name " + self.path + " is not found")


class VideoMerger(object):
    """Function of this class is to perform encoding / merging of secret video and mask video"""

    def __init__(self, base_video_path, secret_video_path, secret_key) -> None:
        self.base_video_obj = VideoExtractor(base_video_path)
        self.secret_video_obj = VideoExtractor(secret_video_path)
        self.secret_key = secret_key
        self.encoded_frames = []

    def perform_validation(self) -> bool:
        """Performs validation checks that video sizes, fps and frame counts match."""
        print("Extracing frames for base video")
        self.base_video_obj.extract_frames()
        print("Extracing frames for base video - DONE")

        print("Extracing frames for secret video")
        self.secret_video_obj.extract_frames()
        print("Extracing frames for secret video - DONE")
        # Now we have the required frames for both the videos.
        # before performing encoding, check if frame counts, width, height and stuff matches

        if self.base_video_obj.frame_count != self.secret_video_obj.frame_count \
                or self.base_video_obj.width != self.secret_video_obj.width \
                or self.base_video_obj.height != self.secret_video_obj.height \
                or self.base_video_obj.fps != self.secret_video_obj.fps:
            return False

        else:
            return True

    def encode_video(self):
        """Encodes videos."""
        self.perform_validation()
        current_frame = 0

        while self.base_video_obj.frame_count != current_frame:

            # call encoder here
            self.encoded_frames.append(self.base_video_obj.frames[current_frame])

            current_frame += 1

        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), self.base_video_obj.fps,
                              (self.base_video_obj.width, self.base_video_obj.height))

        print("Writing to output")
        for img in self.encoded_frames:
            out.write(img)
        out.release()
        print("Writing to output - DONE")


if __name__ == "__main__":

    video_merger = VideoMerger("sample.mp4", "sample.mp4", "")
    video_merger.encode_video()
