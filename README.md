# [TITLE]

## Purpose

The purpose of [TITLE] is to provide a relatively simple, fast yet secure encryption of images and videos using the process of [image steganography](https://en.wikipedia.org/wiki/Steganography#Digital_messages). Simply provide a **secret** image (most formats work, but .png is best supported due to being lossless), an accompanying **mask** image and a cryptographic key. The algorithm then uses bit manipulation to hide the secret image inside the mask image. The secret-containing image (usually referred to as a steg-image) is nearly identical to the original mask, and at higher resolutions, the differences are almost inperceptible to the naked eye. The software is also capable of encrypting videos, however (as warned) this does eat up quite a lot of RAM.

## Instructions

* Download the entire codebase
* Run `main.py`
* Prepare the 2 images
* Follow the command line prompts
* The output image will be stored as `output.png` or `output_decrypted.png`, depending on the operation

## Limitations (PLEASE READ)

TL:DR, this is a codejam projectt. Don't use it to hide your sensitive info. Stay safe online, kids.

* The software uses 2-bit LSB (Least Significant Bit) conversion in order to encrypt images, and the key is used to generate a random array sequence using numpy. This method is _not_ foolproof. [WHY?]
* As mentioned, this software supports various image and video filetypes. Here are is the complete list, ranked by the format the algorithm is best suited for:
  * Lossless Image Formats: .png, .bmp, .raw
  * Lossy Image Formats: .jpg/.jpeg
  * Video Formats: .mp4, .mov, .avi
*  Batch Image/Video Encryption is unsupported
*  Video sizes capped to ~ [FIND OUT]
*  Cryptographic key is strictly numeric

## Examples

[INSERT IMAGES]

