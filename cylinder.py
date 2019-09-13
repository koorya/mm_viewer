import numpy as np

def fghCircleTable(n = 10, halfCircle = False):


	# /* Table size, the sign of n flips the circle direction */
	size = abs(n)
	M_PI = np.pi
	# /* Determine the angle between samples */
	angle = (1.+int(not halfCircle))*M_PI/( n + int(n == 0))

	# /* Allocate memory for n samples, plus duplicate of first entry at the end */
	sint = list([0.] * (size+1))
	cost = list([0.] * (size+1))


	# /* Compute cos and sin around the circle */
	sint[0] = 0.0;
	cost[0] = 1.0;

	for i in range(1, size):
		sint[i] = np.sin(angle*i)
		cost[i] = np.cos(angle*i)
 
	if (halfCircle):
		sint[size] =  0.0 # /* sin PI */
		cost[size] = -1.0 # /* cos PI */

	else:
		# /* Last sample is duplicate of the first (sin or cos of 2 PI) */
		sint[size] = sint[0]
		cost[size] = cost[0]

	return (sint, cost)
	
	
def fghGenerateCylinder(radius=0.5, height=1, slices=10, stacks=10):
	idx = 0    #/* idx into vertex/normal buffer */

   # /* Step in z as stacks are drawn. */
	radf = radius
	stacks_ = stacks
	if stacks_ <= 0:
		stacks_ = 1
	zStep = 1.*height / ( stacks_ );



	# /* number of unique vertices */
	if (slices==0 or stacks<1):
		return ([],[], 0)

	nVert = slices*(stacks+3)+2

   # /* Pre-computed circle */
	sint, cost = fghCircleTable(-slices, False)

  #  /* Allocate vertex and normal buffers, bail out if memory allocation fails */
	vertices = list([0.]*3*nVert)
	normals  = list([0.]*3*nVert)

	z=-0.5*height
	# /* top on Z-axis */
	vertices[0] =  0.
	vertices[1] =  0.
	vertices[2] =  -0.5*height
	normals[0] =  0.
	normals[1] =  0.
	normals[2] = -1.
	idx = 3
 #   /* other on top (get normals right) */
	for j in range(0, slices):
		vertices[idx  ] = cost[j]*radf
		vertices[idx+1] = sint[j]*radf
		vertices[idx+2] = z
		normals[idx  ] = 0.
		normals[idx+1] = 0.
		normals[idx+2] = -1.
		idx+=3


   # /* each stack */
	for i in range(0, stacks+1):
		for j in range(0, slices):
			vertices[idx  ] = cost[j]*radf
			vertices[idx+1] = sint[j]*radf
			vertices[idx+2] = z
			normals [idx  ] = cost[j]
			normals [idx+1] = sint[j]
			normals [idx+2] = 0.
			idx+=3
		z += zStep


	# /* other on bottom (get normals right) */
	z -= zStep
	for j in range(0, slices):
		vertices[idx  ] = cost[j]*radf
		vertices[idx+1] = sint[j]*radf
		vertices[idx+2] = z
		normals [idx  ] = 0.
		normals [idx+1] = 0.
		normals [idx+2] = 1.
		idx+=3


	# /* bottom */
	vertices[idx  ] =  0.
	vertices[idx+1] =  0.
	vertices[idx+2] =  0.5*height
	normals [idx  ] =  0.
	normals [idx+1] =  0.
	normals [idx+2] =  1.


	
	vertices_3 = []
	normals_3 = []
	ofset = slices+1
	for i in range(stacks):
		for j in range(slices-1):
			cur_ofset = (ofset+i*slices+j)
			vertices_3 += vertices[cur_ofset*3:cur_ofset*3+3] + vertices[(cur_ofset+slices)*3:(cur_ofset+slices)*3+3] + vertices[(cur_ofset+slices+1)*3:(cur_ofset+slices+1)*3+3]
			normals_3 += normals[cur_ofset*3:cur_ofset*3+3] + normals[(cur_ofset+slices)*3:(cur_ofset+slices)*3+3] + normals[(cur_ofset+slices+1)*3:(cur_ofset+slices+1)*3+3]
			vertices_3 += vertices[cur_ofset*3:cur_ofset*3+3] + vertices[(cur_ofset+slices+1)*3:(cur_ofset+slices+1)*3+3] + vertices[(cur_ofset+1)*3:(cur_ofset+1)*3+3]
			normals_3 += normals[cur_ofset*3:cur_ofset*3+3] + normals[(cur_ofset+slices+1)*3:(cur_ofset+slices+1)*3+3] + normals[(cur_ofset+1)*3:(cur_ofset+1)*3+3]
		cur_ofset = (ofset+i*slices+slices-1)
		vertices_3 += vertices[cur_ofset*3:cur_ofset*3+3] + vertices[(cur_ofset+slices)*3:(cur_ofset+slices)*3+3] + vertices[(ofset+i*slices+slices)*3:(ofset+i*slices+slices)*3+3]
		normals_3 += normals[cur_ofset*3:cur_ofset*3+3] + normals[(cur_ofset+slices)*3:(cur_ofset+slices)*3+3] + normals[(ofset+i*slices+slices)*3:(ofset+i*slices+slices)*3+3]
		vertices_3 += vertices[cur_ofset*3:cur_ofset*3+3] + vertices[(ofset+i*slices+slices)*3:(ofset+i*slices+slices)*3+3] + vertices[(ofset+i*slices)*3:(ofset+i*slices)*3+3]
		normals_3 += normals[cur_ofset*3:cur_ofset*3+3] + normals[(ofset+i*slices+slices)*3:(ofset+i*slices+slices)*3+3] + normals[(ofset+i*slices)*3:(ofset+i*slices)*3+3]		
	return (vertices_3, normals_3)#/* output */
#	return (vertices[ofset*3:(ofset+2*slices)*3], normals, nVert)#/* output */