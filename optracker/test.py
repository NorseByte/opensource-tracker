from facerec.facerec import facerec

def run():
    print("run started")
    myFace = facerec()
    #myFace.findFaceinImg("C:\\Users\\ZeroBit\\OneDrive - Forsvarets høgskole\\09 - Kadettsamfundet\\01 - Bilder\\05 - Skytekurs og Øvelse Inf Strid\\test1.jpg")
    #myFace.findFaceinImg("C:\\Users\\ZeroBit\\OneDrive - Forsvarets høgskole\\09 - Kadettsamfundet\\01 - Bilder\\05 - Skytekurs og Øvelse Inf Strid\\test2.jpg")
    #myFace.findFaceinImg("C:\\Users\\ZeroBit\\OneDrive - Forsvarets høgskole\\09 - Kadettsamfundet\\01 - Bilder\\05 - Skytekurs og Øvelse Inf Strid\\test4.jpg")
    myFace.findFaceinImgCNN("C:\\Users\\ZeroBit\\OneDrive - Forsvarets høgskole\\09 - Kadettsamfundet\\01 - Bilder\\05 - Skytekurs og Øvelse Inf Strid\\test4.jpg")


if __name__ == '__main__':
    run()
