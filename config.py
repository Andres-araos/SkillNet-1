#Conexion a la DB
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",        
        database="skillnet"
    )
