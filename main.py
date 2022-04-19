import os
from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    rgb_colors = []
    pic = None
    filename = None
    if request.method == "POST":
        pic = (request.files.get("picture"))
        if pic and allowed_file(pic.filename):
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_pic = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            rgb_colors = palette(new_pic)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("palette generated successfully")

        else:
            flash(f"Please upload a valid file {ALLOWED_EXTENSIONS}")
            return redirect(url_for("home"))

    if rgb_colors is None:
        all_colours = rgb_colors
    else:
        all_colours = jsonify(rgb_colors).json

    return render_template("index.html", all_colours=all_colours,
                           filename=filename)


def palette(pic):
    """
    Return palette in descending order of frequency
    """
    arr = np.asarray(pic)
    pal, index = np.unique(asvoid(arr).ravel(), return_inverse=True)
    pal = pal.view(arr.dtype).reshape(-1, arr.shape[-1])
    count = np.bincount(index)
    order = np.argsort(count)
    palette_list = pal[order[::-1]]
    new_pal = ['#%02x%02x%02x' % (i[0], i[1], i[2]) for i in palette_list[:10]]
    return new_pal


def asvoid(arr):
    """View the array as dtype np.void (bytes)
    This collapses ND-arrays to 1D-arrays, so you can perform 1D operations on them.
    Warning:
    >>> asvoid([-0.]) == asvoid([0.])
    array([False], dtype=bool)
    """
    arr = np.ascontiguousarray(arr)
    return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))


if __name__ == '__main__':
    app.run(debug=True)
