from flask import Flask, request, render_template
import json

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
        "pagePic": "./static/book1/page1.png"
    },
    "page2": {
        "pageType": "content",
        "pageLayer": "layer80",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page2.png"
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
        "pagePic": "./static/book1/page4.png"
    },
    "page5": {
        "pageType": "content",
        "pageLayer": "layer50",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page5.png"
    },
    "page6": {
        "pageType": "content",
        "pageLayer": "layer40",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page6.png"
    },
    "page7": {
        "pageType": "content",
        "pageLayer": "layer30",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page7.png"
    },
    "page8": {
        "pageType": "content",
        "pageLayer": "layer20",
        "pageTitle": "pageTitle",
        "pageText": "pageText",
        "pagePic": "./static/book1/page8.png"
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
    if 'pagePic' in data:
        pagePic = data['pagePic']
    else:
        pagePic = None
    pageText = data['pageText']
    pageLayer = data['pageLayer']
    pageType  = data['pageType']
    if 'pageBackground' in data:
        pageBackground = data['pageBackground']
    else:
        pageBackground = None
    return render_template(
        "page.html",
        pageTitle = pageTitle,
        pagePic = pagePic,
        pageText = pageText,
        pageLayer = pageLayer,
        pageType = pageType,
        pageBackground = pageBackground
    )

@app.route("/generate_book", methods = ['POST', 'GET'])
def generate_book(contentJson = MOCK_BOOK):
    data = contentJson
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




@app.route("/book_generator")
def book_input_page():
    file = open("../picturebooks/book_input.html", 'r')
    page = ''
    for l in file:
        page += l

    return page

@app.route("/book1")
def book1():
    contentFile = open('/Users/lifenglin/dev/sites/slidingCards/flask/static/book1/book1.json', 'r')
    contentJson = json.load(contentFile)
    book = {
        "Title": "book1",
        "TitlePic": "placeholder for picture url for title",
        "Pages": contentJson
    }
    return generate_book(contentJson=book)

@app.route("/book2")
def book2():
    contentFile = open('/Users/lifenglin/dev/sites/slidingCards/flask/static/book2/book2.json', 'r')
    contentJson = json.load(contentFile)
    book = {
        "Title": "book2",
        "TitlePic": "placeholder for picture url for title",
        "Pages": contentJson
    }
    return generate_book(contentJson=book)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
