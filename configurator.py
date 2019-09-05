# This Python file uses the following encoding: utf-8
import numpy as np
import MySQLdb
from Constants import *

from Manipulator import Manipulator 

manip = Manipulator()

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
for indx, col in enumerate(col_name_list):
	print col," : ", row[indx]

################################
values_list[2] += 10
################################

conn = MySQLdb.connect('172.16.0.77', 'user1', 'vbtqjpxe', DATABASE_NAME)
cursor = conn.cursor()

col_name_list = manip.driven_joints_name

value_str = "`{0}` = {1}".format(col_name_list[0], values_list[0])
for indx, col in enumerate(col_name_list[1:]):
	value_str += ", `{0}` = {1}".format(col, values_list[indx+1])
	print value_str
	
query_str = "UPDATE `{0}` SET {1} WHERE (id = {2})".format(CONFIGURATION_TABLE, value_str, id)
print query_str

cursor.execute(query_str)
conn.commit()
conn.close()