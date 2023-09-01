# Single Image Encoding Part

- def swap_pixels(secret_image, pixel_number_1, pixel_number_2):

  - swap the (r,g,b) values of pixel_number_1 & pixel_number_2

- def scrammble_secret_image(secret_image, key):

  - if len(key) is odd:
    - `key += ' '` (single space character)
  - make pairs of two from the key, for eg: if `key = "ABCD"` then `pairs = [('A', 'B'), ('C', 'D')]`
  - convert character inside of the `pairs` into their ASCII values, for eg: if `pairs = [('A', 'B'), ('C', 'D')]` then `pairs_ascii = [(65, 66), (67, 68)]`
  - for pair in pairs_ascii:
    - `swap_pixels(secret_image, pair[0], pair[1])`

- def put_secret_image_into_mask_image(mask_image, secret_image, key = None):

  - use to pillow load both images
  - if (size of both images don't match):
    - resizing is important as since we will be mapping each pixel of the secret_image to mask_image
    - resize the images to match their dimensions
  - if key:
    - scrammble_secret_image(secret_image, key)
  - for every pixel of the mask_image:
    - replace the least signifact bits of (r,g,b) values with the most significant bits of (r,g,b) values of the secret_image (refer to https://youtu.be/bZ88gnHzwz8?si=isbafeywEA95fz5X)

---

# Main Video Encoding Part

## 1. User Input

- mask video
- secret video
- key

## 2. Separate out each frame from mask video & secret video

- TODO

## 3. Encode secret video's each frame onto each frame of mask video

- for frame_index in range(total_number_of_frames);
  `- put_secret_image_into_mask_image(mask_video_frames[frame_index], secret_video_frames[frame_index], key)`

## 4. Put all mask_video_frames back into a video

- TODO

## 5. Bring back original audio of mask_video

- (Audio of mask_video would have been lost during the frame extraction, need to bring it back)
- TODO (current resource: https://stackoverflow.com/questions/56973205/how-to-combine-the-video-and-audio-files-in-ffmpeg-python)

## 6. Add encoded audio from secret_video to mask_video

- read audio from secret_video into a some variable, say - `secret_audio`
- scramble the byte data of `secret_audio` with some similar technique like in `scrammble_secret_image` function used in [single image encoding part](#single-image-encoding-part)
- put the byte data of `secret_audio` after the EOF of mask_video (will have search up what the EOF charater of a .mp4 looks like, here's the same method but for .jpg files - https://youtu.be/r-7d3w5xerY?si=bguv9Ha98ncYORz7)

> Give the encoded mask_video back to user now

---

# Single Image Decoding Part

- TODO

---

# Main Video Decoding Part

- TODO
