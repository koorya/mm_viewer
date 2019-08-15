from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 

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