from flask import Flask, render_template, request, make_response, Response
import cv2
import numpy as np
import datetime
from foto import mainfuntion
from camera import get_frame

app = Flask(__name__)

descripcionTexto = {
    'rectangular':'A las personas con rostro rectangular les favorecen unas gafas que consigan acortar la largura que aporta esta forma facial. Es indispensable evitar gafas alargadas horizontalmente.',
    'alargada':'Para este tipo de cara la proporción también es esencial, ya que las que más le favorecen son las que tienen la lente alargada, pero con una estructura no demasiado ancha.',
    'cuadrada':'Para las personas que tienen un rostro cuadrado son favorecedoras las gafas con forma ovalada o redonda, para suavizar las líneas faciales.',
    'redonda':'Si tienes la cara redonda, apuesta por formas rectangulares y estrechas para conseguir un efecto de contraste. Es importante que la montura sea proporcionada a la anchura y altura de tu cara. El puente transparente puede ser de ayuda para crear espacio entre los ojos. Las gafas con un diseño más llamativo en la parte superior de la montura también favorecen a este tipo de cara.',
    'triangular':'Las personas con este tipo de cara suelen tener pronunciados el mentón y la mandíbula. Para contrarrestar esto, lo mejor es elegir monturas que acentúen la parte superior del rostro, ya sea con colores llamativos, medias monturas o con diseños originales.',
    'ovalada':'A las personas con rostro ovalado le sientan bien, prácticamente, cualquier tipo de gafas, ya que las proporciones de su cara son consideradas ideales.',
    'corazon': 'Las personas con rostro corazón deben usar gafas de tamaño mediano, sin alcanzar las mejillas. Así se conseguirá equilibrar las facciones.'}

imagenesTipos = {
    'alargada':['https://i.ibb.co/5BFKM1L/Recomendaci-n-para-Rostro-Alargado.png','https://i.ibb.co/BP75G83/Recomendaci-n-para-Rostro-Ovalado.png','https://i.ibb.co/yYRh3cH/Recomendaci-n-para-Rostro-Alargado.png' ],
    'rectangular':['https://i.ibb.co/ynS19fB/Recomendacion-1-para-Rostro-Rectangular.png','https://i.ibb.co/C8QXCDG/Recomendacion-2-para-Rostro-Rectangular.png','https://i.ibb.co/K7Gx4Cx/Recomendacion-3-para-Rostro-Rectangular.png'],
    'cuadrada':['https://i.ibb.co/cLMJ1pr/Recomendaci-n-para-Rostro-Cuadrado.png','https://i.ibb.co/pP3Xvd8/Recomendaci-n-para-Rostro-Cuadrado.png','https://i.ibb.co/bPcT0Zx/Recomendaci-n-para-Rostro-Cuadrado.png'],
    'redonda': ['https://i.ibb.co/2hK3rzp/Recomandacion-1-para-Rostro-Redondo.png','https://i.ibb.co/93xf1f4/Recomandacion-2-para-Rostro-Redondo.png','https://i.ibb.co/H4Js0wc/Recomandacion-3-para-Rostro-Redondo.png'],
    'triangular':['https://i.ibb.co/gMRg9hc/Recomendacion-1-para-Rostro-Triangular.png','https://i.ibb.co/7SkLMzX/Recomendacion-2-para-Rostro-Triangular.png','https://i.ibb.co/Drz1g6L/Recomendacion-3-para-Rostro-Triangular.png'],
    'ovalada':['https://i.ibb.co/LCCpDKQ/Recomendaci-n-para-Rostro-Ovalado.png','https://i.ibb.co/mT1JG9P/2.png" alt="2','https://i.ibb.co/T2J5b0G/3.png'],
    'corazon':['https://i.ibb.co/gMRg9hc/Recomendacion-1-para-Rostro-Triangular.png','https://i.ibb.co/7SkLMzX/Recomendacion-2-para-Rostro-Triangular.png','https://i.ibb.co/Drz1g6L/Recomendacion-3-para-Rostro-Triangular.png'],
}

imgen  = [0]
@app.route('/')
def index():
    return render_template("index.html")

def send_file_data(data, mimetype='image/jpeg', filename='output.jpg'):
    # https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database/11017839

    response = make_response(data)
    response.headers.set('Content-Type', mimetype)
    response.headers.set('Content-Disposition', 'attachment', filename=filename)

    return response

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #print(request.files)  # it slowdown video
        #print(request.data)   # it slowdown video
        #fs = request.files['snap'] # it raise error when there is no `snap` in form
        fs = request.files.get('snap')
        if fs:
            #print('FileStorage:', fs)
            #print('filename:', fs.filename)

            # https://stackoverflow.com/questions/27517688/can-an-uploaded-image-be-loaded-directly-by-cv2
            # https://stackoverflow.com/a/11017839/1832058
            img = cv2.imdecode(np.frombuffer(fs.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            imgen[0] = img 
            img2 = get_frame(img)
            #cv2.imshow('image', img)
            #cv2.waitKey(1)

            # https://jdhao.github.io/2019/07/06/python_opencv_pil_image_to_bytes/
            ret, buf = cv2.imencode('.jpg', img)

            #return f'Got Snap! {img.shape}'
            return send_file_data(img2)
        else:
            #print('You forgot Snap!')
            return 'You forgot Snap!'

    return 'Hello World!'
@app.route('/prueba')
def probando():
    variable = mainfuntion(imgen[0])
    print(variable)
    text = descripcionTexto[variable]
    # imag_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'example_uno.png')
    img_1 = imagenesTipos[variable][0]
    img_2 = imagenesTipos[variable][1]
    img_3 = imagenesTipos[variable][2]
    if variable == 'corazon':
        variable = 'corazón'
    return render_template('prueba.html', variable=variable.capitalize(),text=text, img_1 = img_1,img_2 = img_2, img_3 = img_3)

def generate():
    frame = imgen[0]
    cv2.imwrite('output.jpg',frame)
    yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + bytearray(frame) +
         b'\r\n\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    # camera can work with HTTP only on 127.0.0.1
    # for 0.0.0.0 it needs HTTPS so it needs `ssl_context='adhoc'` (and in browser it need to accept untrusted HTTPS
    #app.run(host='127.0.0.1', port=5000)#, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')