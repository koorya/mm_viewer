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


	

	# /* First, generate vertex index arrays for drawing with glDrawElements
	 # * All stacks, including top and bottom are covered with a triangle
	 # * strip.
	 # */

	# /* Create index vector */
	offset = 0

	# /* Allocate buffers for indices, bail out if memory allocation fails */
	stripIdx = [0]*(slices+1)*2*(stacks+2)   # /*stacks +2 because of closing off bottom and top */
	
	idx=0
	# /* top stack */
	for j in range(slices):
		stripIdx[idx  ] = 0
		stripIdx[idx+1] = j+1             # /* 0 is top vertex, 1 is first for first stack */
		idx+=2
	stripIdx[idx  ] = 0                   # /* repeat first slice's idx for closing off shape */
	stripIdx[idx+1] = 1
	idx+=2

	#/* middle stacks: */
	#  /* Strip indices are relative to first index belonging to strip, NOT relative to first vertex/normal pair in array */
	for i in range(stacks):
		offset = 1+(i+1)*slices            #    /* triangle_strip indices start at 1 (0 is top vertex), and we advance one stack down as we go along */
		for j in range(slices):
			stripIdx[idx  ] = offset+j
			stripIdx[idx+1] = offset+j+slices
			idx+=2
		stripIdx[idx  ] = offset            #   /* repeat first slice's idx for closing off shape */
		stripIdx[idx+1] = offset+slices
		idx+=2

	#   /* top stack */
	offset = 1+(stacks+2)*slices
	for j in range(slices):
		stripIdx[idx  ] = offset+j
		stripIdx[idx+1] = nVert-1           #   /* zero based index, last element in array (bottom vertex)... */
		idx+=2
	stripIdx[idx  ] = offset
	stripIdx[idx+1] = nVert-1               #   /* repeat first slice's idx for closing off shape */

	#     /* draw */
#	fghDrawGeometrySolid(vertices,normals,NULL,nVert,stripIdx,stacks+2,(slices+1)*2);
	vertices_3 = []
	normals_3 = []
	for i in [0]:#range(stacks):
		for j in range(slices):
			vertices_3 += [vertices[i*slices+j+1], vertices[i*slices+j+slices+1], vertices[i*slices+j+slices+1+1]]
			normals_3 += [normals[i*slices+j+1], normals[i*slices+j+slices+1], normals[i*slices+j+slices+1+1]]

#	return (vertices_3, normals_3, nVert*3)#/* output */
	return (vertices, normals, nVert)#/* output */