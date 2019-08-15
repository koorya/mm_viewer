# This Python file uses the following encoding: utf-8
import numpy as np

class Intersection:
	def __init__(self, dist, int_pos):
		self.pos = int_pos
		self.dist = dist
		self.obj = None

def get_intersect_square(norm, size, ray_pos, ray_dir):
	size_ = size/2.0 + 0.001
	t_x = 0
	d_n = np.dot(norm, ray_dir)	
	if d_n != 0 :
		t_x = (size/2 - np.dot(ray_pos, norm))/d_n
	if t_x>0:
		int_pos_ = ray_pos+t_x*ray_dir
		if (int_pos_[1]<=size_ and int_pos_[1]>=-size_) :
			if (int_pos_[2]<=size_ and int_pos_[2]>=-size_) :
				if (int_pos_[0]<=size_ and int_pos_[0]>=-size_) :
					dist_ = np.linalg.norm(int_pos_-ray_pos)
					return (dist_, int_pos_)
	return 0

def get_intersect_disk(norm, size, ray_pos, ray_dir):
	t_x = 0
	d_n = np.dot(norm, ray_dir)	
	if d_n != 0 :
		t_x = (size/2 - np.dot(ray_pos, norm))/d_n
	if t_x>0:
		int_pos_ = ray_pos+t_x*ray_dir
		int_pos_2d = np.array([int_pos_[0], int_pos_[1]]) 
		if np.linalg.norm(int_pos_2d)<size/2.0:
			dist_ = np.linalg.norm(int_pos_-ray_pos)
			return (dist_, int_pos_)
	return 0
	
def get_intersect_cil_surface(size, ray_pos, ray_dir, root_index):
	t_x = 0
	a = ray_dir[0]**2 + ray_dir[1]**2
	if a != 0 :
		b = 2*(ray_dir[0]*ray_pos[0] + ray_dir[1]*ray_pos[1])
		c = ray_pos[0]**2 + ray_pos[1]**2 - 0.25 # окружность с диаметром 1, т.е. вписанная в единичный квадрат
		D = b**2 - 4*a*c
		if root_index:
			t_x = (-b+D**0.5)/(2*a)
		else:
			t_x = (-b-D**0.5)/(2*a)
			
	if t_x>0:
		int_pos_ = ray_pos+t_x*ray_dir
		if (int_pos_[2]<size/2.0) and (int_pos_[2]>-size/2.0):
			dist_ = np.linalg.norm(int_pos_-ray_pos)
			return (dist_, int_pos_)
	return 0
	
def get_intersect_cube(ray_pos, ray_dir):
	ray_pos = np.array([ray_pos[0], ray_pos[1], ray_pos[2]])
	ray_dir = np.array([ray_dir[0], ray_dir[1], ray_dir[2]])
	intersect_exist = 0
	intersect = [0, 0, 0, 0, 0, 0]

	int_pos = 0
	dist = 'not a number'
	n = range(6)
	n[0] = np.array([1.0, 0.0, 0.0])
	n[1] = np.array([-1.0, 0.0, 0.0])
	n[2] = np.array([0.0, 1.0, 0.0])
	n[3] = np.array([0.0, -1.0, 0.0])
	n[4] = np.array([0.0, 0.0, 1.0])
	n[5] = np.array([0.0, 0.0, -1.0])

	for i in range(6):
		intersect_ = get_intersect_square(n[i], 1.0, ray_pos, ray_dir)
		if intersect_ != 0:
			if not intersect_exist:
				dist = intersect_[0]
				int_pos = intersect_[1]
			elif dist > intersect_[0]:
				dist = intersect_[0]
				int_pos = intersect_[1]
			intersect[i] = 1
			intersect_exist = intersect_exist or intersect[i]
	if intersect_exist:
		return Intersection(dist, int_pos)
	else:
		return None



def get_intersect_cil(ray_pos, ray_dir):
	ray_pos = np.array([ray_pos[0], ray_pos[1], ray_pos[2]])
	ray_dir = np.array([ray_dir[0], ray_dir[1], ray_dir[2]])
	intersect_exist = 0
	intersect = [0, 0, 0, 0, 0, 0]

	int_pos = 0
	dist = 'not a number'
	n = range(6)
	n[0] = np.array([0.0, 0.0, 1.0])
	n[1] = np.array([0.0, 0.0, -1.0])

	for i in range(2):
		intersect_ = get_intersect_disk(n[i], 1.0, ray_pos, ray_dir)
		if intersect_ != 0:
			if not intersect_exist:
				dist = intersect_[0]
				int_pos = intersect_[1]
			elif dist > intersect_[0]:
				dist = intersect_[0]
				int_pos = intersect_[1]
			intersect[i] = 1
			intersect_exist = intersect_exist or intersect[i]
			
	for i in range(2):
		intersect_ = get_intersect_cil_surface(1.0, ray_pos, ray_dir, i)
		if intersect_ != 0:
			if not intersect_exist:
				dist = intersect_[0]
				int_pos = intersect_[1]
			elif dist > intersect_[0]:
				dist = intersect_[0]
				int_pos = intersect_[1]
			intersect[i] = 1
			intersect_exist = intersect_exist or intersect[i]


	
	if intersect_exist:
		return Intersection(dist, int_pos)
	else:
		return None