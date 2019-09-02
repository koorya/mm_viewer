# This Python file uses the following encoding: utf-8
import numpy as np
from Constants import *
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
from opengl_drawing_tools import *
from Column import *
import sensor
from World_Components import *

from stl_loader import *


class Joint(Hanger_Component):
	def __init__(self, color, Theta_f, Alpha, d_f, r, uplimit=100, downlimit = 0):
		self.uplimit = uplimit
		self.downlimit = downlimit
		self.color = color
		self.q = 0 # degree or mm
		self.al = Alpha # radians
		self.r = r
		self.d_funct = d_f
		self.theta_funct = Theta_f
		self.H = np.eye(4)
		self.resMatrix = np.eye(4)
		self.parent = None
		self.calcHMatrix()
		self.model = None
		self.model_end = None
		
		
	def set_parent_matrix(self, par_matrix):
		self.resMatrix = np.dot(par_matrix, self.H)
			
	
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
	def draw_(self):
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glutSolidCube(150*2)
		glutSolidCylinder(100, self.d(), 20, 20)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		glutWireCube(150*2)
	def draw(self):
		draw_grid(1000)
		
		
class Pusher_Joint(Prismatic_Joint):
	def draw_(self):
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glutSolidCube(15*2)
		glutSolidCylinder(10, self.d(), 20, 20)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		glutWireCube(15*2)

class Static_Joint(Joint):
	def draw_(self):
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glutSolidCylinder(20, self.d(), 20, 20)

class Revolute_Joint(Joint):
	def draw(self):
		draw_grid(1000)
	def draw_(self):
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glPushMatrix()
		glTranslatef(0, 0, -100)
		glutSolidCylinder(100*2, 100*2, 20, 20)
		glPopMatrix()
		glutSolidCylinder(100, self.d(), 20, 20)

class Tower_Revolute_Joint(Revolute_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
	
		if self.model_end is None:	
			self.model_end = []	
			self.model_end.append(Loaded_Model("models/Component18.stl", "#161614")) # рама 
			self.model_end.append(Loaded_Model("models/Component31.stl", "#747061")) #шкаф
			# self.model_end.append(Loaded_Model("models/Body1.stl", "#957000"))		
			
		glPushMatrix()
		glRotatef(90, 0, 0, 1)
		glTranslatef(0.0, 0.0, -428.0)
		for model in self.model:
			model.draw()

		glMultMatrixf(np.transpose(self.H))	
		glRotatef(-90, 1, 0, 0)
#		glRotatef(90, 0, 0, 1)
		for model in self.model_end:
			model.draw()
		
		glPopMatrix()
		
class Kareta_Prismatic_Joint(Prismatic_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
			
		if self.model_end is None:	
			self.model_end = []	
			self.model_end.append(Loaded_Model("models/Component1_reduce.stl", "#957000"))	

			
		glPushMatrix()
#		glRotatef(90, 0, 0, 1)

		for model in self.model:
			model.draw()

		glMultMatrixf(np.transpose(self.H))	
#		glRotatef(-90, 1, 0, 0)
		glRotatef(90, 0, 0, 1)
		glTranslatef(0.0, 0.0, -428.0)
		# draw_grid(1000)
		for model in self.model_end:
			model.draw()
		
		glPopMatrix()

class Jack_Prismatic_Joint(Prismatic_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
			
		if self.model_end is None:	
			self.model_end = []	
			self.model_end.append(Loaded_Model("models/Component129.stl", "#6F9416"))	

			
		glPushMatrix()
#		glRotatef(90, 0, 0, 1)

		for model in self.model:
			model.draw()

		glMultMatrixf(np.transpose(self.H))	
		glRotatef(-90, 1, 0, 0)
		glRotatef(90, 0, 0, 1)
		glTranslatef(-3000.0, 0.0, 0.0)
		# draw_grid(1000)
		for model in self.model_end:
			model.draw()
		
		glPopMatrix()
class Pantograph_Prismatic_Joint(Prismatic_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
			
		# glPushMatrix()
		# for model in self.model:
			# model.draw()
		# glPopMatrix()

		glPushMatrix()
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glTranslatef(0.0, -428.0, 0.0)
		glScalef(600.0, 2500.0, self.d()-350)
		glTranslatef(0.0, -0.5, 0.5)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (1.*149/255, 1.*112/255, 0.0, 1.0))
		glutSolidCube(1)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		glutWireCube(1)
		glPopMatrix()

class Column_Pantograph_Prismatic_Joint(Prismatic_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
			
		# glPushMatrix()
		# for model in self.model:
			# model.draw()
		# glPopMatrix()

		glPushMatrix()
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
		glTranslatef(0.0, -428.0, 0.0)
		glTranslatef(0.0, -200.0, -350)
		glScalef(400.0, 1300.0, self.d()+600)
		glTranslatef(0.0, -0.7, 0.5)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (1.*149/255, 1.*112/255, 0.0, 1.0))
		glutSolidCube(1)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		glutWireCube(1)
		glPopMatrix()
		
class link_rotation_Revolute_Joint(Revolute_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
			self.model.append(Loaded_Model("models/Component26.stl", "#1E027D"))

		glPushMatrix()
		glRotatef(180, 0, 0, 1)
#		draw_grid(1000)
		glPopMatrix()
		glPushMatrix()
		glRotatef(-90, 1, 0, 0)
		glRotatef(90, 0, 0, 1)
		glTranslatef(-389.688, -17.159, 0.0)
		for model in self.model:
			model.draw()
		glPopMatrix()
		
		

class wrist_Revolute_Joint(Revolute_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
			self.model.append(Loaded_Model("models/Component19.stl", "#957000"))

		glPushMatrix()
		glRotatef(180, 0, 0, 1)
#		draw_grid(1000)
		glPopMatrix()
		glPushMatrix()
		glRotatef(90, 0, 0, 1)
		glTranslatef(0.0, 0.0, -68.0)
		for model in self.model:
			model.draw()
		glPopMatrix()

class link_carige_Prismatic_Joint(Prismatic_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
			self.model.append(Loaded_Model("models/Component21.stl", "#051520"))

		glPushMatrix()
		glRotatef(180, 0, 0, 1)
#		draw_grid(1000)
		glPopMatrix()
		glPushMatrix()
		glRotatef(-90, 0, 0, 1)
		glTranslatef(-639.0, 0.0, -428.0)
		glRotatef(180, 0, 0, 1)
		for model in self.model:
			model.draw()
		glPopMatrix()
		
class column_carige_Prismatic_Joint(Prismatic_Joint):
	def draw(self):
		if self.model is None:	
			self.model = []
			self.model.append(Loaded_Model("models/Component20.stl", "#051520"))


		# draw_grid(1000)

		if self.model_end is None:	
			self.model_end = []
			self.model_end.append(Loaded_Model("models/Component40.stl", "#2D728C"))


		# draw_grid(1000)

		glPushMatrix()
		glRotatef(90, 0, 0, 1)
		glRotatef(180, 0, 1, 0)
		glTranslatef(-780.0, 0.0, -428.0)
#		glTranslatef(0.0, 0.0, 500.0)
		for model in self.model:
			model.draw()
		glPopMatrix()	

		glPushMatrix()
		glMultMatrixf(np.transpose(self.H))
		glRotatef(90, 1, 0, 0)
		glRotatef(90, 0, 0, 1)
		glTranslatef(-780.0, 0.0, 500.0)
#		glTranslatef(0.0, 0.0, 500.0)
		for model in self.model_end:
			model.draw()
		glPopMatrix()	
		

class Hanger_Joint(Joint):
	is_active = 0
	hanged_obj = Mounted_Component()
	type = "empty"
	def pick_up(self):
		self.is_active = 1
	def drop(self):
		if self.is_active == 0:
			return
		self.is_active = 0
		matrix = self.hanged_obj.resMatrix
		print matrix
		pos = np.transpose(matrix)[3:][0][:3]
		print pos
		dir = np.transpose(matrix)[2:3][0][:3]
		print dir
		angle = -np.rad2deg(np.arctan2(matrix[0][0], matrix[1][0]))
		print angle
		conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', 'MM')		
		cursor = conn.cursor()
		query_str = "INSERT INTO Links (`type`, `pos_x`, `pos_y`, `pos_z`, `dir_x`, `dir_y`, `dir_z`, `angle`) VALUES ('{7}', {0}, {1}, {2}, {3}, {4}, {5}, {6})".format(pos[0], pos[1], pos[2], dir[0], dir[1], dir[2], angle, self.type)
		cursor.execute(query_str)
		conn.commit()
		conn.close()
		
	def switch_state(self):
		if self.is_active == 1:
			self.drop()
		else:
			self.pick_up()
			
	def draw(self):
		if self.is_active == 1:
			self.hanged_obj.draw()
		
	def set_parent_matrix(self, par_matrix):
		self.resMatrix = par_matrix
		self.hanged_obj.set_parent(self)		
		
	
	
class column_hanger_Joint(Hanger_Joint):
	hanged_obj = Column((0, 2550, 450/1.4), (0.0, -1.0, 0.0), 0.0)
	type = "column"

class link_hanger_Joint(Hanger_Joint):
	hanged_obj = Link((0., 0., 0.), (0.0, 0.0, 1.0), 180.0)
	type = "diagonal"

		
		
class Manipulator:

	sens_list = []

	def __init__(self):
		global d_1, d_3_c, d_2_1, d_2_2, d_5, H
		
		
		self.append_joints()
		self.calcMatrixes()
		self.target = 0
		self.target_conf = np.array([0, 0, 0, 0, 0])
		self.delta_config = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
#		self.position = np.array([617, 0, H])
		self.position = np.array([0, 0, 0])
		
		
		
		self.active_field = None
		
	def append_joints(self):
		jack = Jack_Prismatic_Joint(green_color, Theta_f=lambda q: np.radians(90), Alpha=np.radians(90), d_f=lambda q, d=0: q, r=0)
		kareta = Kareta_Prismatic_Joint(green_color, Theta_f=lambda q: np.radians(0), Alpha=np.radians(-90), d_f=lambda q, d=0: q, r=0)
		
		tower = Tower_Revolute_Joint(green_color, Theta_f=lambda q: np.radians(-q), Alpha=np.radians(90), d_f=lambda q, d=d_1: d, r=0, uplimit = 110, downlimit = -200)
		link_pantograph = Pantograph_Prismatic_Joint(red_color, Theta_f=lambda q: 0, 				Alpha=np.radians(-90), d_f=lambda q, d=(d_2_1+d_2_2): d+q, r=0, uplimit = 2920, downlimit = 0)
		link_carige = link_carige_Prismatic_Joint(blue_color, Theta_f=lambda q: 0, 				Alpha=np.radians(-0), d_f=lambda q, d=d_3_c: d+q, r=0, uplimit = 1777 , downlimit = 0)#1582
		wrist = wrist_Revolute_Joint(yellow_color, Theta_f=lambda q: np.radians(-q), 				Alpha=np.radians(90), d_f=lambda q: 0, r=0, uplimit = 100, downlimit = -100)
		link_rotation = link_rotation_Revolute_Joint(pink_color, Theta_f=lambda q: np.radians(q), 				Alpha=np.radians(-90), d_f=lambda q, d=d_5: d, r=0, uplimit = 0, downlimit = -135)		

		column_pantograph = Column_Pantograph_Prismatic_Joint(red_color, Theta_f=lambda q: 0, 				Alpha=np.radians(90), d_f=lambda q, d=780: -d-q, r=0, uplimit = 2920, downlimit = 0)
		column_carrige = column_carige_Prismatic_Joint(yellow_color, Theta_f=lambda q: np.radians(0), 				Alpha=np.radians(90), d_f=lambda q, d=(1021.5): d-q, r=0, uplimit = 2920, downlimit = 0)
		
		
		column_handle = column_hanger_Joint(yellow_color, Theta_f=lambda q: np.radians(0), 				Alpha=np.radians(0), d_f=lambda q: 0, r=0)
		


		sens1 = sensor.Sensor() 
		sens1.set_location_on_parent(np.array([	[1., 0., 0., 0.],
												[0., 0., -1., 153.],
												[0., 1., 0., 1321.],
												[0., 0., 0., 1.]]))


		sens2 = sensor.Sensor() 
		sens2.set_location_on_parent(np.array([	[1., 0., 0., 0.],
												[0., 0., -1., 153.],
												[0., 1., 0., -1321.],
												[0., 0., 0., 1.]]))

		link_hanger = link_hanger_Joint(yellow_color, Theta_f=lambda q: np.radians(0), Alpha=np.radians(0), d_f=lambda q: 0, r=0)
		

#		some_model = Loaded_Model()
#		some_model.load_model("models/Component5.stl")

		stik_midle = Loaded_Model("models/Component5_3.stl", "#155713")


		stik_left = Loaded_Model("models/Component5_1.stl", "#2D728C")

		
		stik_right = Loaded_Model("models/Component5_2.stl", "#2D728C")

		  


		self.joints_tree = 	[
							jack,
								[kareta,
									[tower,
										[link_pantograph, 
											[link_carige, 
												[wrist, 
													[link_rotation,
														[sens1],
														[sens2],
														[link_hanger],
														[stik_midle],
														[stik_left],
														[stik_right],
														
													]
												]
											]
										],
										
										[column_pantograph, 
											[column_carrige, 
												[column_handle]#, [Column((0, 2550, 450/1.4), (0.0, -1.0, 0.0), 0.0)]]
											]
										]
									]
								]
							]
		
		self.driven_joints = [
								jack,
								kareta,
								tower, 
								link_pantograph, 
								link_carige,
								wrist, 
								link_rotation, 
								column_pantograph, 
								column_carrige
							]
		self.driven_joints_name = """jack
								kareta
								tower
								link_pantograph
								link_carige
								wrist
								link_rotation
								column_pantograph
								column_carrige""".split()					
		
		self.hanger_joints = [link_hanger, column_handle]
		
		def tree_to_list(root, line_list, parent, class_name):
			
			for i in root:
				if not isinstance(i, list):
					if isinstance(i, class_name):
						line_list.append(i)
					i.set_parent(parent)
					parent = i
				else:
					tree_to_list(i, line_list, parent, class_name)
			return line_list[:]
		
		self.all_elements = tree_to_list(self.joints_tree, [], None, World_Component)
		self.joints = tree_to_list(self.joints_tree, [], None, Joint)
		
		self.sens_list = tree_to_list(self.joints_tree, [], None, sensor.Sensor)
	#	for i in self.joints:
	#		print i.parent, i
	#	exit()
	
	#	self.append_sensor(sens1)
	#	self.append_sensor(sens2)
		
		
	def append_sensor(self, sensor):
		self.sens_list.append(sensor)
		
	def setActiveField(self, field):
		for cur_sens in self.sens_list:
			cur_sens.reset_measure()		
		self.active_field = field
	
	def calcMatrixes(self):

		for i in self.joints:
			i.calcHMatrix()
				
			
	def calc_kinematics(self):
		global mode
		ofset_matrix = np.array([		[1., 0., 0., self.position[0]],
										[0., 1., 0., self.position[1]],
										[0., 0., 1., self.position[2]],
										[0., 0., 0., 1.				 ]])		

		end_point_matrix = ofset_matrix		
		j = 0
		self.joints[0].resMatrix = np.dot(ofset_matrix, self.joints[0].H)
		for i in self.all_elements:
			j += 1
			i.set_parent()
		#	end_point_matrix = np.dot(end_point_matrix, i.H)
		
	#	end_point_matrix = np.dot(end_point_matrix, ofset_matrix)
		
	#	if self.link is not None:
		#	self.link.set_parent_matrix(end_point_matrix)
				
		for cur_sens in self.sens_list:
			cur_sens.measure(self.active_field)

	def get_sql_sensor_query(self, id=1):
		dist1 = -1
		if self.sens_list[0].distance is not None:
			dist1 = self.sens_list[0].distance
		dist2 = -1
		if self.sens_list[1].distance is not None:
			dist2 = self.sens_list[1].distance
		return "UPDATE sensors SET `sensor1`={0}, `sensor2`={1} WHERE (id = {2})".format(dist1, dist2, id)
	
	def draw_end(self):		

		pass
#		if self.link is not None:
#			self.link.draw()
	#	for cur_sens in self.sens_list:
	#		cur_sens.draw()

		
	def draw(self):
	

#		draw_grid(1000);
		glPushMatrix()

		glPushMatrix()
		glTranslatef(self.position[0], self.position[1], self.position[2])
		self.joints[0].draw()
		glPopMatrix()

		for i in self.all_elements:
			if isinstance(i.parent, Joint):
				glPushMatrix()
				cur_matrix = np.transpose(glGetFloatv(GL_MODELVIEW_MATRIX))
				cur_matrix = np.dot(cur_matrix, i.parent.resMatrix)
				glLoadMatrixf(np.transpose(cur_matrix))
				i.draw()

				#draw_grid(1000);
				glPopMatrix()
			

		#draw_grid(1000);

		self.draw_end()
		
		glPopMatrix()
		
		
	def set_pos(self, x_pos):
		self.position[0] = x_pos
		

	def setConfig(self, config):
			
		for idx, val in enumerate(self.driven_joints):
			if len(config)>idx:
				val.q = config[idx]
				val.calcHMatrix()

			
	def getConfig(self):

		return list(joint.q for joint in self.driven_joints)
		
		
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
		
