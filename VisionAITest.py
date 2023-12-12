import io
from google.cloud import vision

client=vision.ImageAnnotatorClient()
image_path='./assets/profile.png'
with io.open(image_path,'rb') as image_file:
    content=image_file.read()

image=vision.Image(content=content)
response=client.text_detection(image=image)

texts=response.text_annotations

for text in texts:
    print(text.description)