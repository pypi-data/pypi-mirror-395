# Run this once to fix your file
with open("secure_hash.py", "r") as f:
    code = f.read()

# Replace all tabs with 4 spaces
code = code.replace("\t", "    ")

with open("secure_hash.py", "w") as f:
    f.write(code)
print("Tabs replaced with spaces ✅")
