# This Python file uses the following encoding: utf-8
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
import numpy as np

treecolor = (1.0, 1.0, 1.0, 1.0)
green_color = (0.0, 1.0, 0.0, 1.0)
red_color = (1.0, 0.0, 0.0, 1.0)
blue_color = (0.0, 0.0, 1.0, 1.0)
yellow_color = (1.0, 0.8, 0.0, 1.0)
pink_color = (1.0, 0.0, 0.5, 1.0)
black_color = (0.0, 0.0, 0.0, 1.0)



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
	
def getCubeVertexArray(matrix, color = [0.1, 0.2, 0.1, 0.8], size = 1):
	size *= 0.5;
	v1 = [size, size, size, 1.]
	v2 = [size, -size, size, 1.]
	v3 = [-size, size, size, 1.]
	v4 = [-size, -size, size, 1.]
	v5 = [size, size, -size, 1.]
	v6 = [size, -size, -size, 1.]
	v7 = [-size, size, -size, 1.]
	v8 = [-size, -size, -size, 1.]
	n1 = [0., 0., 1., 0.]
	n2 = [0., 0., -1., 0.]
	n3 = [-1., 0., 0., 0.]
	n4 = [1., 0., 0., 0.]
	n5 = [0., 1., 0., 0.]
	n6 = [0., -1., 0., 0.]
	vertexes = np.array([	v3, v1, v2, 
							v3, v2, v4, 
							v7, v5, v6, 
							v7, v6, v8, 
							
							v7, v4, v8, 
							v7, v4, v3, 
							v1, v6, v5, 
							v1, v6, v2, 
							v3, v5, v1, 
							v3, v5, v7, 
							v4, v6, v2, 
							v4, v6, v8 ])
	normals = np.array(([n1]*3)*2 + 
						([n2]*3)*2 +
						([n3]*3)*2 +
						([n4]*3)*2 +
						([n5]*3)*2 +
						([n6]*3)*2 )
	
	# vertexes = np.array([	v3, v2, v1, v3, v2, v4 ])
	# normals = np.array(([n1]*3)*2)
						
			
#	print vertexes		
#	vertexes = vertexes.dot(np.array([[1000., 0., 0., 0.], [0., 1000., 0., 0.], [0., 0., 1000., 0.], [0., 0., 0., 1.]]))
#	print matrix
	vertexes = np.array([matrix.dot(vertex) for vertex in vertexes])
#	print vertexes
#	exit()
	normals = np.array([matrix.dot(normal) for normal in normals])
	
	c = np.linalg.norm(normals, axis = 1)
	normals = normals / np.array([[v]*3+[1] for v in c])	
#	print vertexes
	return [[vertexes[:]], [normals[:]], [np.array([color]*36)]]	
	
	
	

# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def create_shader(shader_type, source):
	# Создаем пустой объект шейдера
	shader = glCreateShader(shader_type)
	# Привязываем текст шейдера к пустому объекту шейдера
	glShaderSource(shader, source)
	# Компилируем шейдер
	glCompileShader(shader)
	# Возвращаем созданный шейдер
	return shader	

	
	
	
	