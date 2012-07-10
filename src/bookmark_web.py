import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import bookmarks

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['html'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
def get_resource_as_string(name, charset='utf-8'):
	with app.open_resource(name) as f:
		return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

@app.route('/')
def newpage():
	return render_template('index.html')
	
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		username = request.form['userID']
		auth = request.form['userAuth']
		data_file = request.files.get('data_file')
		data_file.save(os.path.join(UPLOAD_FOLDER, 'bookmarks.html'))
		bookmarks.import_bookmarks(username,auth,'bookmarks.html')
		return render_template('success.html')
	return render_template('index.html')

if __name__ == '__main__':
	app.debug = True
	app.run()