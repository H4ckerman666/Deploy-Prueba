import cv2
import os
import os.path
import math
import platform
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import mediapipe as mp
from calculoRostros import principal

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


#function left's points to right's points
def points_leftorRight(list,leftorright):
  #declaramos los puntos de la izquierda
  if leftorright:
    points = [152,148,176,149,150,136,172,58]
  #puntos de la derecha
  else:
    points = [152,377,400,378,379,365,397,288]

  #pointlist tiene la lista con x,y,z de los anteriores
  pointlist = []  
  #llena la lista de pointlist
  for add in points:
    pointlist.append(list[add])
  
  #Calculo del ancho de la cara
  ancho = (((list[454].x - list[234].x)**2) + ((list[454].y - list[234].y)**2))**(1/2)
  #Calculo del largo de la cara
  largo = (((list[152].x - list[10].x)**2) + ((list[152].y - list[10].y)**2))**(1/2)
  
  #lista de los angulos
  list_angulos = []

  #recorre los 8 puntos 
  for i in range(7):
    #print(pointlist[i])
    #print(pointlist[i+1])

    distanceX = pointlist[i].x - pointlist[i+1].x
    if distanceX < 0:
      distanceX *= -1
    distanceX /= ancho
    #print("ancho", ancho)
    #print(distanceX)
    #Calculo de distancia y
    distanceY = pointlist[i].y - pointlist[i+1].y
    if distanceY < 0:
      distanceY *= -1
    distanceY /= largo
    #print("largo", largo)
    #print(distanceY)
    #Calculo de hipotenusa
    hipotenusa = (((pointlist[i].x - pointlist[i+1].x)**2) + ((pointlist[i].y - pointlist[i+1].y)**2))**(1/2)
    #print(hipotenusa)
    #Calculo del angulo
    angulo = math.atan(distanceY/distanceX)
    angulo = math.degrees(angulo)
    #guardamos los angulos de la derecha e izquierda
    #angulos de la izquierda
    if leftorright:
      list_angulos.append(angulo)
    #angulos de la derecha
    else:
      list_angulos.append(angulo)

  return list_angulos, largo, ancho




def mainfuntion():
  #declaracion de la lista de imagen
  file_list = []

  # path diferente dependiendo del sistema operativo
  operativeSystem = platform.system()
  if 'Linux' == operativeSystem:
    file_list.append('static/img/foto4.jpg')
  else:
    file_list.append('static\\img\\foto4.jpg')

  #implementacion de libreria mediapipe
  drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
  with mp_face_mesh.FaceMesh(
      static_image_mode=True,
      max_num_faces=1,
      min_detection_confidence=0.5) as face_mesh:
    #recorrido de la lista de imagenes 
    for file in file_list: 
      image = cv2.imread(file)
      # Convert the BGR image to RGB before processing.
      results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
      # Print and draw face mesh landmarks on the image.
      if not results.multi_face_landmarks:
        continue
      annotated_image = image.copy()  
      #recorrimiento de puntos de la mandibula derecha e izquierda  
      for face_landmarks in results.multi_face_landmarks:
        izQuierda, l, a= points_leftorRight(face_landmarks.landmark,False)
        deRecha, l, a = points_leftorRight(face_landmarks.landmark,True)
      typerostro = principal(l,a,izQuierda,deRecha)
      return typerostro

mainfuntion()