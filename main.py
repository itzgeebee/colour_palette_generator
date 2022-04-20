from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
import numpy as np
from PIL import Image
import io
import base64



app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    rgb_colors = []
    pic_data = None
    if request.method == "POST":
        pic = request.files.get("picture")
        if pic and allowed_file(pic.filename):
            new_pic = Image.open(pic).convert('RGB')
            new_pic.thumbnail((500, 500))

            # encode and decode image file
            data = io.BytesIO()
            new_pic.save(data, "JPEG")
            encoded_pic = base64.b64encode(data.getvalue())
            decoded_pic = encoded_pic.decode('utf-8')
            pic_data = f"data:image/jpeg;base64,{decoded_pic}"

            rgb_colors = palette(new_pic)
            flash("palette generated successfully")

        else:
            flash(f"Please upload a valid file {ALLOWED_EXTENSIONS}")
            return redirect(url_for("home"))

    if rgb_colors is None:
        all_colours = rgb_colors
    else:
        all_colours = jsonify(rgb_colors).json

    return render_template("index.html", all_colours=all_colours,
                           pic=pic_data)


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
