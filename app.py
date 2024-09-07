import os
from flask import Flask, flash, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from main import identify_cosmetic_synchronous  # Import the function from your main.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./"


@app.post("/send")
def send():
    if request.method == 'POST':
        if 'file' not in request.files:
            return make_response({"file": "is_required"}, 400)

        file = request.files['file']
        if file.filename == '':
            return make_response({"file": "no_file_selected"}, 400)

        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        try:
            result = identify_cosmetic_synchronous(path)
            os.remove(path)
            if result:
                return make_response({"data": result}, 200)
            else:
                return make_response({"data": "No match found"}, 200)

        except Exception as error:
            return make_response({"error": str(error)}, 500)


@app.get("/")
def index():
    return '''
    <!doctype html>
    <title>Upload a File</title>
    <h1>Upload a File</h1>
    <form method="post" enctype="multipart/form-data" action="/send">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
