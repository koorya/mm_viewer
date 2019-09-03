# This Python file uses the following encoding: utf-8
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
import numpy as np
from cylinder import *

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


def getCylinVertexArray(matrix, color = [0.1, 0.2, 0.1, 0.8], size = 1):
# # getCylinVertexArray

	
	#vertexes, normals, nVert = fghGenerateCylinder(size/2., size, 5, 5)


	#print vertexes
	# exit()

	
	size *= 0.5;
	v1 = [ size,  size,  size]
	v2 = [ size, -size,  size]
	v3 = [-size,  size,  size]
	v4 = [-size, -size,  size]
	v5 = [ size,  size, -size]
	v6 = [ size, -size, -size]
	v7 = [-size,  size, -size]
	v8 = [-size, -size, -size]
	
	
	n1 = [ 0.,  0.,  1.]
	n2 = [ 0.,  0., -1.]
	n3 = [-1.,  0.,  0.]
	n4 = [ 1.,  0.,  0.]
	n5 = [ 0.,  1.,  0.]
	n6 = [ 0., -1.,  0.]
	
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
	
	
	vertexes = np.array(vertexes).ravel().reshape(-1, 3)						
	vertexes = np.vstack([np.hstack((a,[1.])) for a in vertexes])		
	
	normals = np.array(normals).ravel().reshape(-1, 3)	
	normals = np.vstack([np.hstack((a,[0.])) for a in normals])
	
	vertexes = np.array([matrix.dot(vertex) for vertex in vertexes])

	normals = np.array([matrix.dot(normal) for normal in normals])
	
	c = np.linalg.norm(normals, axis = 1)
	normals = normals / np.array([[v]*3+[1] for v in c])	

	return [[vertexes[:]], [normals[:]], [np.array([color]*len(vertexes))]]	
	
	
def getCubeVertexArray(matrix, color = [0.1, 0.2, 0.1, 0.8], size = 1):
	size *= 0.5;
	v1 = [ size,  size,  size]
	v2 = [ size, -size,  size]
	v3 = [-size,  size,  size]
	v4 = [-size, -size,  size]
	v5 = [ size,  size, -size]
	v6 = [ size, -size, -size]
	v7 = [-size,  size, -size]
	v8 = [-size, -size, -size]
	
	
	n1 = [ 0.,  0.,  1.]
	n2 = [ 0.,  0., -1.]
	n3 = [-1.,  0.,  0.]
	n4 = [ 1.,  0.,  0.]
	n5 = [ 0.,  1.,  0.]
	n6 = [ 0., -1.,  0.]
	
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
	
	
	vertexes = np.array(vertexes).ravel().reshape(-1, 3)						
	vertexes = np.vstack([np.hstack((a,[1.])) for a in vertexes])		
	
	normals = np.array(normals).ravel().reshape(-1, 3)	
	normals = np.vstack([np.hstack((a,[0.])) for a in normals])


	vertexes = np.array([matrix.dot(vertex) for vertex in vertexes])

	normals = np.array([matrix.dot(normal) for normal in normals])
	
	c = np.linalg.norm(normals, axis = 1)
	normals = normals / np.array([[v]*3+[1] for v in c])	

	return [[vertexes[:]], [normals[:]], [np.array([color]*len(vertexes))]]	
	
	
	

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

	
	
	
	