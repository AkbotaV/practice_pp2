import os
os.makedirs("newdirs/project/data/sorted", exist_ok=True)

open("newdirs/file1.txt", "w").close()
open("newdirs/file2.txt", "w").close()

print(os.listdir("newdirs"))


for f in os.listdir("newdirs"):
  if f.endswith(".txt"):
    print(f)