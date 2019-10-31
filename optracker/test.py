from PIL import Image
from facerec.facerec import facerec

def run():
    print("run started")
    myFace = facerec()
    #myFace.findFaceinImg("C:\\Users\\ZeroBit\\OneDrive - Forsvarets høgskole\\09 - Kadettsamfundet\\01 - Bilder\\05 - Skytekurs og Øvelse Inf Strid\\test1.jpg")
    #myFace.findFaceinImg("C:\\Users\\ZeroBit\\OneDrive - Forsvarets høgskole\\09 - Kadettsamfundet\\01 - Bilder\\05 - Skytekurs og Øvelse Inf Strid\\test2.jpg")
    #myFace.findFaceinImg("C:\\Users\\ZeroBit\\OneDrive - Forsvarets høgskole\\09 - Kadettsamfundet\\01 - Bilder\\05 - Skytekurs og Øvelse Inf Strid\\test4.jpg")
    #myFace.findFaceinImgCNN("C:\\Users\\ZeroBit\\OneDrive - Forsvarets høgskole\\09 - Kadettsamfundet\\01 - Bilder\\05 - Skytekurs og Øvelse Inf Strid\\test4.jpg")
    face_locations, image = myFace.findFaceinImg("C:\\Local Work\\05 - Codes\\12 - Python\\05 - openSource Tracker v0.3\\optracker\\facerec\\source\\two_people.jpg")

    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()

if __name__ == '__main__':
    run()
