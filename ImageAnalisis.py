from PIL import Image
import os
directory = "resized_aww"
sizes = []
for i, fileName in enumerate(sorted(os.listdir(directory))):
    if fileName.endswith("jpeg") or fileName.endswith("png"):
        # sizes.append((Image.open(directory+"/"+fileName).size))
        print(fileName.split(".")[-1])


# print([i for i in enumerate(sizes) if i[1] != (2504, 1878)])
# # sizes.sort(key=lambda x: min(x[1][0], x[1][1]))
# sortedRatios = sorted([(i[1][0]/i[1][1])
#                        for i in sizes], key=(lambda x: abs(1 - x)))


# frequencies = {}
# for item in sizes:
#     if item in frequencies:
#         frequencies[item] += 1
#     else:
#         frequencies[item] = 1


# with open("sizeFrequency.csv", "w") as output:
#     for f in frequencies.items():
#         output.write(str(f[0]) + ";" + str(f[1]) + "\n")

# print(sum([i[0] / i[1] for i in sizes]) / len(sizes))
