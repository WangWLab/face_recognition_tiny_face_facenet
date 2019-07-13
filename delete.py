import sys
import os

def delete(path):
    files = [os.path.join(path, item) for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]
    dirs = [os.path.join(path, item) for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
    for item in files:
        os.remove(item)
        print(item)
    for item in dirs:
        delete(item)
        os.rmdir(item)
        print(item)

if __name__ == '__main__':
    delete(sys.argv[1])