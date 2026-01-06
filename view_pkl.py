import pickle

file_path = "phishing_model.pkl"   # your pickle file name

with open(file_path, "rb") as f:
    data = pickle.load(f)

print("PKL File Loaded Successfully!")
print("\nContents:\n")
print(data)
