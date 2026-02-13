from pix2text import Pix2Text

p2t = Pix2Text.from_config()
while(True):
    dir = input("imagepath: ")

    res = p2t.recognize(dir, resized_shape = 608)
    print(res)
