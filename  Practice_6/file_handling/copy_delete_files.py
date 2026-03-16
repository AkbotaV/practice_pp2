import shutil
import os
shutil.copy("file_1.txt", "file_1_backup.txt")
os.remove("file_1_backup.txt")