names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

print("Enumerate example:")
for index, name in enumerate(names, start=1):
    print(index, name)

print("\nZip example:")
for name, score in zip(names, scores):
    print(name, "scored", score)

print("\nCombined enumerate and zip:")
for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{i}. {name} -> {score}")