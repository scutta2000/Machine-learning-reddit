from PIL import Image, ImageOps
import os

# Target resolution = (2504, 1878)


def resize(im):
    w, h = im.size
    if w > h:
        scale = 2504 / w
        newH = round(h * scale)//2 * 2
        im = im.resize((2504, newH))
        return ImageOps.expand(im, (0, (1878 - newH)//2))
    else:  # h >= w
        scale = 1878 / im.size[1]
        newW = round(im.size[0] * scale)//2 * 2
        im = im.resize((newW, 1878))
        return ImageOps.expand(im, ((2504 - newW)//2, 0))


# ImageOps.expand(im, (200, 0)).show()
directory = "aww"

for fileName in os.listdir(directory):
    if fileName.endswith("jpeg") or fileName.endswith("png"):
        im = resize(Image.open(directory + "/" + fileName))
        im = im.convert("RGB")
        # im.save("resized_aww/" + ".".join(fileName.split(".")[:-1]) + ".jpeg")
        im.save("resized_aww/" + fileName, "JPEG")
        print("Saved", fileName)
