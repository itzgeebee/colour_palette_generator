from flask import Flask, jsonify, render_template, request, url_for, redirect
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    rgb_colors = []
    pic = None
    if request.method == "POST":
        pic = (request.form.get("picture"))
        print(pic)
        rgb_colors = palette(pic)

    if rgb_colors is None:
        all_colours = rgb_colors
    else:
        all_colours = jsonify(rgb_colors).json
    print(all_colours)
    return render_template("index.html", all_colours=all_colours, pic=pic)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


# img = Image.open("C:/Users/gb/Pictures/my bitmoji (2).png").convert("RGB")
# print(type(img))


# arr = np.asarray(img)
# print(arr.shape)
# print(arr.ndim)

# b = (arr[:10][0])
# print(len(b))
# for i in b:
#     print(i)
# print(arr.unique(axis=0))
# vals,counts = np.unique(arr, return_counts=True, axis=0)
# index = np.argmax(counts)
# print(vals[index][10:-1])
# print(np.unique(arr, axis=0))

def palette(pic):
    """
    Return palette in descending order of frequency
    """
    arr = np.asarray(pic)
    print(arr)
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
    http://stackoverflow.com/a/16216866/190597 (Jaime)
    http://stackoverflow.com/a/16840350/190597 (Jaime)
    Warning:
    >>> asvoid([-0.]) == asvoid([0.])
    array([False], dtype=bool)
    """
    arr = np.ascontiguousarray(arr)
    return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))


# print(palette(img)[:10])

if __name__ == '__main__':
    app.run(debug=True)
