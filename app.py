from flask import Flask, request, make_response, render_template, Response
import numpy as np
from service import save_img
from camera import get_frame
app = Flask(__name__)
image = [np.fromfile('ejemplo.dat')]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/capture_img', methods=['POST'])
def capture_img():
    msg,imgg = save_img(request.form["img"])
    image[0] = imgg
    return make_response(msg)


def generate():
    while True:
        frame = get_frame(image[0])

        yield(b'--frame\r\n'
        b'Content-Type:  image/jpeg\r  \n\r\n' + frame +
            b'\r\n\r\n')
@app.route("/video_feed")
def video_feed():
    return Response(generate(),
    mimetype='multipart/x-mixed-replace; boundary=frame')
app.run(debug = True, port=8000)