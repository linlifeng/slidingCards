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


# @app.route("/generate_page", methods=['POST', 'GET'])
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


@app.route("/generate_book", methods=['POST'])
def generate_book(content_json=MOCK_BOOK):
    data = json.loads(content_json)
    #if request.form:
    #    data = request.form
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
    book = json.dumps(content_json)
    return generate_book(content_json=book)

@app.route("/bookInput")
def inputform():
    return render_template(
        "define_book.html",
        page1_input=render_template("define_single_page.html", page_id="page1"),
        page2_input = render_template("define_single_page.html", page_id="page2"),
        page3_input=render_template("define_single_page.html", page_id="page3"),
        page4_input=render_template("define_single_page.html", page_id="page4"),
        page5_input=render_template("define_single_page.html", page_id="page5"),
        page6_input=render_template("define_single_page.html", page_id="page6"),
        page7_input=render_template("define_single_page.html", page_id="page7"),
        page8_input=render_template("define_single_page.html", page_id="page8"),
        page9_input=render_template("define_single_page.html", page_id="page9"),
        page10_input=render_template("define_single_page.html", page_id="page10")
    )

@app.route("/test", methods=['POST'])
def test():
    #print("request")
    #print(request.form)
    data = request.form.to_dict(flat=False)
    #print(data)

    page1_title = data['page1pageTitle'][0]
    page1_text = data['page1pageText'][0]
    page1_url = data['page1imageURL'][0]
    page1_background = data['page1backgroundURL'][0]

    page2_title = data['page2pageTitle'][0]
    page2_text = data['page2pageText'][0]
    page2_url = data['page2imageURL'][0]


    page3_title = data['page3pageTitle'][0]
    page3_text = data['page3pageText'][0]
    page3_url = data['page3imageURL'][0]

    page4_title = data['page4pageTitle'][0]
    page4_text = data['page4pageText'][0]
    page4_url = data['page4imageURL'][0]

    page5_title = data['page5pageTitle'][0]
    page5_text = data['page5pageText'][0]
    page5_url = data['page5imageURL'][0]

    page6_title = data['page6pageTitle'][0]
    page6_text = data['page6pageText'][0]
    page6_url = data['page6imageURL'][0]

    page7_title = data['page7pageTitle'][0]
    page7_text = data['page7pageText'][0]
    page7_url = data['page7imageURL'][0]

    page8_title = data['page8pageTitle'][0]
    page8_text = data['page8pageText'][0]
    page8_url = data['page8imageURL'][0]

    page9_title = data['page9pageTitle'][0]
    page9_text = data['page9pageText'][0]
    page9_url = data['page9imageURL'][0]

    page10_title = data['page10pageTitle'][0]
    page10_text = data['page10pageText'][0]
    page10_url = data['page10imageURL'][0]

    cover = {}
    cover["pageBackground"] = page1_background
    cover["pageType"] = "cover"
    cover["pageLayer"] = "layer100"
    cover["pageTitle"] = page1_title
    cover["pageText"] = page1_text
    cover["pagePic"] = page1_url

    page2 = {}
    page2["pageType"] = "content"
    page2["pageLayer"] = "layer90"
    page2["pageTitle"] = page2_title
    page2["pageText"] = page2_text
    page2["pagePic"] = page2_url

    page3 = {}
    page3["pageType"] = "content"
    page3["pageLayer"] = "layer80"
    page3["pageTitle"] = page3_title
    page3["pageText"] = page3_text
    page3["pagePic"] = page3_url

    page4 = {}
    page4["pageType"] = "content"
    page4["pageLayer"] = "layer70"
    page4["pageTitle"] = page4_title
    page4["pageText"] = page4_text
    page4["pagePic"] = page4_url

    page5 = {}
    page5["pageType"] = "content"
    page5["pageLayer"] = "layer60"
    page5["pageTitle"] = page5_title
    page5["pageText"] = page5_text
    page5["pagePic"] = page5_url

    page6= {}
    page6["pageType"] = "content"
    page6["pageLayer"] = "layer50"
    page6["pageTitle"] = page6_title
    page6["pageText"] = page6_text
    page6["pagePic"] = page6_url

    page7= {}
    page7["pageType"] = "content"
    page7["pageLayer"] = "layer40"
    page7["pageTitle"] = page7_title
    page7["pageText"] = page7_text
    page7["pagePic"] = page7_url

    page8= {}
    page8["pageType"] = "content"
    page8["pageLayer"] = "layer30"
    page8["pageTitle"] = page8_title
    page8["pageText"] = page8_text
    page8["pagePic"] = page8_url

    page9= {}
    page9["pageType"] = "content"
    page9["pageLayer"] = "layer20"
    page9["pageTitle"] = page9_title
    page9["pageText"] = page9_text
    page9["pagePic"] = page9_url

    page10 = {}
    page10["pageType"] = "content"
    page10["pageLayer"] = "layer10"
    page10["pageTitle"] = page10_title
    page10["pageText"] = page10_text
    page10["pagePic"] = page10_url


    pages = {
        "page1": cover,
        "page2": page2,
        "page3": page3,
        "page4": page4,
        "page5": page5,
        "page6": page6,
        "page7": page7,
        "page8": page8,
        "page9": page9,
        "backcover": page10
     }

    book = {}
    book["Pages"] = pages
    book["Title"] = data['bookTitle'][0]

    book_json = json.dumps(book)

    print(type(book_json))
    return generate_book(content_json=book_json)


    # pages = []
    # for page_name in data['Pages']:
    #     page_html = generate_bookpage(page_data=data['Pages'][page_name])
    #     pages.append(page_html)
    # page_cnt = len(pages)
    # return render_template(
    #     "slidingPages.html",
    #     bookTitle=book_title,
    #     pageCnt=page_cnt,
    #     pages=pages
    # )



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
