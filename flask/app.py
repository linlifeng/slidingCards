from flask import Flask, request, render_template
import json
from sys import argv

# MOCK_PAGES = {
#     "page1": {
#         "pageTitle": "pageTitle",
#         "pageText": "pageText",
#         "pagePic": "placeholder for picture url"
#     },
#     "page2": {
#         "pageTitle": "pageTitle",
#         "pageText": "pageText",
#         "pagePic": "placeholder for picture url"
#     }
# }

MOCK_PAGES = {
    "cover": {
        "pageType": "cover",
        "pageLayer": "layer100",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "page1": {
        "pageType": "content",
        "pageLayer": "layer90",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "page2": {
        "pageType": "content",
        "pageLayer": "layer80",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "page3": {
        "pageType": "content",
        "pageLayer": "layer70",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "page4": {
        "pageType": "content",
        "pageLayer": "layer60",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "page5": {
        "pageType": "content",
        "pageLayer": "layer50",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "page6": {
        "pageType": "content",
        "pageLayer": "layer40",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "page7": {
        "pageType": "content",
        "pageLayer": "layer30",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "page8": {
        "pageType": "content",
        "pageLayer": "layer20",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
    "backCover": {
        "pageType": "backCover",
        "pageLayer": "layer10",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page3.png"
    },
}

MOCK_BOOK = {
    "Title":"testBookTitle",
    "TitlePic":"placeholder for picture url for title",
    "Pages": MOCK_PAGES
}

app = Flask(__name__)

@app.route("/")
def home():
    file = open("../picturebooks/index.html", 'r')
    page = ''
    for l in file:
        page += l

    return page


@app.route("/generate_page", methods = ['POST', 'GET'])
def generate_bookpage(pageData = MOCK_PAGES):
    data = pageData

    pageTitle = data['pageTitle']
    pagePic = data['pagePic']
    pageText = data['pageText']
    pageLayer = data['pageLayer']
    pageType  = data['pageType']
    return render_template(
        "page.html",
        pageTitle = pageTitle,
        pagePic = pagePic,
        pageText = pageText,
        pageLayer = pageLayer,
        pageType = pageType
    )

@app.route("/generate_book", methods = ['POST', 'GET'])
def generate_book():
    mockData = MOCK_BOOK
    if request.data:
        data = json.loads(request.data)
    else:
        data = mockData
    bookTitle = data['Title']
    coverPic  = data['TitlePic']
    pages = []
    for pageName in data['Pages']:
        #print(pageName)
        pageHtml = generate_bookpage(pageData = data['Pages'][pageName])
        pages.append(pageHtml)
    pageCnt   = len(pages)
    return render_template(
        "slidingPages.html",
        bookTitle = bookTitle,
        pageCnt   = pageCnt,
        pages     = pages
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
