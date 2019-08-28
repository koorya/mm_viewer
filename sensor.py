# This Python file uses the following encoding: utf-8
import numpy as np
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
from opengl_drawing_tools import *
from World_Components import *


#import Column

class Sensor(Mounted_Component):
	distance = None
	int_pos = None
	target_obj = None
	pos = None
	dir = None
	location_on_parent = np.eye(4)
	res_location = np.eye(4)

	def __init__(self, pos=(0., 0., 0.), dir=(0., 0., 1.)):
		self.set_pos(pos)
		self.set_dir(dir)
		self.reset_measure()
		self.target_obj = None
		pass
	


	def set_location_on_parent(self, matrix):
		self.location_on_parent = matrix
		
	def set_parent_matrix(self, par_matrix):
		self.res_location = np.dot(par_matrix, self.location_on_parent)
		self.pos = np.dot(self.res_location, np.array([0.0, 0.0, 0.0, 1.0]))		
		self.dir = np.dot(self.res_location, np.array([0.0, 0.0, 1.0, 1.0]))
		self.dir[:3] -= self.pos[:3];

	def set_pos(self, pos):
		self.pos = np.array([pos[0], pos[1], pos[2], 1.0])
	def set_dir(self, dir):
		self.dir = np.array([dir[0], dir[1], dir[2], 1.0])
	def set_pos_and_dir(self, pos=None, dir=None):
		if pos is not None:
			self.set_pos(pos)
		if dir is not None:
			self.set_pos(dir)
			
	def reset_measure(self):
		if self.target_obj is not None:
			self.target_obj.intersect_counter -= 1
			self.target_obj = None
			self.distance = None
			self.int_pos = None
			
	def measure(self, body):
		self.reset_measure()
		if body is not None:
			intersection = body.does_intersect_exist(self.pos, self.dir)
	#		print intersection
			if intersection is not None:
				self.target_obj = intersection.obj
				self.target_obj.intersect_counter += 1
				self.int_pos = intersection.pos
				self.distance = intersection.dist
			
	
	def draw(self):
		self.draw_intersect()
		
		
		treecolor = (1.0, 1.0, 1.0, 1.0)
		green_color = (0.0, 1.0, 0.0, 1.0)
		red_color = (1.0, 0.0, 0.0, 1.0)
		blue_color = (0.0, 0.0, 1.0, 1.0)
		yellow_color = (1.0, 0.8, 0.0, 1.0)
		pink_color = (1.0, 0.0, 0.5, 1.0)
		black_color = (0.0, 0.0, 0.0, 1.0)	
		glPushMatrix()	
		glLoadIdentity()
		glBegin(GL_LINES)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, black_color)	
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , blue_color)		
		glVertex3f(self.pos[0], self.pos[1], self.pos[2])
		if self.target_obj is not None:
			glVertex3f(self.int_pos[0], self.int_pos[1], self.int_pos[2])
		else:
			sens_end = self.pos + 10000.0*self.dir		
			glVertex3f(sens_end[0], sens_end[1], sens_end[2])
		glEnd()
		glPushMatrix()
		glTranslatef(self.pos[0], self.pos[1], self.pos[2])
		glutSolidSphere(10.0, 10, 10)
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , black_color)
		glPopMatrix()
		glPopMatrix()
		
	def draw_intersect(self):
		if self.target_obj is not None:
			glPushMatrix()
			glLoadIdentity()
			glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, black_color)
			glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (1.0, 0.0, 0.0, 1.0))	
			glTranslatef(self.int_pos[0], self.int_pos[1], self.int_pos[2])
			glutSolidSphere(50.0, 10, 10)
			glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))
			glPopMatrix()
	