from PIL import Image
import numpy as np
import pickle
import os


def rgb2BinaryHex(rgbColor):
    r, g, b = rgbColor

    hexColor = (r//16 * 16**5 +
                r % 16 * 16**4 +
                g//16 * 16**3 +
                g % 16 * 16**2 +
                b//16 * 16**1 +
                b % 16 * 16**0)
    return hexColor


# def binaryHex2rgb(h):
#     b = h % 16**2
#     h = h // 16**2

#     g = h % 16**2
#     h = h // 16**2

#     r = h % 16**2

#     return r, g, b


# im = [rgb2BinaryHex(i) for i in (Image.open(
#     "resized_aww/000_Meet_the_newest_member_of_the_family_Dutch.jpeg").getdata())]

# im = [binaryHex2rgb(px) for px in im]

# im2 = Image.new("RGB", (160, 120))
# im2.putdata(im)
# im2.show()

out = []
directory = "resized_aww"
files = os.listdir(directory)
for i, fileName in enumerate(files):
    if fileName.endswith("jpeg") or fileName.endswith("png"):
        im = [rgb2BinaryHex(i) for i in (
            Image.open(directory + "/" + fileName).getdata())]
        out.append(im)
        print("{.2f}%".format(i/len(files)*100))


with open("images.pkl", "wb") as f:
    pickle.dump(out, f)
