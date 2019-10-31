from PIL import Image
from .api import face_recognition

class facerec():
    def __init__(self, Zero):
        self.zero = Zero
        
        self.zero.printText("+ Loading Face Recognition", True)
        self.face = face_recognition()

    def findFaceinImgCNN(self, img):
        print("Finding Face CNN")
        image = self.face.load_image_file(img)
        face_locations = self.face.face_locations(image, number_of_times_to_upsample=0, model="cnn")
        print("I found {} face(s) in this photograph.".format(len(face_locations)))

        for face_location in face_locations:
            # Print the location of each face in this image
            top, right, bottom, left = face_location
            print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

            # You can access the actual face itself like this:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.show()

    def findFaceinImg(self, img):
        print("Finding Face HOG")
        image = self.face.load_image_file(img)
        face_locations = self.face.face_locations(image)
        print("I found {} face(s) in this photograph.".format(len(face_locations)))

        for face_location in face_locations:
            # Print the location of each face in this image
            top, right, bottom, left = face_location
            print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

            # You can access the actual face itself like this:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.show()

    def readSource(self, file):
        print("Read source")
