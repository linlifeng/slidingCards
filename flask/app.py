from flask import Flask, request, render_template, redirect, url_for
import json
import os
import glob

# Global variables
BOOK_JSON_DIR = 'static/books/'

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

# end global variables

app = Flask(__name__)


@app.route("/books")
def list_books():
    book_jsons = glob.glob(os.path.join(app.root_path, BOOK_JSON_DIR) + '*.json')
    book_jsons.sort(key=os.path.getmtime, reverse=True)

    # print(book_jsons)
    page = ''
    for book in book_jsons:
        book_name = '.'.join(os.path.basename(book).split('.')[:-1])
        if book_name == 'tmp':
            continue
        book_content = json.load(open(book, 'r'))
        book_cover = book_content["Pages"]["page1"]["pageBackground"]
        page += render_template("book_thumbnail.html", book_name=book_name, book_cover=book_cover)
    add_button = '<div id=save_button><a href=\"/bookInput\"><button>create a new book</button></a></div>'

    return page + add_button


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
    book_title = data['Title']
    pages = []
    for page_name in data['Pages']:
        page_html = generate_bookpage(page_data=data['Pages'][page_name])
        pages.append(page_html)
    return render_template(
        "slidingPages.html",
        bookTitle=book_title,
        pages=pages
    )


@app.route("/preview_book", methods=['GET'])
def preview_book(content_json=MOCK_BOOK):
    data = json.loads(content_json)
    book_title = data['Title']
    pages = []
    for page_name in data['Pages']:
        page_html = generate_bookpage(page_data=data['Pages'][page_name])
        pages.append(page_html)

    rendered_book = render_template(
        "slidingPages.html",
        bookTitle=book_title,
        pages=pages
    )

    #save_button = "<div class=bookmark><button>save</button></div>"
    save_button = '<div id=save_button><a href=\"/save_book?book_name=%s\"><button>save</button></a></div>'%book_title
    return save_button + rendered_book


@app.route("/show_book/<book_name>", methods=['GET'])
def show_book(book_name="default"):
    # if request.args:
    #     book_name = request.args['book_name']
    book_path = BOOK_JSON_DIR + book_name + '.json'
    json_path = os.path.join(app.root_path, book_path)
    content_file = open(json_path, 'r')
    content_json = json.load(content_file)
    book = json.dumps(content_json)
    return generate_book(content_json=book)


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


@app.route("/book3")
def book3():
    json_path = os.path.join(app.root_path, 'static/book3/book3.json')
    content_file = open(json_path, 'r')
    content_json = json.load(content_file)
    book = json.dumps(content_json)
    return generate_book(content_json=book)


@app.route("/bookInput")
def input_form():
    return render_template(
        "define_book.html",
        page1_input=render_template("define_single_page.html", page_id="page1"),
        page2_input=render_template("define_single_page.html", page_id="page2"),
        page3_input=render_template("define_single_page.html", page_id="page3"),
        page4_input=render_template("define_single_page.html", page_id="page4"),
        page5_input=render_template("define_single_page.html", page_id="page5"),
        page6_input=render_template("define_single_page.html", page_id="page6"),
        page7_input=render_template("define_single_page.html", page_id="page7"),
        page8_input=render_template("define_single_page.html", page_id="page8"),
        page9_input=render_template("define_single_page.html", page_id="page9"),
        page10_input=render_template("define_single_page.html", page_id="page10")
    )


@app.route("/book_generator", methods=['POST'])
def generate_book_from_webform():
    data = request.form.to_dict(flat=False)

    book_title = data['bookTitle'][0]

    page1_title = data['page1pageTitle'][0]
    page1_text = data['page1pageText'][0]
    page1_url = data['page1imageURL'][0]
    page1_background = data['page1backgroundURL'][0]
    page1_type = data['page1pageType'][0]

    page2_title = data['page2pageTitle'][0]
    page2_text = data['page2pageText'][0]
    page2_url = data['page2imageURL'][0]
    page2_background = data['page2backgroundURL'][0]
    page2_type = data['page2pageType'][0]

    page3_title = data['page3pageTitle'][0]
    page3_text = data['page3pageText'][0]
    page3_url = data['page3imageURL'][0]
    page3_background = data['page3backgroundURL'][0]
    page3_type = data['page3pageType'][0]

    page4_title = data['page4pageTitle'][0]
    page4_text = data['page4pageText'][0]
    page4_url = data['page4imageURL'][0]
    page4_background = data['page4backgroundURL'][0]
    page4_type = data['page4pageType'][0]

    page5_title = data['page5pageTitle'][0]
    page5_text = data['page5pageText'][0]
    page5_url = data['page5imageURL'][0]
    page5_background = data['page5backgroundURL'][0]
    page5_type = data['page5pageType'][0]

    page6_title = data['page6pageTitle'][0]
    page6_text = data['page6pageText'][0]
    page6_url = data['page6imageURL'][0]
    page6_background = data['page6backgroundURL'][0]
    page6_type = data['page6pageType'][0]

    page7_title = data['page7pageTitle'][0]
    page7_text = data['page7pageText'][0]
    page7_url = data['page7imageURL'][0]
    page7_background = data['page7backgroundURL'][0]
    page7_type = data['page7pageType'][0]

    page8_title = data['page8pageTitle'][0]
    page8_text = data['page8pageText'][0]
    page8_url = data['page8imageURL'][0]
    page8_background = data['page8backgroundURL'][0]
    page8_type = data['page8pageType'][0]

    page9_title = data['page9pageTitle'][0]
    page9_text = data['page9pageText'][0]
    page9_url = data['page9imageURL'][0]
    page9_background = data['page9backgroundURL'][0]
    page9_type = data['page9pageType'][0]

    page10_title = data['page10pageTitle'][0]
    page10_text = data['page10pageText'][0]
    page10_url = data['page10imageURL'][0]
    page10_background = data['page10backgroundURL'][0]
    page10_type = data['page10pageType'][0]

    cover = dict()
    cover["pageBackground"] = page1_background
    cover["pageType"] = page1_type
    cover["pageLayer"] = "layer100"
    cover["pageTitle"] = page1_title
    cover["pageText"] = page1_text
    cover["pagePic"] = page1_url

    page2 = dict()
    page2["pageBackground"] = page2_background
    page2["pageType"] = page2_type
    page2["pageLayer"] = "layer90"
    page2["pageTitle"] = page2_title
    page2["pageText"] = page2_text
    page2["pagePic"] = page2_url

    page3 = dict()
    page3["pageBackground"] = page3_background
    page3["pageType"] = page3_type
    page3["pageLayer"] = "layer80"
    page3["pageTitle"] = page3_title
    page3["pageText"] = page3_text
    page3["pagePic"] = page3_url

    page4 = dict()
    page4["pageBackground"] = page4_background
    page4["pageType"] = page4_type
    page4["pageLayer"] = "layer70"
    page4["pageTitle"] = page4_title
    page4["pageText"] = page4_text
    page4["pagePic"] = page4_url

    page5 = dict()
    page5["pageBackground"] = page5_background
    page5["pageType"] = page5_type
    page5["pageLayer"] = "layer60"
    page5["pageTitle"] = page5_title
    page5["pageText"] = page5_text
    page5["pagePic"] = page5_url

    page6 = dict()
    page6["pageBackground"] = page6_background
    page6["pageType"] = page6_type
    page6["pageLayer"] = "layer50"
    page6["pageTitle"] = page6_title
    page6["pageText"] = page6_text
    page6["pagePic"] = page6_url

    page7 = dict()
    page7["pageBackground"] = page7_background
    page7["pageType"] = page7_type
    page7["pageLayer"] = "layer40"
    page7["pageTitle"] = page7_title
    page7["pageText"] = page7_text
    page7["pagePic"] = page7_url

    page8 = dict()
    page8["pageBackground"] = page8_background
    page8["pageType"] = page8_type
    page8["pageLayer"] = "layer30"
    page8["pageTitle"] = page8_title
    page8["pageText"] = page8_text
    page8["pagePic"] = page8_url

    page9 = dict()
    page9["pageBackground"] = page9_background
    page9["pageType"] = page9_type
    page9["pageLayer"] = "layer20"
    page9["pageTitle"] = page9_title
    page9["pageText"] = page9_text
    page9["pagePic"] = page9_url

    page10 = dict()
    page10["pageBackground"] = page10_background
    page10["pageType"] = page10_type
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
        "page10": page10
     }

    book = dict()
    book["Pages"] = pages
    book["Title"] = book_title

    book_json = json.dumps(book)

    books_path = os.path.join(app.root_path, BOOK_JSON_DIR)
    json_path = books_path + book["Title"] + '.json'
    tmp_json_path = books_path + 'tmp.json'
    with open(tmp_json_path, "w") as f:
        f.write(book_json)

    return preview_book(content_json=book_json)


@app.route("/save_book")
def save_book(book_name='tmp'):
    if request.args:
        book_name = request.args['book_name']
    books_path = os.path.join(app.root_path, BOOK_JSON_DIR)
    json_path = books_path + book_name + '.json'
    tmp_json_path = books_path + 'tmp.json'

    if os.path.exists(json_path):
        alert = '<script type="text/javascript">' + \
                'alert("The book name: "%s" already exists.")'%book_name + \
                '</script>'
        # raise Exception("File Exist Error")
        return alert + "The book name already exists."
    os.system('mv ' + tmp_json_path + ' ' + json_path)
    alert = '<script type="text/javascript">' + \
            'alert("Saving the book to %s")'%book_name + \
            '</script>'
    return redirect(url_for('list_books'))
    # return alert + list_books()


@app.route("/delete_book")
def delete_book(book_name='tmp'):
    if request.args:
        book_name = request.args['book_name']
    books_path = os.path.join(app.root_path, BOOK_JSON_DIR)
    json_path = books_path + book_name + '.json'

    os.system('rm ' + json_path)
    alert = '<script type="text/javascript">' + \
            'confirm("Book %s has been deleted")'%book_name + \
            '</script>'

    return redirect(url_for('list_books'))


@app.route("/edit_book")
def edit_book(book_name='tmp'):
    # todo this is not implemented yet
    if request.args:
        book_name = request.args['book_name']
    books_path = os.path.join(app.root_path, BOOK_JSON_DIR)
    json_path = books_path + book_name + '.json'
    book = json.load(open(json_path, 'r'))
    pages = book['Pages']
    book_title = book['Title']

    page_inputs = {}
    for page in pages:
        page_inputs[page] = render_template("define_single_page.html",
                                            page_id=page,
                                            page_title=pages[page]['pageTitle'],
                                            page_text=pages[page]['pageText'],
                                            page_image_url=pages[page]['pagePic'],
                                            page_background_url=pages[page]['pageBackground'])

    return render_template(
        "define_book.html",
        book_title=book_title,
        page1_input=page_inputs['page1'],
        page2_input=page_inputs['page2'],
        page3_input=page_inputs['page3'],
        page4_input=page_inputs['page4'],
        page5_input=page_inputs['page5'],
        page6_input=page_inputs['page6'],
        page7_input=page_inputs['page7'],
        page8_input=page_inputs['page8'],
        page9_input=page_inputs['page9'],
        page10_input=page_inputs['page10']
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
