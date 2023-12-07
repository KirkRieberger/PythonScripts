import os
import argparse
from progress.bar import Bar
from sys import exit as sys_ex

parser = argparse.ArgumentParser(
    description="Replaces the 'replacement' character with a new one.")
parser.add_argument('dir', type=str,
                    help="The directory of files to be renamed")
parser.add_argument('-d', '--delete', action='store_true',
                    help="Delete files suspected to have already been renamed")
# parser.add_argument()
args = parser.parse_args()

dir = os.fsencode(args.dir)
if (not os.path.isdir(dir)):
    print("Error: Directory specified does not exist!\n")
    sys_ex()

os.chdir(dir)

fileList = {}
for file in os.listdir(dir):  # file == bytes
    filename = os.fsdecode(file)  # String
    if filename.endswith(".sbp") or filename.endswith(".sbpcfg"):
        fileList.update({filename: file})

del(filename) # Debug: Remove filename from the list of variables

progBar = Bar("Renaming...", max=len(fileList))
for key in fileList.keys():
    newName = key.replace("�", "°")
    if newName != key:
        try:
            os.rename(fileList.get(key), newName)
        except FileExistsError:
            if args.delete:
                print(f"\nFile '{key}' already exists. Assuming already renamed. Deleting.")
                os.remove(fileList.get(key))
            else:
                print(f"\n[WinError 183] Cannot create a file when that file already exists: '{key}' -> '{newName}'!\nContinuing...")

    progBar.next()
