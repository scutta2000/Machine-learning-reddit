import pickle


with open("images.pkl", "rb") as f:
    l = pickle.load(f)

print(l[0])
