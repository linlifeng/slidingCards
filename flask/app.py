from flask import Flask, request, render_template
import json
from sys import argv

app = Flask(__name__)

@app.route("/")
def home():
    file = open("../picturebooks/index.html", 'r')
    page = ''
    for l in file:
        page += l

    return page


@app.route("/generate_book", methods = ['POST', 'GET'])
def generate_book():
    mockData = {
        "Title":"testBookTitle",
        "TitlePic":"placeholder for picture url for title",
        "Pages":{
            "page1":{
                "pageTitle":"pageTitle",
                "pageText":"pageText",
                "pagePic":"placeholder for picture url"
            },
            "page2":{
                "pageTitle":"pageTitle",
                "pageText":"pageText",
                "pagePic":"placeholder for picture url"
            }
        }
	}
    if request.data:
        data = json.loads(request.data)
    else:
        data = mockData
    bookTitle = data['Title']
    coverPic = data['TitlePic']
    pageCnt = len(data['Pages'])
    return render_template(
        "slidingPages.html",
        bookTitle = bookTitle,
        pageCnt = pageCnt
    )


# @app.route("/generate_book", methods = ['GET'])
# def display_generated_book():
#     try:
#         page = generate_book()
#     except:
#         page = "error loading page"
#     return page



@app.route("/book_generator")
def book_input_page():
    file = open("../picturebooks/book_input.html", 'r')
    page = ''
    for l in file:
        page += l

    return page

@app.route("/book1")
def book1():
    file = open("../picturebooks/book1/book1.html", 'r')
    page = ''
    for l in file:
        page += l

    return page
if __name__ == "__main__":
    app.run(debug=True)
