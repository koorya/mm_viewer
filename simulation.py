# This Python file uses the following encoding: utf-8
import sys
import numpy as np
import MySQLdb

from Column import Body
from Column import Column
from Column import Petal
from Column import Floor
from Column import Field
from Column import FilledFloor
from Column import Link
import sensor
import Manipulator as mm
from Constants import *

import time 




np.set_printoptions(precision = 3)

mode = 'sql'




floor1 = Floor((0.0, 0.0, -636.5), (0.0, 0.0, 1.0), 0.0)
floor2 = FilledFloor((0.0, 0.0, -636.5 - 3000.0), (0.0, 0.0, 1.0), 0.0)
field = Field((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 0.0)
field.append_child(floor1)
field.append_child(floor2)




manip = mm.Manipulator()
res_pos = (-1750.0, 720.5, 652.8, 0.0, 0.0)
conf = manip.getConfigByTarget(res_pos)
conf = np.zeros(10)
conf[0] = H #2618.5
conf[1] = 617
manip.setConfig(conf)
manip.setActiveField(field)



conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', 'MM')

time_stamp = time.time()

call_cnt = 0
def timercallback():
	global manip, mode, conn, time_stamp, call_cnt, id

	if mode== 'sql':
#		conn = MySQLdb.connect('localhost', 'user1', 'vbtqjpxe', 'my_new_schema')
		
		cursor = conn.cursor()
		col_name_list = manip.driven_joints_name
		col_name_str = "`{0}`".format(col_name_list[0])
		for i in col_name_list[1:]:
			col_name_str += ", `{0}`".format(i)
		query_str = "SELECT {0} FROM configuration_new WHERE (id = {1})".format(col_name_str, id)
#		print query_str
		cursor.execute(query_str)
		# Получаем данные.
		row = cursor.fetchone()
		manip.setConfig(row)
#		print "q1: ",row[0], "q2: ",row[1], "q3: ",row[2], "q4: ",row[3], "q5: ",row[4]
#		conn.close()
#		print manip.getTarget();

	manip.calc_kinematics()



	if mode== 'sql':
#		conn = MySQLdb.connect('localhost', 'user1', 'vbtqjpxe', 'my_new_schema')
		conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', 'MM')		
		cursor = conn.cursor()
		cursor.execute(manip.get_sql_sensor_query(id))
		conn.commit()
#		conn.close()

	
#	print "callback execute"
	call_cnt += 1
	if (call_cnt % 500 == 0):
		print "time: ", (time.time()-time_stamp)/500.
		time_stamp = time.time()
	
	pass



while 1:
	timercallback()

