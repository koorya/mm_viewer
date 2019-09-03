# This Python file uses the following encoding: utf-8
import numpy as np
import MySQLdb
import intersection
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
from opengl_drawing_tools import *
from World_Components import *
import sys


###################################################################################		
		
class Body(Hanger_Component):
	def __init__(self, pos, dir, angle, par_matrix = np.eye(4)):
		self.v_list = [[], [], []]
		self.vertexes = []
		self.normals = []
		self.colors = []
		self.program = None
		
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
	#	self.resMatrix = np.eye(4)
		self.fw_shape_matrix = np.eye(4)		
		
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
		self.resMatrix = np.dot(par_matrix, self.own_matrix)
		self.inv_matrix = np.linalg.inv(self.resMatrix)
		
		self.fw_shape_matrix = np.dot(self.resMatrix, self.own_shape_matrix)
		self.inv_shape_matrix = np.linalg.inv(self.fw_shape_matrix)
		
		for i in self.children_list:
			i.set_parent_matrix(self.resMatrix)
	
	def append_child(self, child):
		self.children_list.append(child)
		child.set_parent_matrix(self.resMatrix)
		
	def draw_self(self):
		return [[], [], []]
		pass
		
		
	def draw_children(self):
		vertex_list = [[], [], []]
		for i in self.children_list:
			ret = i.draw()
			vertex_list[0] += ret[0]
			vertex_list[1] += ret[1]
			vertex_list[2] += ret[2]
		return vertex_list

	
	def draw(self):
		print "MAIN DRAW"
		if self.intersect_counter > 0:
			glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.5, 0.0, 1.0))	
		else:
			glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
		vertex_list = self.draw_self()
		ret = self.draw_children()
		vertex_list[0] += ret[0]
		vertex_list[1] += ret[1]
		vertex_list[2] += ret[2]
		return vertex_list
	
	def set_vertex_list(self, v_list):
		
		
#		orig_stdout = sys.stdout
#		f = open('log.txt', 'w')
#		sys.stdout = f

		a = np.array(v_list[0]).ravel()
		print "start a"
		print a
		print "end a"
		print "start v_list[0]"
		print np.array(v_list[0])
		print "endv_list[0]"
#		sys.stdout = orig_stdout
#		f.close()
		print a.reshape(-1, 4)
#		exit()
		b = np.array(v_list[1]).ravel()
		c = np.array(v_list[2]).ravel()
		self.vertexes = np.transpose(np.transpose(a.reshape(-1, 4))[:-1]).ravel()
		self.normals  =	np.transpose(np.transpose(b.reshape(-1, 4))[:-1]).ravel()
		self.colors = np.transpose(np.transpose(c.reshape(-1, 4))[:-1]).ravel()


	
	def draw_vertex_list(self):
		
		if len(self.colors)<1 :
			return

		if self.program is None:
			try:
				vertex2 = create_shader(GL_VERTEX_SHADER, """
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
						
						gl_FrontColor = NdotL * gl_Color;
						
						gl_Position = ftransform();
					}
				""")

				fragment = create_shader(GL_FRAGMENT_SHADER,"""
				
				 void main()
					{
						gl_FragColor = gl_Color;
					}
					""")
				# Создаем пустой объект шейдерной программы
				self.program = glCreateProgram()
				
				# Приcоединяем вершинный шейдер к программе
				glAttachShader(self.program, vertex2)
				# Присоединяем фрагментный шейдер к программе
				glAttachShader(self.program, fragment)
				# "Собираем" шейдерную программу
				glLinkProgram(self.program)	
			except Exception as e:
				print "except"
				return
				pass
		

		glUseProgram(self.program)
	#	print self.colors[:10]
	#	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.2, 0.1, 0.1, 0.8))
		glEnableClientState(GL_VERTEX_ARRAY)            # Включаем использование массива вершин
		glEnableClientState(GL_NORMAL_ARRAY)            # Включаем использование массива вершин
		glEnableClientState(GL_COLOR_ARRAY)

		# Указываем, где взять массив верши:
		# Первый параметр - сколько используется координат на одну вершину
		# Второй параметр - определяем тип данных для каждой координаты вершины
		# Третий парметр - определяет смещение между вершинами в массиве
		# Если вершины идут одна за другой, то смещение 0
		# Четвертый параметр - указатель на первую координату первой вершины в массиве
		glVertexPointer(3, GL_FLOAT, 0, self.vertexes)
		glNormalPointer(GL_FLOAT, 0, self.normals)
		glColorPointer(3, GL_FLOAT, 0, self.colors)
		# Рисуем данные массивов за один проход:
		# Первый параметр - какой тип примитивов использовать (треугольники, точки, линии и др.)
		# Второй параметр - начальный индекс в указанных массивах
		# Третий параметр - количество рисуемых объектов (в нашем случае это 3 вершины - 9 координат)
		glDrawArrays(GL_TRIANGLES, 0, len(self.vertexes)/3)
		glDisableClientState(GL_VERTEX_ARRAY)           # Отключаем использование массива вершин
		glDisableClientState(GL_NORMAL_ARRAY)           # Отключаем использование массива вершин
		glDisableClientState(GL_COLOR_ARRAY) 
		
		
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
				pass
		
	def draw_self(self):
		return [[], [], []]
		glPushMatrix()
		glLoadMatrixf(np.transpose(self.fw_shape_matrix))	

		floor_size = 7000.0	
		glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.0, 0.0, 0.0, 1.0))	
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
	#	glBegin(GL_QUADS)
		# glBegin(GL_LINES)
		# glNormal3f(0.0, 0.0, 1.0);
		# glVertex3f(-floor_size, -floor_size, -200.0)
		# glVertex3f(-floor_size, floor_size,  -200.0)
		# glVertex3f(floor_size, floor_size,  -200.0)
		# glVertex3f(floor_size, -floor_size,  -200.0)
		# glEnd()
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
class Floor1Col(Floor):
	def child_constr(self):
		self.append_child(Column((0, -1750, 0), (0.0, 0.0, 1.0), 0.0))
		pass
		
class Field(Floor):
	def child_constr(self):
		pass
	def draw_self(self):
		return [[], [], []]
		pass
	
class FieldDB(Field):
	db_link_list = []
	def updateByDB(self):
		conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', 'MM')
		table_name = "Links_test"
		cursor = conn.cursor()
		query_str = "SELECT `id` FROM "+table_name
#		print query_str
		cursor.execute(query_str)
		conn.close()
		server_id_list = list(i[0] for i in cursor.fetchall())
#		print server_id_list
		add_id_list = list(item for item in set(server_id_list).difference( list( db_link[0] for db_link in self.db_link_list) ) )
#		print add_id_list
		rm_id_list = list(item for item in set(list( db_link[0] for db_link in self.db_link_list)).difference( server_id_list ) )
#		print rm_id_list
		
		for rm_id in rm_id_list:
			for db_link in self.db_link_list[:]:
				if db_link[0] == rm_id:
					self.children_list.remove(db_link[1])
					self.db_link_list.remove(db_link)
		

		if len(add_id_list)>0:
			id_str = "{0}".format(add_id_list[0])
			for i in add_id_list[1:]:
				id_str += ", {0}".format(i)

			conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', 'MM')
			cursor = conn.cursor()
			query_str = "SELECT `id`, `pos_x`, `pos_y`, `pos_z`, `dir_x`, `dir_y`, `dir_z`, `angle`, `type` FROM {1} WHERE id IN ({0})".format(id_str, table_name)
			print query_str
			cursor.execute(query_str)
			conn.close()
			for add_id_link in cursor.fetchall():
				new_link = None
				if add_id_link[8] == "horisontal":
					new_link = LinkSloped((add_id_link[1], add_id_link[2], add_id_link[3]), (add_id_link[4], add_id_link[5], add_id_link[6]), add_id_link[7])
				elif add_id_link[8] == "diagonal":
					new_link = Link((add_id_link[1], add_id_link[2], add_id_link[3]), (add_id_link[4], add_id_link[5], add_id_link[6]), add_id_link[7])			
				elif add_id_link[8] == "column":
					new_link = Column((add_id_link[1], add_id_link[2], add_id_link[3]), (add_id_link[4], add_id_link[5], add_id_link[6]), add_id_link[7])							
				self.append_child(new_link)
				self.db_link_list.append([add_id_link[0], new_link])
			self.set_vertex_list(self.draw())
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
		#return [[], [], []]
		
		return getCylinVertexArray(self.fw_shape_matrix, (0.25, 0.25, 0.25, 0.9))
		#return getCubeVertexArray(self.fw_shape_matrix, (0.25, 0.25, 0.25, 0.9))
		glPushMatrix()
		glLoadMatrixf(np.transpose(self.fw_shape_matrix))	
#		glRotatef(45, 0, 0, 1)
#		glScalef(450, 450, 3000)
#		glTranslatef(0, 0, 0.5)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.25, 0.25, 0.25, 0.9))
		
		glPushMatrix()
		glTranslatef(0.0, 0.0, -0.5)
		glutSolidCylinder(0.5, 1, 10, 10)
		
		glPopMatrix()
		
#		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
#		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
#		glutWireCube(1.0)
		
		glPopMatrix()

class LinkSloped(Link):	
	def child_constr(self):	
		self.append_child(LinkEndBond((0.0, 0.0, 1210.0), (0.0, 0.0, 1.0), 0.0))
		self.append_child(LinkEndBond((0.0, 0.0, -1210.0), (0.0, 0.0, -1.0), 0.0))
		
				
		
class Column_Stock(BodyCil):
	def child_constr(self):
		pass

		
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
		heigh = 150.
		self.own_shape_matrix = np.array([[50.,   0.,   0.,   0.],
											[  0., 50.,   0.,   0.],
											[  0.,   0.,   heigh,   heigh/2],
											[  0.,   0.,   0.,  1.]])
		
		
		pass
	def draw_self(self):
		#return [[], [], []]
		return getCubeVertexArray(self.fw_shape_matrix, (0.25, 0.25, 0.25, 0.9))
		glPushMatrix()
		glLoadMatrixf(np.transpose(self.fw_shape_matrix))	
#		glRotatef(45, 0, 0, 1)
#		glScalef(450, 450, 3000)
#		glTranslatef(0, 0, 0.5)
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.25, 0.25, 0.25, 0.9))
		
		glPushMatrix()
		glTranslatef(0.0, 0.0, -0.5)
		glutSolidCylinder(0.5, 1, 10, 10)
		glPopMatrix()
		
#		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
#		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION , (0.0, 0.0, 0.0, 1.0))	
#		glutWireCube(1.0)
		
		glPopMatrix()


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
		self.append_child(Column_Stock((0.0, 0.0, 3000.0), (0.0, 0.0, 1.0), -90.0))


	def set_shape(self):
		self.own_shape_matrix = np.array([[ 3.182e+02, -3.182e+02,  0.000e+00,  0.000e+00],
											[ 3.182e+02,  3.182e+02,  0.000e+00,  0.000e+00],
											[ 0.000e+00,  0.000e+00,  3.000e+03,  1.500e+03],
											[ 0.000e+00,  0.000e+00,  0.000e+00,  1.000e+00]])
		pass

	def draw_self(self):
		#return [[], [], []]
		return getCubeVertexArray(self.fw_shape_matrix, (0.15, 0.15, 0.15, 0.9))
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




	
class Petal(Body):
	def set_shape(self):
		self.own_shape_matrix = np.array([[300.,   0.,   0.,   0.],
											[  0., 150.,   0.,   0.],
											[  0.,   0.,   8.,   0.],
											[  0.,   0.,   0.,  1.]])
		pass
	def draw_self(self):
	#	return [[], [], []]
		return getCubeVertexArray(self.fw_shape_matrix, (0.3, 0.1, 0.1, 0.9))
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