import zipfile
import hashlib
import argparse
parser = argparse.ArgumentParser()                                               
parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()
hash_md5 = hashlib.md5()

file = args.file
# zip file handler  
zip = zipfile.ZipFile(file)


# list available files in the container
try:
    root = zipfile.ZipFile(file, "r")
except:
    root = "."  
for name in root.namelist():
    i = name.find("md5")
    if i>0:
        lines = root.open(name).readlines()
        for line in lines:
            split = line.split()
            md5Hash = split[0].decode("utf-8") 
            checkFile = split[1].decode("utf-8")
            for fileToCheck in root.namelist():
                fileCount = fileToCheck.find(checkFile.replace('*', ''))
                if(fileCount > 0):
                    with root.open(fileToCheck, "r") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_md5.update(chunk)
                    checksum = hash_md5.hexdigest()
                    result = checksum == md5Hash
                    print(checkFile, result)
                
