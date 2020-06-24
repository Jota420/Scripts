import serial
import json
import http.client
#Libreria para thingSpeak
import urllib3
from urllib.parse import urlencode
#Libreria para fecha y transforamr datos
from decimal import Decimal
from datetime import date
from datetime import datetime
#Libreria para la conexión a la base de datos MariaDB
import mysql.connector as mariadb
import time
#Lectura de datos por el puerto serial
arduino = serial.Serial('/dev/ttyACM0',9600)



key = "IAA97MYBRMW3WVJJ"  # API Key ThingSpeak

def Planta():
    
    DO2 = ""
    WATTS = ""
    IRMS = ""    
    while True:
        
        #Conexion hacia Mariadb
        mariadb_connection = mariadb.connect(host='localhost', user='user1',
                                             password='secret', database='sensor')
        cursor = mariadb_connection.cursor()
        #Obtencion de Datos
        dato = arduino.readline()
        #convertir a string
        chare = str(dato)
        #Comprobando si el dato es Oxigeno
        if(chare.find("DO2 =") >= 0 and chare.find("DO2 =") >= 0):
            #Discriminando el valor de Oxígeno
            DO2_PURGUE = chare.find("DO2 =")+5
            chareb = chare.find("DO2 =")+10
            #Obteniendo y almacenando el valor de Oxígeno
            DO2 = chare[DO2_PURGUE:chareb]
            print("DO2   =",DO2)
            
        elif(chare.find("Watts =") >= 0):
            WATTS_PURGUE = chare.find("Watts =")+7
            charea = chare.find("Watts =")+12
            WATTS = chare[WATTS_PURGUE:charea]
            print("Watts =",WATTS)
            
        elif(chare.find("Irms =") >= 0):
            IRMS_PURGUE = chare.find("Irms =")+6
            charec = chare.find("Irms =")+11
            IRMS = chare[IRMS_PURGUE:charec]
            print("Irms  =",IRMS)
        
        #Guardando los datos en la base local de mariadb
        sql = "INSERT INTO sensor.datos(fecha,oxigeno,watts,irms) values (%s,%s,%s,%s)"
        now = datetime.now()
        #array de los datos
        val = (now,DO2,WATTS,IRMS)
        #inserción de datos en la setencia SQL
        cursor.execute(sql,val)
        #Guardando la sesion
        mariadb_connection.commit()
        #Enviando datos hacia ThingSpeak
        params = urlencode({'field1': DO2,'field2': WATTS, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            #Abriendo al conexión hacia ThingSpeak
            conn.request("POST", "/update", params, headers)
            #Estado de la conxión 
            response = conn.getresponse()
            #print (Oxigeno)
            print (response.status, response.reason)
            data = response.read()
            #cerrando la conexión
            conn.close()
        except:
            print ("connection failed")
        break
if __name__ == "__main__":
        while True:
                Planta()

