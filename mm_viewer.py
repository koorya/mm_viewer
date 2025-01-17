# This Python file uses the following encoding: utf-8
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
import sys
import numpy as np
import MySQLdb

from Column import *


import Manipulator as mm
from Constants import *
from opengl_drawing_tools import *
from stl_loader import *

import time 
import threading



np.set_printoptions(precision = 3)



#conn = MySQLdb.connect('localhost', 'user2', 'vbtqjpxe', 'my_new_schema')
conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', DATABASE_NAME)




scale = 0.0003
treecolor = (1.0, 1.0, 1.0, 1.0)
green_color = (0.0, 1.0, 0.0, 1.0)
red_color = (1.0, 0.0, 0.0, 1.0)
blue_color = (0.0, 0.0, 1.0, 1.0)
yellow_color = (1.0, 0.8, 0.0, 1.0)
pink_color = (1.0, 0.0, 0.5, 1.0)
black_color = (0.0, 0.0, 0.0, 1.0)

def calback():
	pass





floor1 = Floor((0.0, 0.0, -636.5), (0.0, 0.0, 1.0), 0.0)
floor2 = FilledFloor((0.0, 0.0, -636.5 - 3000.0), (0.0, 0.0, 1.0), 0.0)
#floor2 = Floor((0.0, 0.0, -636.5 - 3000.0), (0.0, 0.0, 1.0), 0.0)
field = FieldDB((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 0.0)
field.append_child(floor1)
field.append_child(floor2)

#field.append_child(LinkSloped((-1750, 0, 0), (1, 0, 0), 180.0))


manip = mm.Manipulator()
res_pos = (-1750.0, 720.5, 652.8, 0.0, 0.0)
conf = manip.getConfigByTarget(res_pos)
conf = np.zeros(10)
conf[0] = H #2618.5
conf[1] = 617

manip.setConfig(conf)
manip.setActiveField(field)
manip.startUpdateConfigByDBTread()

#target_x, target_y, target_z, target_theta, target_phi


state = 'q'

conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', DATABASE_NAME)
time_stamp = time.time()
call_cnt = 0

def timercallback(value):
	global manip, conn, time_stamp, call_cnt, id, field

	call_cnt += 1
	if (call_cnt % 500 == 0):
		print "time: ", (time.time()-time_stamp)/500.
		time_stamp = time.time()
	glutPostRedisplay()
	glutTimerFunc(10, timercallback, 1)
	pass


key_f, key_t = 1, 0
target_x, target_y, target_z, target_theta, target_phi = manip.getTarget() # 1.28e+3, 0, 1.118e+3, 0, 00
def mouse_wheel_funct(button, dir, x, y):
	global scale
	global state
	global key_f
	global key_t
	global target_x
	global target_y
	global target_z
	global target_theta
	global target_phi
	global eye_dir, eye_pos
	global sens_alpha, sens_beta

	# print "button: ", button

	_phi = np.deg2rad(90 - manip.joints[0].q - manip.joints[3].q)
	_theta = np.deg2rad(manip.joints[4].q)
	
	add_config = manip.getConfig()
	add_pos = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
	
	key_t = 1
	if state == 'q':
		scale += (0.00001+key_f*0.0001)*dir
		eye_pos += dir*150*eye_dir
	elif state == '1':
		add_config[0] += (1.0+key_f*10)*dir
		key_t = 0
	elif state == '2':
		add_config[1] += (1.0+key_f*10)*dir
		key_t = 0
	elif state == '3':
		add_config[2] += (1.0+key_f*10)*dir
		key_t = 0
	elif state == '4':
		add_config[3] += (1.0+key_f*10)*dir
		key_t = 0
	elif state == '5':
		add_config[4] += (1.0+key_f*10)*dir
		key_t = 0
	elif state == '6':
		add_config[5] += (1.0+key_f*10)*dir
		key_t = 0
	elif state == '7':
		add_config[6] += (1.0+key_f*10)*dir
		key_t = 0
	elif state == '8':
		add_config[7] += (1.0+key_f*10)*dir
		key_t = 0
	elif state == '9':
		add_config[8] += (1.0+key_f*10)*dir
		key_t = 0

	elif state == '-':
		add_pos += np.array([0, 0, 0, (1.0+key_f*10)*dir, 0])
	elif state == '=':
		add_pos += np.array([0, 0, 0, 0, (1.0+key_f*10)*dir])
	elif state == 'x':
		add_pos += np.array([(1.0+key_f*10)*dir, 0, 0,0, 0])
	elif state == 'y':
		add_pos += np.array([0, (1.0+key_f*10)*dir, 0,0, 0])
	elif state == 'z':
		add_pos += np.array([0, 0, (1.0+key_f*10)*dir, 0, 0])

	elif state == 'c': #вдоль балки (проверил, точно работает)
		add_pos += np.array([(1.0+key_f*10)*dir*np.cos(_phi)*np.sin(_theta), 
							-(1.0+key_f*10)*dir*np.sin(_phi)*np.sin(_theta), 
							-(1.0+key_f*10)*dir*np.cos(_theta),
							0, 0])
	elif state == 'v':# ортогонально балке вдоль кисти (проверил, работает)
		add_pos += np.array([-(1.0+key_f*10)*dir*np.cos(_phi-np.pi/2), 
							(1.0+key_f*10)*dir*np.sin(_phi-np.pi/2), 
							0,
							0, 0])
	elif state == 'b': # ортогонально балке ортогонально кисти
		add_pos += np.array([-(1.0+key_f*10)*dir*np.cos(_phi)*np.sin(_theta+np.pi/2), 
							(1.0+key_f*10)*dir*np.sin(_phi)*np.sin(_theta+np.pi/2), 
							(1.0+key_f*10)*dir*np.cos(_theta+np.pi/2),
							0, 0])

		
	# print "scale: %.5f"%scale
	# print "key_t: %i"%key_t
	# print "theta: %i"%target_theta,"phi: %i"%target_phi 

	if key_t != 1:
		manip.setConfig(add_config)
		manip.calc_kinematics()
		
#	glutPostRedisplay()

# Процедура обработки специальных клавиш
def keyboard_funct(key, x, y):
	global state
	global key_f
	global key_t
	global target_x, target_y, target_z, target_theta, target_phi, manip
	global aspect, prj_mode, program1, program2
	if key == 'f':
		key_f = 1
	elif key == 'g':
		key_f = 0
	elif key == 't':
		target_x, target_y, target_z, target_theta, target_phi = manip.getTarget()
		key_t = 1
	elif key == 'r':
		key_t = 0
	elif key == ',':
		glUseProgram(program2)
		key_t = 0
	elif key == '.':
		glUseProgram(program1)
		key_t = 0
	elif key == 'k':
		if prj_mode == "perspective":
			prj_mode = "ortho"
		else:
			prj_mode = "perspective"
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		if prj_mode == "perspective":
			gluPerspective(40, aspect, 0.01, 30)
		else:
			glOrtho(-aspect, aspect, -1.0, 1.0, -1.0, 50.0)	
		glScale(0.0003, 0.0003, 0.0003)
	elif key == '[':
		manip.hanger_joints[0].switch_state()
		key_t = 0
	elif key == ']':
		manip.hanger_joints[1].switch_state()
		key_t = 0
	else:
		state = key
	print key
#	glutPostRedisplay()

def specialkeys(key, x, y):
	global eye_pos, eye_dir
	speed = 150
	# Обработчики для клавиш со стрелками
	if key == GLUT_KEY_UP:	  # Клавиша вверх
		eye_pos += speed*eye_dir			 # Уменьшаем угол вращения по оси X
	if key == GLUT_KEY_DOWN:	# Клавиша вниз
		eye_pos -= speed*eye_dir			 # Увеличиваем угол вращения по оси X
	if key == GLUT_KEY_LEFT:	# Клавиша влево
		eye_pos -= speed*np.cross(eye_dir, np.array([0, 0, 1]))			 # Уменьшаем угол вращения по оси Y
		
	if key == GLUT_KEY_RIGHT:   # Клавиша вправо
		eye_pos += speed*np.cross(eye_dir, np.array([0, 0, 1]))			 # Увеличиваем угол вращения по оси Y
	print eye_pos
#	glutPostRedisplay()		 # Вызываем процедуру перерисовки
	
last_x, last_y = 0, 0
left_button_state = 0
right_button_state = 0
middle_button_state = 0
alpha, beta = -5.46, -0.85
def active_mouse_motion(x, y):
	global last_x, last_y, alpha, beta, eye_dir, eye_pos
	pwr = 0.001
	if right_button_state:
		if x!=last_x:
			alpha += pwr*(x-last_x)
		if y!=last_y:
			beta += pwr*(y-last_y)
			pi_2 = np.pi/2
			if beta >= pi_2:
				beta = pi_2*0.999
			if beta <= -pi_2:
				beta = -pi_2*0.999
	elif left_button_state:
		vec = np.cross(eye_dir, np.array([0, 0, 1]))
		vec /= np.linalg.norm(vec)
		eye_pos -= 10*(x-last_x)*vec
		eye_pos += 10*(y-last_y)*np.cross(vec, eye_dir)
	elif middle_button_state:
		eye_pos -= (y-last_y)*50*eye_dir

	# print "alpha: ", alpha, "  beta: ", beta
	# print "x: ", x, "  y: ", y
	last_x, last_y = x, y
	eye_dir = np.array([np.cos(alpha)*np.cos(beta), np.sin(alpha)*np.cos(beta), np.sin(beta)])
#	glutPostRedisplay()

def passive_mouse_motion(x, y):
	pass 
	
def mouse_funct(button, state, x, y):
	global last_x, last_y, left_button_state, right_button_state, middle_button_state

	if button == 0:
		left_button_state = not state
	if button == 2:
		right_button_state = not state
	if button == 1:
		middle_button_state = not state
	# print "left: ", left_button_state
	# print "right: ", right_button_state		
	last_x, last_y = x, y

# Процедура инициализации
def init():
	global xrot		 # Величина вращения по оси x
	global yrot		 # Величина вращения по оси y
	global ambient	  # Рассеянное освещение

	global treecolor	# Цвет елочного ствола
	global lightpos	 # Положение источника освещения
	global program1, program2





	xrot = 0.0						  # Величина вращения по оси x = 0
	yrot = 0.0						  # Величина вращения по оси y = 0
	ambient = (0.5, 0.5, 0.5, 1.0)		# Первые три числа - цвет в формате RGB, а последнее - яркость
#	ambient = (0.0, 0.0, 0.0, 1.0)		# Первые три числа - цвет в формате RGB, а последнее - яркость

	glEnable(GL_DEPTH_TEST) 
	glEnable(GL_NORMALIZE)
#	glEnable(GL_COLOR_MATERIAL)
	glClearColor(0.7, 0.7, 0.7, 1.0)				# Серый цвет для первоначальной закраски
#	glOrtho(-1.0, 1.0, -1.0, 1.0, -50.0, 50.0)				# Определяем границы рисования по горизонтали и вертикали

#	glRotatef(-90, 1.0, 0.0, 0.0)				   # Сместимся по оси Х на 90 градусов
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient) # Определяем текущую модель освещения
	glEnable(GL_LIGHTING)						   # Включаем освещение
	glEnable(GL_LIGHT0)							 # Включаем один источник света
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
	glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 0.0, 0.0, 1.0))
	glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 0.0))


	vertex2 = create_shader(GL_VERTEX_SHADER, """
	varying vec4 vertex_color;
				void main(){
					gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
					//vertex_color = gl_Color;
				}""")

	vertex = create_shader(GL_VERTEX_SHADER, """
	varying vec4 vertex_color;
				void main(){
					gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
					vertex_color = gl_Color;
				}""")
	# Создаем фрагментный шейдер:
	# Определяет цвет каждого фрагмента как "смешанный" цвет его вершин
	fragment = create_shader(GL_FRAGMENT_SHADER, """
	varying vec4 vertex_color;
				void main() {
					gl_FragColor = vertex_color;
	}""")
	# Создаем пустой объект шейдерной программы
	program1 = glCreateProgram()
	program2 = glCreateProgram()
	
	# Приcоединяем вершинный шейдер к программе
	glAttachShader(program2, vertex2)
	# Присоединяем фрагментный шейдер к программе
	glAttachShader(program2, fragment)
	# "Собираем" шейдерную программу
	glLinkProgram(program2)	
	
	# Приcоединяем вершинный шейдер к программе
	glAttachShader(program1, vertex)
	# Присоединяем фрагментный шейдер к программе
	glAttachShader(program1, fragment)
	# "Собираем" шейдерную программу
	glLinkProgram(program1)

	glUseProgram(program2)		


	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
#	gluPerspective(40, aspect, 0.01, 30)
	glOrtho(-1.0, 1.0, -1.0, 1.0, -50.0, 50.0)	
	glScale(0.0003, 0.0003, 0.0003)




aspect = 1.0
prj_mode = "perspective"
def resize_window(w, h):
	global aspect, prj_mode
	glViewport(0, 0, w, h)
	aspect = 1.0*w/h

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	if prj_mode == "perspective":
		gluPerspective(40, aspect, 0.01, 30)
	else:
		glOrtho(-aspect, aspect, -1.0, 1.0, -1.0, 50.0)	
	glScale(0.0003, 0.0003, 0.0003)
	pass

eye_pos = np.array([-3430.0, -6455.0, 6825.0])
eye_dir = np.array([ 0.44871517,  0.48397567, -0.75128041])


# Процедура перерисовки


#some_model = Loaded_Model()
#some_model.load_model("models/test.stl")

def draw():
	global xrot
	global yrot
	global lightpos
	global greencolor
	global treecolor
	global aspect, prj_mode
	global field, floor1, floor2, manip
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)								# Очищаем экран и заливаем серым цветом


	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	if prj_mode == "perspective":
		gluPerspective(40, aspect, 0.01, 30)
	else:
#		ortho_pos = np.linalg.norm(np.array([eye_pos[0], eye_pos[1], eye_pos[2]]))*0.0003
		glOrtho(-aspect, aspect, -1.0, 1.0, -1.0, 50.0)	
	glScale(0.0003, 0.0003, 0.0003)
	
	center_pos = eye_pos + eye_dir	
	gluLookAt(eye_pos[0], eye_pos[1], eye_pos[2], center_pos[0], center_pos[1], center_pos[2], 0, 0, 1)
	
	
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()	
	glLightfv(GL_LIGHT0, GL_POSITION, (eye_pos[0], eye_pos[1], eye_pos[2], 1.0))	
	
	draw_grid(1000);
	
	manip.draw()
	field.draw_vertex_list()

#	some_model.draw()


	glutSwapBuffers()							
	
#	print "draw execute"
	pass

	


glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) 
glutInitWindowSize(1300, 900)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow(b"MM kinematick viewer")
glutDisplayFunc(draw)
glutSpecialFunc(specialkeys)
glutKeyboardFunc(keyboard_funct)
glutReshapeFunc(resize_window)
glutMouseWheelFunc(mouse_wheel_funct)
glutMotionFunc(active_mouse_motion)
glutPassiveMotionFunc(passive_mouse_motion)
glutMouseFunc(mouse_funct)
glutTimerFunc(100, timercallback, 1)
init()

field.startUpdateThread()



glutMainLoop()

