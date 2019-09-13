# This Python file uses the following encoding: utf-8
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
from opengl_drawing_tools import *
from World_Components import *
import numpy as np
# this comment is on both repo

import struct

class Loaded_Model(Mounted_Component):
	model = []
	vertexes = []
	normals = []
	colors = []
	color = (0.25, 0.35, 0.25, 0.9)
	program = None
	def __init__(self, file_name = None, color = "#a55505"):
		self.color = list(1.*int(color[i:i+2], 16)/0xff for i in (1, 3, 5))
		self.color.append(0.8)
		if not file_name is None:
			self.load_model(file_name)


	
	def load_model(self, file_name = 'models/test.stl'):
		return
		f = open(file_name)
		if f.read(5) != "solid":
			f.close()
			self.load_model_bin(file_name)
			return 
			
		state = "start"
		a, b, c = (0., 0., 0.)

		triangle = []
		self.model = []
		for line in f:
			line_spl = line.split()
			for word in line_spl:
				if state == "normal" or state == "vertex":
					a = float(word)
					state = "read_1"
				elif state == "read_1":
					b = float(word)
					state = "read_2"		
				elif state == "read_2":
					c = float(word)
					state = "def_state"
					triangle.append([a, b, c])
					if len(triangle) == 4:
						self.model.append(triangle)
						triangle = []
				else:
					state = word
		self.transform_vertex_array()
		self.model = []

	def load_model_bin(self, file_name = 'models/Component1.stl'):
	
		data = open(file_name, "rb").read()
		
		triangle_count = struct.unpack("I", data[80:84])[0]
		
		print "in ", file_name, " triangle count ", triangle_count
		
		a, b, c = (0., 0., 0.)

		triangle = []
		self.model = []

		for i in range(triangle_count):
			base = 84 + i * 50;
			
			(a, b, c) = struct.unpack("fff", data[base:base+12])
			triangle.append([a, b, c])
			(a, b, c) = struct.unpack("fff", data[base+12:base+12+12])
			triangle.append([a, b, c])
			(a, b, c) = struct.unpack("fff", data[base+12+12:base+12+12+12])
			triangle.append([a, b, c])
			(a, b, c) = struct.unpack("fff", data[base+12+12+12:base+12+12+12+12])
			triangle.append([a, b, c])
			attr_byte_count = struct.unpack("h", data[base+12+12+12+12:base+12+12+12+12+2])
			
			
			self.model.append(triangle)
			triangle = []

		self.transform_vertex_array()
		self.model = []

	def transform_vertex_array(self):
		self.vertexes = np.empty(len(self.model)*9)
		self.normals = np.empty(len(self.model)*9)

		for indx, i in enumerate(self.model):
			self.vertexes[indx*9+0] = i[1][0]
			self.vertexes[indx*9+1] = i[1][1]
			self.vertexes[indx*9+2] = i[1][2]
			
			self.vertexes[indx*9+3] = i[2][0]
			self.vertexes[indx*9+4] = i[2][1]
			self.vertexes[indx*9+5] = i[2][2]

			self.vertexes[indx*9+6] = i[3][0]
			self.vertexes[indx*9+7] = i[3][1]
			self.vertexes[indx*9+8] = i[3][2]
			

			self.normals[indx*9+0] = i[0][0]
			self.normals[indx*9+1] = i[0][1]
			self.normals[indx*9+2] = i[0][2]
			
			self.normals[indx*9+3] = i[0][0]
			self.normals[indx*9+4] = i[0][1]
			self.normals[indx*9+5] = i[0][2]

			self.normals[indx*9+6] = i[0][0]
			self.normals[indx*9+7] = i[0][1]
			self.normals[indx*9+8] = i[0][2]
			
		self.colors = np.array([[self.color[:3]]*len(self.vertexes)]).ravel()	
		print len(self.vertexes)
				
	def draw_(self):
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glBegin(GL_TRIANGLES)
		for i in self.model:
			glNormal3f(i[0][0], i[0][1], i[0][2])
			glVertex3f(i[1][0], i[1][1], i[1][2])
			glVertex3f(i[2][0], i[2][1], i[2][2])
			glVertex3f(i[3][0], i[3][1], i[3][2])
		glEnd()

	def draw(self):
	#	print self.colors
		if self.program is None:
			try:
				vertex2 = create_shader(GL_VERTEX_SHADER, 
							"""varying vec4 vertex_color;
							void main() {
			
						vec3 normal, lightDir;
						vec4 diffuse;
						float NdotL;
						
						/* сначала трансформируем нормаль в нужные координаты и нормализуем результат */
						normal = normalize(gl_NormalMatrix * gl_Normal);
						
						/* Теперь нормализуем направление света. Учтите, что согласно спецификации
						OpenGL, свет сохраняется в пространстве нашего взгляда. Также, так как мы 
						говорим о направленном свете, поле "позиция" - это и есть направление. */
						lightDir = normalize(vec3(gl_LightSource[0].position));

						/* вычислим косинус угла между нормалью и направлением света. Свет у нас
						направленный, так что направление - константа для каждой вершины. */
						NdotL = max(dot(normal, lightDir), 0.0);
						
						/* вычисляем диффуз */
						diffuse = gl_FrontMaterial.diffuse * gl_LightSource[0].diffuse;
						
						gl_FrontColor =  NdotL * diffuse;
						
						gl_Position = ftransform();
					}""")

				# Создаем фрагментный шейдер:
				# Определяет цвет каждого фрагмента как "смешанный" цвет его вершин
				fragment = create_shader(GL_FRAGMENT_SHADER, """
				varying vec4 vertex_color;
							void main() {
								gl_FragColor = gl_Color;
				}""")
				# Создаем пустой объект шейдерной программы
				self.program = glCreateProgram()
				
				# Приcоединяем вершинный шейдер к программе
				glAttachShader(self.program, vertex2)
				# Присоединяем фрагментный шейдер к программе
				glAttachShader(self.program, fragment)
				# "Собираем" шейдерную программу
				glLinkProgram(self.program)	
			except Exception as e:
				print "except", e
				return
				pass
		
			

		glUseProgram(self.program)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glEnableClientState(GL_VERTEX_ARRAY)            # Включаем использование массива вершин
		glEnableClientState(GL_NORMAL_ARRAY)            # Включаем использование массива вершин
	#	glEnableClientState(GL_COLOR_ARRAY)
		# Указываем, где взять массив верши:
		# Первый параметр - сколько используется координат на одну вершину
		# Второй параметр - определяем тип данных для каждой координаты вершины
		# Третий парметр - определяет смещение между вершинами в массиве
		# Если вершины идут одна за другой, то смещение 0
		# Четвертый параметр - указатель на первую координату первой вершины в массиве
		glVertexPointer(3, GL_FLOAT, 0, self.vertexes)
		glNormalPointer(GL_FLOAT, 0, self.normals)
	#	glColorPointer(3, GL_FLOAT, 0, self.colors)

		# Рисуем данные массивов за один проход:
		# Первый параметр - какой тип примитивов использовать (треугольники, точки, линии и др.)
		# Второй параметр - начальный индекс в указанных массивах
		# Третий параметр - количество рисуемых объектов (в нашем случае это 3 вершины - 9 координат)
		glDrawArrays(GL_TRIANGLES, 0, len(self.vertexes)/3)
		glDisableClientState(GL_VERTEX_ARRAY)           # Отключаем использование массива вершин
		glDisableClientState(GL_NORMAL_ARRAY)           # Отключаем использование массива вершин
	#	glDisableClientState(GL_COLOR_ARRAY)

