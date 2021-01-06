import boto3
import json
import cv2

# Document
documentName = "7_screen.png"

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())


img = cv2.imread('messi5.jpg',