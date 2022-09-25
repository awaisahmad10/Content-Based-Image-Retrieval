import numpy as np
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img


def concatenate(list):  # function to concatenate barcodes
    result = ''
    for element in list:
        result += str(element)
    return result


def hammingDist(str1, str2):  # function to calculate hamming distance
    i = 0
    count = 0
    while i < len(str1):
        if str1[i] != str2[i]:
            count += 1
        i += 1
    return count


# Barcode Generator
barcodes = []  # Array to hold barcodes
paths = []  # Array to hold path to images
pathList = Path("MNIST_DS").glob('**/*.jpg') #Defining path to data set


for path in pathList:

    path_in_str = str(path) # converting path to image to string
    paths.append(path_in_str) # saving paths to paths array
    arr = np.array(Image.open(path_in_str).convert('P')) #Creating array out of images

    # getting sums
    sum_row = np.sum(arr, axis=1).tolist()
    sum_col = np.sum(arr, axis=0).tolist()
    sum_dig1 = [np.trace(arr, offset=i) for i in range(-np.shape(arr)[0] + 2, np.shape(arr)[1] - 1)]
    sum_dig2 = [np.trace(np.fliplr(arr), offset=i) for i in range(-np.shape(np.fliplr(arr))[0] + 2, np.shape(np.fliplr(arr))[1] - 1)]  # order is slightly different than example

    # getting averages
    avg_row = np.average(sum_row).round(0)
    avg_col = np.average(sum_col).round(0)
    avg_dig1 = np.average(sum_dig1).round(0)
    avg_dig2 = np.average(sum_dig2).round(0)

    tempBarcode = []  # empty array for barcodes to be in before being concatenated
    for i in range(len(sum_row)):
        if sum_row[i] >= avg_row:
            tempBarcode.append(1)
        else:
            tempBarcode.append(0)

    for i in range(len(sum_dig1)):
        if sum_dig1[i] >= avg_dig1:
            tempBarcode.append(1)
        else:
            tempBarcode.append(0)

    for i in range(len(sum_col)):
        if sum_col[i] >= avg_col:
            tempBarcode.append(1)
        else:
            tempBarcode.append(0)

    for i in range(len(sum_dig2)):
        if sum_dig2[i] >= avg_dig2:
            tempBarcode.append(1)
        else:
            tempBarcode.append(0)

    barcodes.append(concatenate(tempBarcode))

# Search Algorithm
hits = 0  # number of hits
minVal = 128  # Current minimum hamming distance
minIndex = -1  # Current index of image with lowest distance
testHam = 128  # hamming distance between two barcodes


for barcodeSearchIndex in range(len(barcodes)): # Search algorithm
    for i in range(len(barcodes)): # Iterating thorough all the barcodes
        if i != barcodeSearchIndex: # Checking to see if barcode isn't reference barcode
            testHam = hammingDist(barcodes[barcodeSearchIndex], barcodes[i]) # Getting hamming distance
            if testHam < minVal: # Check to find minimum hamming distance
                minVal = testHam
                minIndex = i
    if paths[barcodeSearchIndex][9] == paths[minIndex][9]: # Check to see if its hit or not
        hits += 1
    # Outputting images
    image1 = img.imread(paths[barcodeSearchIndex])
    image2 = img.imread(paths[minIndex])
    plt.subplot(2, 2, 1)
    plt.title("Base Image")
    plt.imshow(image1)
    plt.subplot(2, 2, 2)
    plt.title("Found Image")
    plt.imshow(image2)
    plt.show()
    minVal = 128
    minIndex = -1


print("Accuracy:", hits) # output statements

