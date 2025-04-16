from flask import Flask
from os import path, walk
from wsgi import app
import os

# create tmp folder if it doesn't exist
if not path.exists("tmp"):
    os.makedirs("tmp")

if os.name == "nt":
    extra_dirs = ["tmp", "static", "templates"]
else:
    extra_dirs = ["/tmp", "static", "templates"]
extra_files = extra_dirs[:]

for extra_dir in extra_dirs:
    for root, dirs, files in walk(extra_dir):
        for file in files:
            filename = path.join(root, file)
            extra_files.append(filename)

if __name__ == "__main__":
    app.run(debug=True, port=3000, extra_files=extra_files)
