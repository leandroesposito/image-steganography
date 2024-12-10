# Image Steganography Utility

This project provides a command-line utility for storing and extracting text within images using steganography techniques. This steganography technique known as Least Significant Bit steganography (LSB) allows users to hide text within an image by modifying the least significant bits of the RGB values of the pixels. This method is effective because the changes are minimal and often imperceptible to the human eye. It allows users to embed secret messages into image files without significantly altering their appearance, making the stored information difficult to detect.

## Key Features

1. **Store Text in Image**: Users can store a text message within an image by specifying the number of least significant bits to modify. This allows for a balance between invisibility and the amount of data that can be stored.
   - **Example Command**: 
     ```bash
     py image_steganography.py --store --image-path "path-to-image" --text "text-to-store" --bits-to-change number-of-last-N-bits-to-use
     ```

2. **Extract Stored Text**: Users can retrieve the stored text from an image.
   - **Example Command**: 
     ```bash
     py image_steganography.py --extract --image-path "path-to-image"
     ```

3. **Store Text from a File**: The utility can also store the contents of a text file within an image, making it easy to conceal larger amounts of information.
   - **Example Command**: 
     ```bash
     py image_steganography.py --store --image-path "path-to-image" --txt-file "path-to-txt-file" --bits-to-change number-of-last-N-bits-to-use
     ```

4. **Text Obfuscation**: Before storing the text, users can obfuscate it using a Vigenère cipher with a user-provided key. This adds an extra layer of security, although it should not be relied upon for strong encryption. Obfuscation can be used with both `--text` or `--txt-file`.
   - **Example Command**: 
     ```bash
     py image_steganography.py --store --image-path "path-to-image" --text "text-to-store" --bits-to-change number-of-last-N-bits-to-use --obfuscate "key"
     ```

5. **Extract Obfuscated Text**: Users can extract the obfuscated text from the image by providing the same key used for obfuscation.
   - **Example Command**: 
     ```bash
     py image_steganography.py --extract --image-path "path-to-image" --desobfuscate "key"
     ```

6. **Text and Image Capacity Checks**: The utility includes commands to check the size of the text intended for storage and the capacity of the image based on different bit values. This helps users determine the feasibility of storing specific messages.
   - **Check Text Size**: 
     ```bash
     py image_steganography.py --check-text --text "text-to-store"
     ```
   - **Check Image Capacity**: 
     ```bash
     py image_steganography.py --check-img --image-path "path-to-image"
     ```
   - **Test Text and Image Compatibility**: 
     ```bash
     py image_steganography.py --test-text-img --text "text-to-store" --image-path "path-to-image"
     ```

This utility is a powerful tool for anyone interested in digital privacy, data management, or simply exploring the fascinating field of steganography.

## Requirements
  - Python 3.
  - OpenCV.
    - Install with the command `pip install opencv-python`.

## Samples
Here we will see how much an image is modified depending on the number of bits per pixel used to store the text.

## Sample Image
![Image of a landscape with a mountain](https://github.com/leandroesposito/image-steganography/blob/main/samples/0%20Original%20Tyler%20Lastovich%20Photo.jpeg)

This image, with dimensions 600 x 411 x 3, can store (600 pixels of width 411 pixels of height and 3 channels, red, green and blue):
   - 90.307 KB using the last 1 bit.
   - 180.615 KB using the last 2 bits.
   - 270.922 KB using the last 3 bits.
   - 361.229 KB using the last 4 bits.
   - 451.537 KB using the last 5 bits.
   - 541.844 KB using the last 6 bits.
   - 632.152 KB using the last 7 bits.
   - 722.459 KB using the last 8 bits.

### Using 1 Bit per Channel
This image stores 46.7 KB of information out of a capacity of 90.3 KB.

No visible change at this point.

![Sample](https://github.com/leandroesposito/image-steganography/blob/main/samples/1bit%2046.7%20KB%20of%20%2090.3%20KB.png)

### Using 2 Bits per Channel
This image stores 91.9 KB of information out of a capacity of 180.6 KB.

![Sample](https://github.com/leandroesposito/image-steganography/blob/main/samples/2bit%2091.9%20KB%20of%20180.6%20KB.png)

### Using 3 Bits per Channel
This image stores 140 KB of information out of a capacity of 270 KB.

Upon close inspection, we can distinguish a lower quality in the top part of the image.

![Sample](https://github.com/leandroesposito/image-steganography/blob/main/samples/3bit%20140%20KB%20of%20270%20KB.png)

### Using 4 Bits per Channel
This image stores 148 KB of information out of a capacity of 361 KB.

Using 4 bits, the output image has poor quality.

![Sample](https://github.com/leandroesposito/image-steganography/blob/main/samples/4bit%20148%20KB%20of%20361%20KB.png)

### Using 5 Bits per Channel
This image stores 247 KB of information out of a capacity of 451 KB.

At this point, the modifications are obvious.

![Sample](https://github.com/leandroesposito/image-steganography/blob/main/samples/5bit%20247%20KB%20of%20451%20KB.png)

### Using 6 Bits per Channel
This image stores 247 KB of information out of a capacity of 541 KB.

![Sample](https://github.com/leandroesposito/image-steganography/blob/main/samples/6bit%20247%20KB%20of%20541.8%20KB.png)

### Using 7 Bits per Channel
This image stores 331 KB of information out of a capacity of 632 KB.

We can barely distinguish what the image is about.

![Sample](https://github.com/leandroesposito/image-steganography/blob/main/samples/7bit%20331%20KB%20of%20632%20KB.png)

### Using 8 Bits per Channel
This image stores 331 KB of information out of a capacity of 722 KB.

The original image has disappeared completely.

![Sample](https://github.com/leandroesposito/image-steganography/blob/main/samples/8bit%20331%20KB%20of%20722%20KB.png)
