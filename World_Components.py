import numpy as np

class World_Component:
	parent = None
	def set_parent_matrix(self, par_matrix):
		pass

	
class Mounted_Component(World_Component):
	def set_parent(self, parent = None):
		if isinstance(parent, Hanger_Component):
			self.parent = parent 
		if isinstance(self.parent, Hanger_Component):
			self.set_parent_matrix(self.parent.resMatrix)
	

class Hanger_Component(Mounted_Component):
	resMatrix = np.eye(4)
	
	
