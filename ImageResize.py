from PIL import Image, ImageOps
import os


def resize(im, size):
    endW, endH = size

    w, h = im.size
    if w > h:
        scale = endW / w
        # //2 * 2 assures the end result is even witch is necessary to add the correct border
        newH = round(h * scale)//2 * 2
        im = im.resize((endW, newH))
        return ImageOps.expand(im, (0, (endH - newH)//2))
    else:  # h >= w
        scale = endH / h
        # //2 * 2 assures the end result is even witch is necessary to add the correct border
        newW = round(w * scale)//2 * 2
        im = im.resize((newW, endH))
        return ImageOps.expand(im, ((endW - newW)//2, 0))


# ImageOps.expand(im, (200, 0)).show()
directory = "aww"

for fileName in os.listdir(directory):
    if fileName.endswith("jpeg") or fileName.endswith("png"):
        im = resize(Image.open(directory + "/" + fileName), (160, 120))
        im = im.convert("RGB")
        # im.save("resized_aww/" + ".".join(fileName.split(".")[:-1]) + ".jpeg")
        im.save("resized_aww/" + fileName, "JPEG")
        print("Saved", fileName)
