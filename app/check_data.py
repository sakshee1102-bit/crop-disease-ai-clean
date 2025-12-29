import os

for split in ["train", "val", "test"]:
    path = f"dataset/{split}"
    classes = os.listdir(path)
    print(f"{split.upper()} classes:", len(classes))
