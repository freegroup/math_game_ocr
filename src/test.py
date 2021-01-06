import boto3
import json

# Document
documentName = "7_screen.png"
documentName = "test2.png"

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
response = textract.detect_document_text(Document={'Bytes': imageBytes})

print(json.dumps(response, indent=4))

# Print detected text
for item in response["Blocks"]:
    if item["BlockType"] in ["LINE", "WORD"]:
        print(item["Text"])
