from app import app
from flask import render_template, request, redirect, url_for, jsonify, make_response
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import  send_from_directory, abort

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d, %b, %y")


@app.route("/")
def index():
    print(app.config["DB_NAME"])
    return render_template("public/index.html")

@app.route("/jinja")
def jinja():
    my_name = "Laban Kibet"
    langs = ["pytho", "go", "javascript", "ruby"]
    friends = {
        "kevo": 26,
        "larry": 30,
        "frank": 37,
        "caleb": 47,
    }

    colors = ("red", "green", "yellow")

    cool = True

    date = datetime.utcnow()

    #class GitRemote:
     #   def __init__(self, name, description, url):
      #      self.name = name
       #     self.description = description
        #    self.url = url
#
 #       def pull(self):
  #          return f'pull repo {self.name}'
   #     def clone(self):
    #        return f'cloning into  {self.url}'
   # my_remote = GitRemote(
    #    name = "Flask Jinja",
     #   description = "Templates design tutorial",
      #  url= "https://github.com/laban254/jinja.git"
#
#
 #   )
    
    def  repeat(x, qty):
        return x * qty

    my_html = "<hi> html file</hi>"

    return render_template("public/jinja.html", my_name = my_name,
                           langs= langs, friends = friends, colors= colors,
                           cool = cool, GitRemote = GitRemote, repeat = repeat,
                           my_remote = my_remote, date=date, my_html = my_html
                           )

@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/sign-up", methods = ["GET",  "POST"])
def sign_up():
    if request.method == "POST":

        req = request.form
        username = req["username"]
        email = req["email"]
        password = request.form["password"]
        print(username, email, password)

        return redirect(url_for('about'))

    return render_template("public/sign_up.html")

users = {
	"mitshik": {
		"fname": "laban",
		"sname": "kibet"
	},
	"benz": {
		"fname": "laban2",
		"sname": "kibet2"
	},
	"volvo": {
		"fame": "laban3",
		"sname": "kibet3"
	}}


@app.route("/profile/<username>")
def profile(username):

    user = None
    if username in users:
        user = users[username]
        print(user)
        print(username)
    
    return render_template("public/profile.html", username = username, user = user)

@app.route("/multiple/<forr>/<bar>/<baz>")
def multiple(forr, bar, baz ):
    return "forr is {}, bar is {}. baz is {}".format(forr, bar, baz)


@app.route("/json", methods=["post"])
def jason():
    if request.is_json:
        req = request.get_json()
        response = {
            "message": "jason received",
            "name": req.get("name")
        }
        res = make_response(jsonify(response), 200)
        return res
    else:
        res = make_response(jsonify({"message": "no jsaon received"}), 400)
        return res


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=['post'])
def  create_entry():
    req = request.get_json()

    print(req)
    res = make_response(jsonify({"message": "JSON received"}), 200)

    return res

#query strings

@app.route('/query')
def query():
    args = request.args
    if "foo" in args:
        foo = args.get("foo")
        print(foo)
    return "query received", 200


app.config["IMAGE_UPLOADS"] = "/home/kibe/flask/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSION"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"]  =  0.5 * 1024 * 1024

def allowed_image(filename):
    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in  app.config["ALLOWED_IMAGE_EXTENSION"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <=   app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False




#uploading images

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if a file was uploaded
        #if 'image' in request.files:
        if request.files:

            if allowed_image_filesize(request.cookies.get("filesize")):
                 print("file exceeded Max size")
                 return redirect(request.url)

            image = request.files['image']
            if image.filename == "":
                print("image must have a file name")
                return redirect(request.url)
            
            if allowed_image(image.file):
                print("that image extension is not allowed")
                return redirect(request.url)
            
            else:
                filename = secure_filename(image.filename)
            
 
            # Save the uploaded file to a folder of your choice
                image.save(os.path.join(app.config["IMAGE_UPLOADS"],  filename))
            # Optionally, perform any additional processing or validation on the uploaded file
            print("image saved")
            # Redirect or render a template to show a success message
            return "Image uploaded successfully!"
    # If no file was uploaded or GET request, render the form template
    return render_template('public/upload_image.html')


# to send you need to import send_from_directory from flask

"""
string:
uuid:
int:
float:
path:
"""

app.config["CLIENT_IMAGES"]  = "location path"

@app.route("/get-image/<image_name>")
def get_image(image_name):
    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

@app.route("/get-csv/<filename>")
def get_csv(filename):
    try:
        return send_from_directory(
            app.config["CLIENT_csv"], filename=filename, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

@app.route("/get-report/<path:path>")
def get_report(path):
    try:
        return send_from_directory(
            app.config["CLIENT_REPORT"], filename=path, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)


"""
working with cookies in flask
"""
from flask import make_response

@app.route("/cookies")
def cookies():
    res = make_response("cookies", 200)

    res.set_cookies(
        "flovor",
        value="chocolate chip",
        max_age=10,
        expire=None,
        domain=None,
        secure=False,
        httponly=False

    )
    return res

