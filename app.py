from flask import Flask
from sys import argv
import json
import ruamel.yaml
from github import Github
from github import UnknownObjectException

path = argv[1]
url_parts = path.split('/')
username = url_parts[-2]
repo_name = url_parts[-1]


app = Flask(__name__)

@app.route("/v1/<filename>")
def home(filename):
    return get_config(filename)


def get_file_contents(user,repo,filename):
    try:
        github = Github()
        user = github.get_user(user)
        repository = user.get_repo(repo)
        file_contents = repository.get_contents(filename)
        return file_contents.decoded_content
    except UnknownObjectException:
        return None


def load_yaml(file_contents):
    return ruamel.yaml.round_trip_load(file_contents, preserve_quotes=True)

def get_config(filename):
    try :
        if filename.endswith(".yml"):
            file_contents = get_file_contents(username,repo_name,filename)
            if file_contents is None: return "Could not connect to repository: " + path + ", for file: "+ filename + "\n"
            obj = load_yaml(file_contents)
            return ruamel.yaml.round_trip_dump(obj) + "\n"

        elif filename.endswith(".json"):
            filename = filename.replace(".json",".yml")
            file_contents = get_file_contents(username,repo_name,filename)
            if file_contents is None: return "Could not connect to repository: " + path + ", for file: "+ filename + "\n"
            obj = load_yaml(file_contents)
            return json.dumps(obj) + "\n"

        else:
            return "format not supported \n"
    except ruamel.yaml.YAMLError as e:
        return "Parse error. could not parse file: " + filename + "\n"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
