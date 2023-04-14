# image-steganography
Hide text inside image modifying least n significant bits of its pixel's color channels values.

## Utilities

### Hide text in image.
Example

```
py image_steganography.py --store --image-path "<path-to-image>" --text "<text-to-store>" --bits-to-change <number-of-last-N-bits-to-use>
```
Note: using higher values for --bits-to-change will modify less pixels but it will be more noticeable. Using lower values will use more pixels but won't be as noticeable, 1 or 2 won't be noticeable at all.

### Extract hidden text from image.
Example

```
py image_steganography.py --extract --image-path "<path-to-image>"
```

### Hide text of a .txt file in the image.
Example 

```
py image_steganography.py --store --image-path <path-to-image> --txt-file "<path-to-txt-file>" --bits-to-change <number-of-last-N-bits-to-use>
```

### Obfuscate text with a key provided by the user before hiding in the image.
Using a Vigenère cipher implementation you can obfuscate the text with a string key before storing it in the image. When extracting you will have to provide the key or ciphered text will be printed to console. Don't use it as a safe encryption.

Example 

```
py image_steganography.py --store --image-path "<path-to-image>" --text "<text-to-store>" --bits-to-change <number-of-last-N-bits-to-use> --obfuscate "<key>"
```

### Extract obfuscated hidden text from image.
Example 

```
py image_steganography.py --extract --image-path "<path-to-image>" --desobfuscate "<key>"
```

### View size of text intended to hide.
Example 

```
py image_steganography.py --check-text --text "<text-to-store>"
```

### View capacity of image using different values of last n bits.
Example 

```
py image_steganography.py --check-img --image-path "<path-to-image>"
```

### Check if text fits inside image and get lowest value of last n bits to use.
Example 

```
py image_steganography.py --test-text-img --text "<text-to-store>" --image-path "<path-to-image>"
```
