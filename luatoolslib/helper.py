import os

# read content from a file
def readFile(path):
    f = open(path, "r")
    content = f.read()
    f.close()
    return content

# write content to a file
def writeFile(path, content):
    f = open(path, "w+")
    f.write(content)
    f.close()

# check file extention
def checkFileExt(file,ext):
    ext1 = os.path.splitext(file)[1][1:]
    if ext1 == ext:
        return True
    else:
        return False

