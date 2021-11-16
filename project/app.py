from flask import Flask, render_template, Response, flash
from camera import Video
import cv2
import time
import os
from foto import mainfuntion

app=Flask(__name__)

descripcionTexto = {
    'rectangular':'A las personas con rostro rectangular les favorecen unas gafas que consigan acortar la largura que aporta esta forma facial. Es indispensable evitar gafas alargadas horizontalmente.',
    'alargada':'Para este tipo de cara la proporción también es esencial, ya que las que más le favorecen son las que tienen la lente alargada, pero con una estructura no demasiado ancha.',
    'cuadrada':'Para las personas que tienen un rostro cuadrado son favorecedoras las gafas con forma ovalada o redonda, para suavizar las líneas faciales.',
    'redonda':'Si tienes la cara redonda, apuesta por formas rectangulares y estrechas para conseguir un efecto de contraste. Es importante que la montura sea proporcionada a la anchura y altura de tu cara. El puente transparente puede ser de ayuda para crear espacio entre los ojos. Las gafas con un diseño más llamativo en la parte superior de la montura también favorecen a este tipo de cara.',
    'triangular':'Las personas con este tipo de cara suelen tener pronunciados el mentón y la mandíbula. Para contrarrestar esto, lo mejor es elegir monturas que acentúen la parte superior del rostro, ya sea con colores llamativos, medias monturas o con diseños originales.',
    'ovalada':'A las personas con rostro ovalado le sientan bien, prácticamente, cualquier tipo de gafas, ya que las proporciones de su cara son consideradas ideales.'}

imagenes = os.path.join('static','img')
app.config['UPLOAD_FOLDER'] = imagenes
# settings
#app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    #flash('Foto Tomada Satisfactoriamente')
    return render_template('index.html')

def gen(camera):
    while True:
        frame,img=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')
@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/prueba')
def probando():
    time.sleep(1.5)
    variable = mainfuntion()
    print(variable*100)
    print(variable*100)
    print(variable*100)
    print(variable*100)
    text=variable
    imag_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'example_uno.png')
    return render_template('prueba.html', variable=variable,text=text, img_1 = imag_1)
app.run(host="0.0.0.0")