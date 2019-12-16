from flask import Flask, request, render_template
import json, os

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
    "Title": "testBookTitle",
    "TitlePic": "placeholder for picture url for title",
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


@app.route("/generate_page", methods=['POST', 'GET'])
def generate_bookpage(page_data=MOCK_PAGES):
    data = page_data
    page_title = data['pageTitle']
    if 'pagePic' in data:
        page_pic = data['pagePic']
    else:
        page_pic = None
    page_text = data['pageText']
    page_layer = data['pageLayer']
    page_type = data['pageType']
    if 'pageBackground' in data:
        page_background = data['pageBackground']
    else:
        page_background = None
    return render_template(
        "page.html",
        pageTitle=page_title,
        pagePic=page_pic,
        pageText=page_text,
        pageLayer=page_layer,
        pageType=page_type,
        pageBackground=page_background
    )


@app.route("/generate_book", methods=['POST', 'GET'])
def generate_book(content_json=MOCK_BOOK):
    data = content_json
    book_title = data['Title']
    pages = []
    for page_name in data['Pages']:
        page_html = generate_bookpage(page_data=data['Pages'][page_name])
        pages.append(page_html)
    page_cnt = len(pages)
    return render_template(
        "slidingPages.html",
        bookTitle=book_title,
        pageCnt=page_cnt,
        pages=pages
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
    json_path = os.path.join(app.root_path, 'static/book1/book1.json')
    content_file = open(json_path, 'r')
    content_json = json.load(content_file)
    book = {
        "Title": "book1",
        "TitlePic": "placeholder for picture url for title",
        "Pages": content_json
    }
    return generate_book(content_json=book)


@app.route("/book2")
def book2():
    json_path = os.path.join(app.root_path, 'static/book2/book2.json')
    content_file = open(json_path, 'r')
    content_json = json.load(content_file)
    book = {
        "Title": "book2",
        "TitlePic": "placeholder for picture url for title",
        "Pages": content_json
    }
    return generate_book(content_json=book)


@app.route("/book3")
def book3():
    json_path = os.path.join(app.root_path, 'static/book3/book3.json')
    content_file = open(json_path, 'r')
    content_json = json.load(content_file)
    book = {
        "Title": "book2",
        "TitlePic": "placeholder for picture url for title",
        "Pages": content_json
    }
    return generate_book(content_json=book)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
