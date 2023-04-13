# informacion:
# bits per char
# bits changed
# text length
#  #
import cv2 as cv
import os
from units import convert_bytes
import argparse
import obfuscator

def textToBinList(text:str) -> list:
    """
    return list of binary representation of chars
    """
    # convert every char to ascii code using ord then to binary and return the list
    return [bin(ord(char))[2:] for char in text]

def binListToText(bins:list) -> str:
    """
    return string representation of list of binary chars
    """
    # convert every binary string to int then to char and return the string
    return "".join([chr(int(c, base=2)) for c in bins])

def writeTextToImage(text:str, imgPath:str, bitsToChange:int) -> list:
    """
        {text} text to store in the image
        {imgPath} path of the image to store the text
        {bitsToChange} number of last n bits to change in each pixel channel

        return {numpy.ndarray} an image with the text stored
    """
    # add the length of the text before the text to later use in extraction
    textToStore = f"{len(text)}\n{text}"

    # convert the string to a list of binary representation of its characters
    charBins = textToBinList(textToStore)

    # get the length of the binary representation of the character with highest ascii code
    bitsPerChar = len(max(charBins, key=len))

    # create the binary string to store in image
    # zfill add leading 0 to the binary string so all of them have the same length
    binText = "".join([b.zfill(bitsPerChar) for b in charBins])

    img = cv.imread(imgPath)
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    index = 0

    # store number of bits used per character and number of bits changed in every pixel channel on the last
    # pixel of the image to use in extraction
    img.itemset((height - 1, width - 1, channels - 1), bitsPerChar)
    img.itemset((height - 1, width - 1, channels - 2), bitsToChange)
    
    for y in range(height):
        for x in range(width):
            for channel in range(channels):
                # prevent writing on last pixel to maintain the value of bitsPerChar and bitsToChange
                if y >= height - 1 and x >= width - 1 and channel >= channels - 2:
                    break

                # get binary value of pixel channel
                # [2:] remove "bx" at the beginning of the string
                binChannel = bin(img.item(y, x, channel))[2:]
                # replace last n bits of pixel channel with index + n bits to change from binary text
                # ljust() is to add right zeroes to the last character for correct extraction
                newBinChannel = binChannel[:-bitsToChange] + binText[index:index + bitsToChange].ljust(bitsToChange, "0")

                # replace old pixel channel with modified
                img.itemset((y, x, channel), int(newBinChannel, base=2))

                index += bitsToChange
                
                if index >= len(binText):
                    return img
    
    raise Exception("Not enough space in the image with current config.")

def readTextFromImg(imgPath:str) -> str:
    img = cv.imread(imgPath)
    
    # convert numpy.ndarray to list to easy itteration
    flattenImg = img.flatten()
    
    # extract data from the last pixel
    bitsPerChar = int(flattenImg[-1])
    changedBits = int(flattenImg[-2])

    # convert every item of list to binary 
    # [:2] removes "0b" from beginning 
    # [-changedBits:] extract last changed bits from binary
    # zfill() add 0 in case if the value es a single 0 #
    binImg = "".join([bin(b)[2:][-changedBits:].zfill(changedBits) for b in flattenImg])

    # split the string using \n character to extract text length
    # maxplit is in case if the stored text hast line breaks #
    extractedText = getTextFromBin(binImg, bitsPerChar)

    # remove nonsense text after stored text
    # extractedText = textImg[:int(textLength)]

    return extractedText

def getTextFromBin(binary:str, bitsPerChar:int) -> str:
    """
        convert a binary string to text string
        {binary} binary string to convert
        {bitsPerChar} number of bits for every binaty char to split the string
    """
    # split one binary string into its characters
    charBins = [binary[i: i+bitsPerChar] for i in range(0, len(binary), bitsPerChar)]
    textLenght = ""
    
    # scan char by char until we find a "\n" to get the text length
    start = 0
    while chr(int(charBins[start], base=2)) != "\n":
        textLenght += chr(int(charBins[start], base=2))
        start += 1
    
    textLenght = int(textLenght)

    # convert each binary character between the first "\n" and text lenght then join them into a string 
    extractedText = "".join([chr(int(b, base=2)) for i, b in enumerate(charBins) if i > start and i <= start + textLenght])
    return extractedText

def showImgCapacity(imgPath:str) -> list:
    """
        print image capacity using differents last n bits

        return {list} with the capacity of item index + 1 bits changed in bits
    """
    img = cv.imread(imgPath)

    totalitems = img.shape[0] * img.shape[1] * img.shape[2]

    print(f"This image with dimensions {img.shape[0]} * {img.shape[1]} * {img.shape[2]} can store:")
    for i in range(1, 9):
        print(f"\t {convert_bytes((totalitems * i) / 8)} using last {i} bits.")

    # return 
    return [totalitems * i for i in range(1, 9)]

def showTextSize(text:str) -> int:
    """
        print text size

        return {int} text size in bits
    """
    binCharList = textToBinList(text)
    bitsPerChar = len(max(binCharList, key=len))

    totalSize = bitsPerChar * len(binCharList)
    
    print(f"The text size is: {convert_bytes(totalSize / 8)}")

    return totalSize

def testTextInImg(text:str, imgPath:str):
    """
        print text size and image capacities using different last n bits and the minimun recommended to use
    """
    textSize = showTextSize(text)
    imageCapacities = showImgCapacity(imgPath)    

    if(textSize > imageCapacities[-1]):
        print("Not enough space in the image to store the text")
    else:
        # get min index of imageCapacities bigger than image size
        print(f"Best config to store the text is to use last {min([i + 1 for i in range(len(imageCapacities)) if imageCapacities[i] > textSize])} bits")

def checkStoredText(text, imgPath):
    print("Checking new stored image")
    storedText = readTextFromImg(imgPath)

    if text == storedText:
        print("Text stored correctly")
    else:
        print("test Text:", text)
        print("read Text:", storedText)
        raise Exception("Stored text is NOT equal to input text")

def storeTextInImg(text:str, imgPath:str, bitsToChange:int):
    newImgPath = os.path.splitext(imgPath)[0] + "_new.png"
    
    print("Saving new image")
    cv.imwrite(newImgPath, writeTextToImage(text, imgPath, bitsToChange))

    checkStoredText(text, newImgPath)

def main(argv):
    store = argv.store
    extract = argv.extract

    checkText = argv.check_text
    checkImg = argv.check_img
    testTextAndImg = argv.test_text_img

    imgPath = argv.image_path
    text = argv.text
    txtFile = argv.txt_file
    bitsToChange = argv.bits_to_change

    obfuscateKey = argv.obfuscate
    desobfuscateKey = argv.desobfuscate
    

    if text is None and argv.txt_file is not None:
        with open(txtFile, encoding="utf-8") as f:
            text = f.read()
    
    if text is not None:
        if obfuscateKey:
            text = obfuscator.encode(text, obfuscateKey)

    if (store and imgPath and text and bitsToChange):    # store text in image
        storeTextInImg(text, imgPath, bitsToChange)
    elif (extract and imgPath):                        # extract text from image
        extractedText = readTextFromImg(imgPath)
        
        if desobfuscateKey:
            extractedText = obfuscator.decode(extractedText, desobfuscateKey)
        
        print(extractedText)
    elif (testTextAndImg and imgPath and text):        # test text in image
        testTextInImg(text, imgPath)
    elif (checkText and text):               # check text size
        showTextSize(text)
    elif (checkImg and imgPath):                          # check image capacity
        showImgCapacity(imgPath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Steganography tool to store text in an image modifying lasts bits from pixel channels in binary")

    parser.add_argument("--store", "-s", action="store_true", help="Store text in an image")
    parser.add_argument("--extract", "-e", action="store_true", help="Extract text from an image")
    
    parser.add_argument("--check-text", "-ct", action="store_true", help="Check text size")
    parser.add_argument("--check-img", "-ci", action="store_true", help="Check image capacity")
    parser.add_argument("--test-text-img", "-tti", action="store_true", help="Test if text fits inside image and recomend best configuration")
    
    parser.add_argument("--text", "-t", type=str, help="Text to store")
    parser.add_argument("--obfuscate", "-o", type=str, help="Obfuscate text using Vigenère cipher with provided key")
    parser.add_argument("--desobfuscate", "-d", type=str, help="Decode obfuscated text")
    parser.add_argument("--image-path", "-i", type=str, help="Image that will store the text")
    parser.add_argument("--txt-file", "-txt", type=str, help="Text file .txt with the text to store")
    parser.add_argument("--bits-to-change", "-b", type=int, help="Number of las N bits to change in pixel channels")
    # create image from text
    # obfuscate text before adding to image using a char to add its ascii code #    

    argv = parser.parse_args()

    s = argv.store
    e = argv.extract

    ct = argv.check_text
    ci = argv.check_img
    tti = argv.test_text_img

    i = argv.image_path
    t = argv.text
    txt = argv.txt_file
    b = argv.bits_to_change

    if (
        (s and i and (bool(t) ^ bool(txt)) and b) or    # store text in image
        (e and i) or                        # extract text from image
        (tti and i and (bool(t) ^ bool(txt))) or        # test text in image
        (ct and (bool(t) ^ bool(txt))) or               # check text size
        (ci and i)                          # check image capacity
        ):
        main(argv)

    else:
        parser.print_help()
        parser.error("MISSING ARGUMENTS")