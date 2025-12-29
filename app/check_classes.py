import os

train_classes = sorted(os.listdir("dataset/train"))
val_classes   = sorted(os.listdir("dataset/val"))
test_classes  = sorted(os.listdir("dataset/test"))

print("Train classes count:", len(train_classes))
print("Val classes count  :", len(val_classes))
print("Test classes count :", len(test_classes))

print("\nMissing in VAL :", set(train_classes) - set(val_classes))
print("Missing in TEST:", set(train_classes) - set(test_classes))
