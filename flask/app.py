from flask import Flask
from sys import argv

app = Flask(__name__)

@app.route("/")
def home():
    file = open(argv[1])
    page = ''
    for l in file:
        page += l

    return page
    
if __name__ == "__main__":
    app.run(debug=True)
