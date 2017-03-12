from flask import Flask
from sys import argv
import subprocess
import os

path = argv[1]
git_dir = "data"
print path

app = Flask(__name__)

@app.route("/")
def home():
    git_clone = subprocess.Popen(
            ["git","clone", path, git_dir],
             stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    out, error = git_clone.communicate()

    os.chdir(git_dir)
    #retval = os.getcwd()
    out = ""
    for filename in os.listdir("."):
        if filename.endswith(".yml"):
            f = open(filename, 'r')
            out += "<h2> contents of file " + filename + "</h2>"
            out += "<ul>"
            for line in f.readlines():
                if line != "\n":
                    out +="<li>" + line + "</li>"
            out += "</ul>"
            f.close()

    return out






if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
