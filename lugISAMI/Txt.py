import os.path
filename="ISAMI_FINAL.py"
file_exists = os.path.isfile(filename)

if file_exists:
    pass
else:
    f = open("ISAMI_FINAL.py", "w")
    f.write("Created file")