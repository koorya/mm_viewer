# This Python file uses the following encoding: utf-8
import numpy as np
from Constants import *
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
from opengl_drawing_tools import *
from Column import *



class Joint:
	def __init__(self, color, Theta_f, Alpha, d_f, r, uplimit=100, downlimit = 0):
		self.uplimit = uplimit
		self.downlimit = downlimit
		self.color = color
		self.q = 0 # dergree or mm
		self.al = Alpha # radians
		self.r = r
		self.d_funct = d_f
		self.theta_funct = Theta_f
		self.H = np.eye(4)
		self.calcHMatrix()
	def __setattr__1(self, name, value):
		if name == "q":
			if value <= self.uplimit:
				if value >= self.downlimit:
					self.__dict__[name] = value
				else:
					self.__dict__[name] = self.downlimit
			else:
				self.__dict__[name] = self.uplimit
		else:
			self.__dict__[name] = value
	def calcHMatrix(self):
			C = np.cos
			S = np.sin
			Th = self.Theta()
			Al = self.al
			r = self.r
			d = self.d()
			self.H = np.array(	[[ C(Th)	, -S(Th)*C(Al)	, S(Th)*S(Al)	, r*C(Th)	],
								 [ S(Th)	, C(Th)*C(Al)	, -C(Th)*S(Al)	, r*S(Th)	],
								 [ 0		, S(Al)			, C(Al)			, 	d		],
								 [ 0		,		0		, 	0			,	1		]])
			pass
			
	def d(self):
		return self.d_funct(self.q)
	def Theta(self):
		return self.theta_funct(self.q)
	
	def draw(self):
		pass

class Prismatic_Joint(Joint):
	def draw(self):
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glutSolidCube(150*2)
		glutSolidCylinder(100, self.d(), 20, 20)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		glutWireCube(150*2)

class Revolute_Joint(Joint):
	def draw(self):
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glPushMatrix()
		glTranslatef(0, 0, -100)
		glutSolidCylinder(100*2, 100*2, 20, 20)
		glPopMatrix()
		glutSolidCylinder(100, self.d(), 20, 20)
		
		
class Manipulator:
	def __init__(self):
		global d_1, d_3_c, d_2_1, d_2_2, d_5, H
		
		
#		j1 = Revolute_Joint(green_color, Theta_f=lambda q: np.radians(90-q), Alpha=np.radians(90), d_f=lambda q: 473, r=0)
		j1 = Revolute_Joint(green_color, Theta_f=lambda q: np.radians(90-q), Alpha=np.radians(90), d_f=lambda q, d=d_1: d, r=0, uplimit = 110, downlimit = -200)
		j2 = Prismatic_Joint(red_color, Theta_f=lambda q: 0, 				Alpha=np.radians(-90), d_f=lambda q, d=(d_2_1+d_2_2): d+q, r=0, uplimit = 2920, downlimit = 0)
		j3 = Prismatic_Joint(blue_color, Theta_f=lambda q: 0, 				Alpha=np.radians(-0), d_f=lambda q, d=d_3_c: d+q, r=0, uplimit = 1777 , downlimit = 0)#1582
		j4 = Revolute_Joint(yellow_color, Theta_f=lambda q: np.radians(-q), 				Alpha=np.radians(90), d_f=lambda q: 0, r=0, uplimit = 100, downlimit = -100)
		j5 = Revolute_Joint(pink_color, Theta_f=lambda q: np.radians(q), 				Alpha=np.radians(-90), d_f=lambda q, d=d_5: d, r=0, uplimit = 0, downlimit = -135)		
		self.joints = [j1, j2, j3, j4, j5]
		self.calcMatrixes()
		self.target = 0
		self.target_conf = np.array([0, 0, 0, 0, 0])
		self.delta_config = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
		self.position = np.array([617, 0, H])
		
		self.link = Link((0., 0., 0.), (0.0, 0.0, 1.0), 180.0)
		self.sens_list = []
		self.active_field = None
	
	def append_sensor(self, sensor):
		self.sens_list.append(sensor)
	
	def calcMatrixes(self):
		for i in self.joints:
			i.calcHMatrix()
	def calc_kinematics(self):
		global mode
		ofset_matrix = np.array([	[1., 0., 0., self.position[0]],
										[0., 1., 0., self.position[1]],
										[0., 0., 1., self.position[2]],
										[0., 0., 0., 1.]])		

		end_point_matrix = ofset_matrix		
		j = 0

		for i in self.joints:
			j += 1
			end_point_matrix = np.dot(end_point_matrix, i.H)
		
	#	end_point_matrix = np.dot(end_point_matrix, ofset_matrix)
		
		if self.link is not None:
			self.link.set_parent_matrix(end_point_matrix)
		
		
		for cur_sens in self.sens_list:
			cur_sens.set_parent_matrix(end_point_matrix)
			cur_sens.measure(self.active_field)
		pass
	
	def get_sql_sensor_query(self, id=1):
		dist1 = -1
		if self.sens_list[0].distance is not None:
			dist1 = self.sens_list[0].distance
		dist2 = -1
		if self.sens_list[1].distance is not None:
			dist2 = self.sens_list[1].distance
		return "UPDATE sensors SET `sensor1`={0}, `sensor2`={1} WHERE (id = {2})".format(dist1, dist2, id)
	
	def draw_end(self):		
		if self.link is not None:
			self.link.draw()
		for cur_sens in self.sens_list:
			cur_sens.draw()

		
	def draw(self):

#		draw_grid(1000);
		glPushMatrix()
#		glLoadIdentity()
		glTranslatef(self.position[0], self.position[1], self.position[2])
		j = 0

		for i in self.joints:
			j += 1
#			print "matrix %i"%j
#			print i.H
			i.draw()
			#draw_grid(1000);
			cur_matrix = np.transpose(glGetFloatv(GL_MODELVIEW_MATRIX))
			cur_matrix = np.dot(cur_matrix, i.H)
			glLoadMatrixf(np.transpose(cur_matrix))

		#draw_grid(1000);

		self.draw_end()
		
		glPopMatrix()
	def set_pos(self, x_pos):
		self.position[0] = x_pos
		

	def setConfig(self, config):
		j = 0
		update_flag = 0
		for i in self.joints:
			if(i.q != config[j]):
				update_flag = 1
			i.q = config[j]
			j += 1
		if update_flag == 1:
			self.calcMatrixes()
			print "set config res:",self.getConfig()
			print "set congig res pos", self.getTarget()
	def getConfig(self):
		return np.array([self.joints[0].q,self.joints[1].q,self.joints[2].q,self.joints[3].q,self.joints[4].q])
	def getTarget(self):
		cur_vec = np.array([0, 0, 0, 1])
		for i in reversed(self.joints):
			cur_vec = np.dot(i.H, cur_vec)
		cur_vec += np.array([self.position[0], self.position[1], self.position[2], 0])
#		cur_vec += np.array([self.position[0], self.position[1], 0, 0])
		return np.array([cur_vec[0], -cur_vec[1], cur_vec[2], self.joints[4].q, 90 - self.joints[0].q - self.joints[3].q])
	def getTargetByConfig(self, conf_vect):
		rec_conf_vect = (self.joinst[0], self.joinst[1], self.joinst[2], self.joinst[3], self.joinst[4] )
		(self.joinst[0], self.joinst[1], self.joinst[2], self.joinst[3], self.joinst[4] ) = conf_vect
		self.calcMatrixes()
		target_pos = getTarget()
		(self.joinst[0], self.joinst[1], self.joinst[2], self.joinst[3], self.joinst[4] ) = rec_conf_vect
		self.calcMatrixes()
		return target_pos
	def getConfigByTarget(self, pos_vect):	# x, y, z, Theta, Phi
		global d_1, d_3_c, d_2_1, d_2_2, d_5
		
		a = d_5	
		x, y, z = pos_vect[0] - self.position[0], pos_vect[1]-self.position[1], pos_vect[2] - self.position[2]

		Theta = np.radians(pos_vect[3])
		Phi = np.radians(pos_vect[4])
		Phi = Phi
		#y = -y
		m = [x - a*np.sin(Phi), y-(a*np.cos(Phi))]
		psy1 = np.arctan2(m[1], m[0])
		psy2 = np.pi/2 - psy1 - Phi

		
		r = np.sqrt(m[0]*m[0]+m[1]*m[1])
#		print "r: %.2f"%r
		
		td2v = (r - d_2_1 - d_2_2)
#		td3v = (z - d_3_c - d_1)
		td3v = (z - d_3_c - d_1)
		return (np.rad2deg(psy1), td2v, td3v, np.rad2deg(psy2), np.rad2deg(Theta))

	def setTargetPosition(self, pos_vect):
		self.target_pos = pos_vect
		self.target = 1
		pass
	def setTargetConfig(self, conf_vect):
		self.target_conf = conf_vect
		self.target = 0
		self.delta_conf = (np.array(conf_vect) - self.getConfig())
		self.delta_conf /= 25.0
		pass
	def moveToTarget_pos(self):
		pass
	def moveToTarget_conf(self):
		if np.linalg.norm(self.target_conf - manip.getConfig(), 1) > 1:
			self.setConfig(self.getConfig()+self.delta_conf)
			return 1
		return 0

	def moveToTarget(self):
		#print self.getTarget()
		if self.target == 0:
			return self.moveToTarget_conf()
		elif self.target == 1:
			return self.moveToTarget_pos()		
		
		