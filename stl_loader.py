from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
from opengl_drawing_tools import *
from World_Components import *


class Loaded_Model(Mounted_Component):
	model = []
	color = (0.25, 0.35, 0.25, 0.9)
	
	def load_model(self, file_name = 'models/test.stl'):
		f = open(file_name)
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
					
				
	def draw(self):
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glBegin(GL_TRIANGLES)
		for i in self.model:
			glNormal3f(i[0][0], i[0][1], i[0][2])
			glVertex3f(i[1][0], i[1][1], i[1][2])
			glVertex3f(i[2][0], i[2][1], i[2][2])
			glVertex3f(i[3][0], i[3][1], i[3][2])
		glEnd()

