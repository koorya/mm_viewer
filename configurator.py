# This Python file uses the following encoding: utf-8
import time
time_stamp = time.time()
import numpy as np
import MySQLdb
print "time: ", (time.time()-time_stamp)

from Constants import *
print "time: ", (time.time()-time_stamp)

from Manipulator import Manipulator 

import zmq
import pickle

manip = Manipulator()
print "time: ", (time.time()-time_stamp)


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://127.0.0.1:43000')

while True:
	command, value = pickle.loads(socket.recv())
	socket.send(b'ok')
	
	conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', DATABASE_NAME)
	cursor = conn.cursor()

	col_name_list = manip.driven_joints_name
	col_name_list.append("stick_in_hand")
	col_name_str = "`{0}`".format(col_name_list[0])
	for i in col_name_list[1:]:
		col_name_str += ", `{0}`".format(i)
	query_str = "SELECT {0} FROM {2} WHERE (id = {1})".format(col_name_str, id, CONFIGURATION_TABLE)
	cursor.execute(query_str)
	conn.close()

	row = cursor.fetchone()
	values_list = [r for r in row]
	# for indx, col in enumerate(col_name_list):
		# print col," : ", row[indx]

	################################
	if command == 'tower_rel':
		values_list[2] += value
	elif command == 'tower_abs':
		values_list[2] = value
	################################

	conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', DATABASE_NAME)
	cursor = conn.cursor()

	col_name_list = manip.driven_joints_name

	value_str = "`{0}` = {1}".format(col_name_list[0], values_list[0])
	for indx, col in enumerate(col_name_list[1:]):
		value_str += ", `{0}` = {1}".format(col, values_list[indx+1])
		# print value_str
		
	query_str = "UPDATE `{0}` SET {1} WHERE (id = {2})".format(CONFIGURATION_TABLE, value_str, id)
	# print query_str

	cursor.execute(query_str)
	conn.commit()
	conn.close()



print "time: ", (time.time()-time_stamp)


