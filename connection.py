import pandas as pd
import sqlalchemy
import mysql.connector

def set_conection():
	rules = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
	database="elixirdatabase"
	)
	return rules
