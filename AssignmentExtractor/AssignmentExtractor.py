import zipfile
import os

def main():
    file = input("Filename: ")
    os.chdir(os.path.dirname(file))
    cwd = os.getcwd()
    
    i = 0
    zip = zipfile.ZipFile(file)
    for file in zip.namelist():
        zip.extract(file, f"{cwd}\\tmp")
        os.chdir(os.fsencode(f"{cwd}\\tmp"))
        if i == 0: # zip File
            pass

        

if __name__ == "__main__":
    main()

   