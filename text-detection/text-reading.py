import cv2
import pytesseract
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mplImg
import productNamesFetcher
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from PIL import Image as PILImage



def makePredictions(imgFile, polygonsFile, dbFile):
    """
    Given an image, the polygons, and the database csv -
    return a list of (UPC, confidence) prediction tuples

    Usage: predictionsDuples = makePredictions('sampleImage.png', 'samplePolygons.txt', 'montrealUPCs.csv')
    """
    text = detectAndRecognizeText(imgFile, polygonsFile)
    return fuzzySearch(text, dbFile)


def detectAndRecognizeText(imgFile, polygonsFile):

    """
    Given an image and its corresponding text-bounding-boxes (from EAST) -
    return the raw text that is read

    Note: automatically parses out punctuation and numerals because of poor
    OCR detection quality
    """
    image = cv2.imread(imgFile)
    height, width = image.shape[:2]
    readText = []
    with open(polygonsFile, 'r') as polygons: #TODO CHANGE THIS LINE
        for numString in polygons:

            numArray = list(map(lambda x: int(x), numString.split(',')))
            xVals = []
            yVals = []
            for i in range(4):
                xVals.append(numArray[i*2])
                yVals.append(numArray[i*2+1])
            xMin = max(min(xVals),0)
            yMin = max(min(yVals),0)
            xMax = min(max(xVals),width)
            yMax = min(max(yVals),height)
            crop = image[yMin:yMax, xMin:xMax]
            # uncomment the lines below to display the cropped polygons
            #plt.imshow(crop)
            #plt.show(block=False)
            #input()
            # plt.close()
            read = recognizeText(crop).strip('')
            read = re.sub(r'[^a-zA-z]+','',read)
            if(len(read)>3):
             readText.append(read)

        return " ".join(readText)


def recognizeText(image):
    """
    Takes cv2 imread object and returns any present text as a single string
    """
    #create temp file for tesseract ocr
    filename = "{}.png".format(os.getpid())
    mplImg.imsave(filename, image)
    # Text holds the characters read
    text = pytesseract.image_to_string(PILImage.open(filename))
    # Delete previously made temporary file
    os.remove(filename)
    return text


def fuzzySearch(text, dbFile):
    """
    Takes in a string of text and fuzzy searches through it to to find corresponding matches in the database
    return a list of (UPC, confidence) prediction duples
    """

    products = productNamesFetcher.fetchNames(dbFile)

    namesToUPC = {name: UPC for (UPC, name) in products}
    guesses = process.extract(text, namesToUPC.keys() , scorer = fuzz.partial_ratio)
    #uncomment below to see the (productName, confidence) duples instead of (UPC, confidence) duples
    #print(guesses)

    return list(map(lambda x: (namesToUPC[x[0]], x[1]), guesses))
