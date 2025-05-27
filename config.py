#Conexion a la DB
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="LeonardElMasMakia123@ñ",        
        database="skillnet"
    )
