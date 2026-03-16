with open("file_1.txt", "r") as f:
  print(f.read(12))
  f.seek(0)
  print(f.readline())
  f.seek(0)
  print(f.readlines())

print()
print()
with open("file_1.txt", "a") as f:
  f.write(". Append new text to the  end")
with open("file_1.txt") as f:
  print(f.read())