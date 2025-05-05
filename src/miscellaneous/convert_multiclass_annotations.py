import os
from glob import glob

for folder in ["./train/labels", "./valid/labels"]:
    for filepath in glob(os.path.join(folder, "*.txt")):
        with open(filepath, 'r') as f:
            lines = f.readlines()

        with open(filepath, 'w') as f:
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 5:
                    parts[0] = '0'  # convert class id to 0
                    f.write(" ".join(parts) + "\n")

print("✅ All label files updated to class ID 0.")
