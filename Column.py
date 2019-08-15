# This Python file uses the following encoding: utf-8
import numpy as np
import intersection
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
from opengl_drawing_tools import *




###################################################################################		
		
class Body():
	def __init__(self, pos, dir, angle, par_matrix = np.eye(4)):
		self.pos = np.array([pos[0], pos[1], pos[2], 1.0])

		self.dir = np.array([dir[0], dir[1], dir[2], 0.0])
		self.dir = self.dir / np.linalg.norm(self.dir)
		self.dir[3] = 1.0

		some_phi = np.rad2deg(np.arctan2(self.dir[1], self.dir[0]))
		some_theta = np.rad2deg(np.arccos(self.dir[2]))

		c = np.cos(np.deg2rad(-some_theta))
		d = np.sin(np.deg2rad(-some_theta))
		e = np.cos(np.deg2rad(some_phi))
		f = np.sin(np.deg2rad(some_phi))
		a = np.cos(np.deg2rad(angle))
		b = np.sin(np.deg2rad(angle))


		self.own_matrix = np.array([[a*c*e - b*f, -b*c*e-a*f, -d*e, self.pos[0]],
								[b*e+a*c*f, 	a*e - b*c*f, 	-d*f, self.pos[1]],
								[a*d,  -b*d, c, self.pos[2]],
								[0, 	0, 	0, 1]])

		self.own_shape_matrix = np.eye(4)
#		self.fw_matrix = np.eye(4)
##		self.fw_shape_matrix = np.eye(4)		
		
		"""
		self.own_matrix = np.array([[c*e, -f, -d*e, self.pos[0]],
								[c*f, 	e, 	-d*f, self.pos[1]],
								[d,  0, c, self.pos[2]],
								[0, 	0, 	0, 1]])
		"""

		
		self.children_list = []
		self.set_parent_matrix(par_matrix)	
		self.intersect = 0
		self.intersect_pos = 0
		self.intersect_dist = 0
		self.intersect_counter = 0#intersect counter
		self.set_shape()

		self.child_constr()
		
		
		
	def child_constr(self):
		pass
	def set_shape(self):
		pass
		
	def set_parent_matrix(self, par_matrix):
		self.fw_matrix = np.dot(par_matrix, self.own_matrix)
		self.inv_matrix = np.linalg.inv(self.fw_matrix)
		
		self.fw_shape_matrix = np.dot(self.fw_matrix, self.own_shape_matrix)
		self.inv_shape_matrix = np.linalg.inv(self.fw_shape_matrix)
		
		for i in self.children_list:
			i.set_parent_matrix(self.fw_matrix)
	
	def append_child(self, child):
		self.children_list.append(child)
		child.set_parent_matrix(self.fw_matrix)
		
	def draw_self(self):
		pass
		
		
	def draw_children(self):
		for i in self.children_list:
			i.draw()

	
	def draw(self):
		if self.intersect_counter > 0:
			glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.5, 0.0, 1.0))	
		else:
			glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		self.draw_self()
		self.draw_children()
		
	def shape_intersect_finder(self, pos, dir):
		return intersection.get_intersect_cube(pos, dir)
		
	def does_intersect_exist(self, ray_pos, ray_dir):
		intersection = None
		sens_start_ = np.dot(self.inv_shape_matrix, np.array([ray_pos[0], ray_pos[1], ray_pos[2], 1.0]))
	
		sens_dir_ = np.dot(self.inv_shape_matrix, np.array([ray_dir[0], ray_dir[1], ray_dir[2], 1.0]))
		ofset_vect = np.dot(self.inv_shape_matrix, [0.0, 0.0, 0.0, 1.0])
		sens_dir_ -= ofset_vect;
		
		intersection = self.shape_intersect_finder(sens_start_, sens_dir_)
		if intersection is not None:
#			print self
			intersection.obj = self
			intersect_cube = intersection.pos
			self.intersect_pos = np.dot(self.fw_shape_matrix, np.array([intersect_cube[0], intersect_cube[1], intersect_cube[2], 1.0]))
			intersection.pos = self.intersect_pos
			self.intersect_dist = np.linalg.norm([self.intersect_pos[0]-ray_pos[0], self.intersect_pos[1]-ray_pos[1], self.intersect_pos[2]-ray_pos[2]])
			intersection.dist = self.intersect_dist
#			print "dist_real: ", self.intersect_dist, "int_obj: ", intersection
			
		for i in self.children_list:
			child_int_tmp = i.does_intersect_exist(ray_pos, ray_dir)
			if child_int_tmp is not None:
				if intersection is None:
					intersection = child_int_tmp
				else:
					if intersection.dist > child_int_tmp.dist:
						intersection = child_int_tmp

			
		return intersection

class BodyCil(Body):

	"""
		glPushMatrix()
		glTranslatef(0.0, 0.0, -0.5)
		glutSolidCylinder(0.5, 1, 20, 20)
		glPopMatrix()
	"""		
	def shape_intersect_finder(self, pos, dir):
		return intersection.get_intersect_cil(pos, dir)

	
class Floor(Body):
	def child_constr(self):
		xsize = 2
		ysize = 4
		for x in range(xsize):
			for y in range(ysize):
				self.append_child(Column(((xsize/2 - x)*3500-1750, (ysize/2 - y)*3500-1750, 0), (0.0, 0.0, 1.0), 0.0))
	
		
	def draw_self(self):
		glPushMatrix()
		glLoadMatrixf(np.transpose(self.fw_shape_matrix))	

		floor_size = 7000.0	
		glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.0, 0.0, 0.0, 1.0))	
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
	#	glBegin(GL_QUADS)
		glBegin(GL_LINES)
		glNormal3f(0.0, 0.0, 1.0);
		glVertex3f(-floor_size, -floor_size, -200.0)
		glVertex3f(-floor_size, floor_size,  -200.0)
		glVertex3f(floor_size, floor_size,  -200.0)
		glVertex3f(floor_size, -floor_size,  -200.0)
		glEnd()
		glPopMatrix()
	def does_intersect_exist(self, ray_pos, ray_dir):
		intersection = None
		for i in self.children_list:
			child_int_tmp = i.does_intersect_exist(ray_pos, ray_dir)
			if child_int_tmp is not None:
				if intersection is None:
					intersection = child_int_tmp
				else:
					if intersection.dist > child_int_tmp.dist:
						intersection = child_int_tmp

		return intersection	
	
class Field(Floor):
	def child_constr(self):
		pass
	def draw_self(self):
		pass
	
	
class FilledFloor(Floor):
	def child_constr(self):
		xsize = 2
		ysize = 4
		for x in range(xsize):
			for y in range(ysize):
				self.append_child(Column(((xsize/2 - x)*3500-1750, (ysize/2 - y)*3500-1750, 0), (0.0, 0.0, 1.0), 0.0))
		
		
		
		s = np.sin(np.deg2rad(27.0))
		c = np.cos(np.deg2rad(27.0))
		
		rot_a = np.array([	[  1,    0.,   0.,  0.],
							[  0.,   c,   -s,  	0.],
							[  0.,   s,    c,   0.],
							[  0.,   0.,   0.,  1.]])		
		dira = np.dot(rot_a, np.array([0.0, 0.0, 1.0, 1.0]))
		rot_b = np.array([	[  c,    0,   -s,  0.],
							[  0,   1,   0,  	0.],
							[  s,   0,    c,   0.],
							[  0.,   0.,   0.,  1.]])		
		dirb = np.dot(rot_b, np.array([0.0, 0.0, 1.0, 1.0]))
		
		for x in range(xsize):
			for y in range(ysize-1):
				self.append_child(LinkSloped(((xsize/2 - x)*3500-1750, (ysize/2 - y)*3500-4275, 1390), (dira[0], dira[1], dira[2]), 180.0))
				self.append_child(LinkSloped(((xsize/2 - x)*3500-1750, (ysize/2 - y)*3500-2725, 1390), (dira[0], -dira[1], dira[2]), 180.0))
		
		for x in range(xsize-1):
			for y in range(ysize):
				ofset = 780
				self.append_child(LinkSloped(((xsize/2 - x)*3500-1750-ofset-193, (ysize/2 - y)*3500-1750, 1390), (-dirb[0], dirb[1], dirb[2]), 180.0))
				self.append_child(LinkSloped(((xsize/2 - x)*3500-3500-ofset, (ysize/2 - y)*3500-1750, 1390), (dirb[0], dirb[1], dirb[2]), 180.0))
		
		for x in range(xsize):
			for y in range(ysize-1):
				self.append_child(Link(((xsize/2 - x)*3500-1750, (ysize/2 - y)*3500-3500, 3000-125), (0.0, 1.0, 0.0), 180.0))
		for x in range(xsize-1):
			for y in range(ysize):
				self.append_child(Link(((xsize/2 - x)*3500-3500, (ysize/2 - y)*3500-1750, 3000-125), (1.0, 0.0, 0.0), 180.0))



class Link(BodyCil):
	def child_constr(self):
		self.append_child(LinkEndBond((0.0, 0.0, 1210.0), (0.0, 0.0, 1.0), 0.0))
		self.append_child(LinkEndBond((0.0, 0.0, -1210.0), (0.0, 0.0, -1.0), 0.0))
		self.append_child(LinkMiddleBond((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), 0.0))

		
	def set_shape(self):
		"""
		self.own_shape_matrix = np.eye(4)
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		glScalef(127, 127, 2420)
		self.own_shape_matrix = np.transpose(glGetFloatv(GL_MODELVIEW_MATRIX))
		glPopMatrix()
		"""
		self.own_shape_matrix = np.array([[127.,   0.,   0.,   0.],
											[  0., 127.,   0.,   0.],
											[  0.,   0.,   2420.,   0.],
											[  0.,   0.,   0.,  1.]])
		
		
		pass
	def draw_self(self):
		glPushMatrix()
		glLoadMatrixf(np.transpose(self.fw_shape_matrix))	
#		glRotatef(45, 0, 0, 1)
#		glScalef(450, 450, 3000)
#		glTranslatef(0, 0, 0.5)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.25, 0.25, 0.25, 0.9))
		
		glPushMatrix()
		glTranslatef(0.0, 0.0, -0.5)
		glutSolidCylinder(0.5, 1, 20, 20)
		glPopMatrix()
		
#		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
#		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
#		glutWireCube(1.0)
		
		glPopMatrix()

class LinkSloped(Link):	
	def child_constr(self):	
		self.append_child(LinkEndBond((0.0, 0.0, 1210.0), (0.0, 0.0, 1.0), 0.0))
		self.append_child(LinkEndBond((0.0, 0.0, -1210.0), (0.0, 0.0, -1.0), 0.0))
		
				
		
		
class Column(Body):
	
	def child_constr(self):
		"""
		self.append_child(Petal((450.0, 0.0, 2800.0), (0.0, 0.0, 1.0), 0.0))
		self.append_child(Petal((400.0, 0.0, 2700.0), (1.0, 0.0, 1.0), 0.0))
		self.append_child(Petal((-450.0, 0.0, 2800.0), (0.0, 0.0, -1.0), 0.0))
		self.append_child(Petal((-400.0, 0.0, 2700.0), (1.0, 0.0, -1.0), 0.0))

		self.append_child(Petal((0.0, 450.0, 2800.0), (0.0, 0.0, 1.0), -90.0))
		self.append_child(Petal((0.0, 400.0, 2700.0), (0.0, 1.0, 1.0), 0.0))

		self.append_child(Petal((0.0, -450.0, 2800.0), (0.0, 0.0, -1.0), 90.0))
		self.append_child(Petal((0.0, -400.0, 2700.0), (0.0, 1.0, -1.0), 0.0))
	
		self.append_child(Petal((0.0, -400.0, 200.0), (0.0, 0.0, 1.0), 90.0))
		"""
		self.append_child(Bond((258.0, 0.0, 2950.0), (0.0, 0.0, 1.0), 0.0))
		self.append_child(Bond((-258.0, 0.0, 2950.0), (0.0, 0.0, 1.0), 180.0))
		self.append_child(Bond((0.0, 258.0, 2950.0), (0.0, 0.0, 1.0), 90.0))
		self.append_child(Bond((0.0, -258.0, 2950.0), (0.0, 0.0, 1.0), -90.0))		


	def set_shape(self):
		self.own_shape_matrix = np.array([[ 3.182e+02, -3.182e+02,  0.000e+00,  0.000e+00],
											[ 3.182e+02,  3.182e+02,  0.000e+00,  0.000e+00],
											[ 0.000e+00,  0.000e+00,  3.000e+03,  1.500e+03],
											[ 0.000e+00,  0.000e+00,  0.000e+00,  1.000e+00]])
		pass

	def draw_self(self):
		glPushMatrix()
		glLoadMatrixf(np.transpose(self.fw_shape_matrix))	
#		glRotatef(45, 0, 0, 1)
#		glScalef(450, 450, 3000)
#		glTranslatef(0, 0, 0.5)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.15, 0.15, 0.15, 0.9))
		

		
		glutSolidCube(1.0)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		glutWireCube(1.0)
		glPopMatrix()
		
class Bond(Body):
	def child_constr(self):
		self.append_child(PetalHor((0.0, 0.0, -75.0), (0.0, 0.0, 1.0), 0.0))

		s = np.sin(np.deg2rad(-90+27.0))
		c = np.cos(np.deg2rad(-90+27.0))
		
		rot_a = np.array([[c,   0.,   -s,   0.],
						[  s, 1.,   0.,   0.],
						[  0.,   0.,  c,   0.],
						[  0.,   0.,   0.,  1.]])		
		dir = np.dot(rot_a, np.array([0.0, 0.0, 1.0, 1.0]))
		self.append_child(PetalSloped((0.0, 0.0, -158.0), (dir[0], dir[1], dir[2]), 0.0))

class LinkEndBond(Body):
	def child_constr(self):
		self.append_child(PetalHor((10.0, 0.0, 0.0), (1.0, 0.0, 0.0), 180.0))
		self.append_child(PetalHor((-10.0, 0.0, 0.0), (1.0, 0.0, 0.0), 180.0))
		
class LinkMiddleBond(Body):
	def child_constr(self):
	
		s = np.sin(np.deg2rad(-90+27.0))
		c = np.cos(np.deg2rad(-90+27.0))
		
		rot_a = np.array([[c,   0.,   -s,   0.],
						[  s, 1.,   0.,   0.],
						[  0.,   0.,  c,   0.],
						[  0.,   0.,   0.,  1.]])		
		dir = np.dot(rot_a, np.array([0.0, 0.0, 1.0, 1.0]))
	
		self.append_child(LinkPetalSloped((0.0, 0.0, 0.0), (dir[0], dir[1], dir[2]), 180.0))
		self.append_child(LinkPetalSloped((0.0, 0.0, 0.0), (-dir[0], dir[1], dir[2]), 180.0))




def draw_grid(size):
	global red_color, green_color, blue_color

	glBegin(GL_LINES)
	glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , red_color)		
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, red_color)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(size, 0.0, 0.0)
	glEnd()
	glBegin(GL_LINES)
	glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , green_color)	
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, green_color)	
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, size, 0.0)
	glEnd()
	glBegin(GL_LINES)
	glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , blue_color)	
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, blue_color)	
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, size)
	glEnd()
	glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , black_color)	


	
class Petal(Body):
	def set_shape(self):
		self.own_shape_matrix = np.array([[300.,   0.,   0.,   0.],
											[  0., 150.,   0.,   0.],
											[  0.,   0.,   8.,   0.],
											[  0.,   0.,   0.,  1.]])
		pass
	def draw_self(self):
		glPushMatrix()

		glLoadMatrixf(np.transpose(self.fw_shape_matrix))	

#		glScalef(300, 150, 8)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.3, 0.1, 0.1, 0.9))		
		glutSolidCube(1.0)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		glutWireCube(1.0)
		glPopMatrix()
class PetalHor(Petal):
	def set_shape(self):
		self.own_shape_matrix = np.array([[200.,   0.,   0.,   0.],
											[  0., 120.,   0.,   0.],
											[  0.,   0.,   8.,   0.],
											[  0.,   0.,   0.,  1.]])
		self.own_shape_matrix = np.dot(self.own_shape_matrix, np.array([[1.0,   0.,   0.,   0.5],
																		[  0., 1.,   0.,   0.],
																		[  0.,   0.,   1.,   0.],
																		[  0.,   0.,   0.,  1.]]))	
		pass
class PetalSloped(Petal):
	def set_shape(self):
		self.own_shape_matrix = np.eye(4)
												
		self.own_shape_matrix = np.dot(self.own_shape_matrix, np.array([[393.0,   0.,   0.,   0.],
																		[  0., 120.,   0.,   0.],
																		[  0.,   0.,   8.,   0.],
																		[  0.,   0.,   0.,  1.]]))

		self.own_shape_matrix = np.dot(self.own_shape_matrix, np.array([[1.0,   0.,   0.,   0.5],
																		[  0., 1.,   0.,   0.],
																		[  0.,   0.,   1.,   0.],
																		[  0.,   0.,   0.,  1.]]))
	
		
		pass
		
class LinkPetalSloped(Petal):
	def set_shape(self):
		self.own_shape_matrix = np.eye(4)
												
		self.own_shape_matrix = np.dot(self.own_shape_matrix, np.array([[269.0,   0.,   0.,   0.],
																		[  0., 120.,   0.,   0.],
																		[  0.,   0.,   8.,   0.],
																		[  0.,   0.,   0.,  1.]]))

		self.own_shape_matrix = np.dot(self.own_shape_matrix, np.array([[1.0,   0.,   0.,   0.5],
																		[  0., 1.,   0.,   0.],
																		[  0.,   0.,   1.,   0.],
																		[  0.,   0.,   0.,  1.]]))
	
		
		pass		