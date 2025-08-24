import os
import shutil
import random

# Base folder = script ke same directory me dataset
base_dir = os.path.join(os.path.dirname(__file__), "dataset")
cat_dir = os.path.join(base_dir, "cat")
dog_dir = os.path.join(base_dir, "dog")

# Output folder
output_dir = os.path.join(base_dir, "split_dataset")
splits = ["train", "validation", "test"]

# Ratios (70/15/15)
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

def prepare_folders():
    for split in splits:
        for category in ["cats", "dogs"]:
            path = os.path.join(output_dir, split, category)
            os.makedirs(path, exist_ok=True)

def split_and_copy(category, src_dir):
    images = os.listdir(src_dir)
    random.shuffle(images)

    total = len(images)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    split_data = {
        "train": images[:train_end],
        "validation": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split, files in split_data.items():
        for file in files:
            src = os.path.join(src_dir, file)
            dst = os.path.join(output_dir, split, category, file)
            shutil.copy(src, dst)

if __name__ == "__main__":
    prepare_folders()
    split_and_copy("cats", cat_dir)
    split_and_copy("dogs", dog_dir)
    print("Dataset successfully split into train, validation, and test folders inside dataset/split_dataset/")
