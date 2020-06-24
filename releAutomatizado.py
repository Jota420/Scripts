  import mysql.connector as mariadb
#import wiringpi2
from datetime import date
from datetime import datetime
import time
import RPi.GPIO as GPIO



while True:
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)
    GPIO.setup(17,GPIO.OUT)
#     GPIO.output(17,GPIO.HIGH)
    mariadb_connection = mariadb.connect(host='localhost', user='user1', password='secret', database='sensor')
    cursor = mariadb_connection.cursor()
    #cursor.execute("drop table tmp_convert")
    cursor.execute("truncate table tmp_convert")
    cursor.execute("insert into tmp_convert select cast(oxigeno as float) as DO2 from datos where oxigeno not in ('') and oxigeno not like '%s%' and oxigeno not like '%xa%' order by fecha desc limit 100")
    cursor.execute("select avg(DO2) as promDO2 from tmp_convert")
    prom = cursor.fetchone()
    datotr = str(prom)
    dato = datotr[1:datotr.find(",")]
    #print(dato)
    if (float(dato) <= 7):
        #Activa el rele para enceder la oxigenación
        print("Alerta de Disminución Oxígeno =",dato)
        #GPIO.output(17,GPIO.LOW)
        GPIO.output(17,GPIO.LOW)
        #time.sleep(1)
    elif (float(dato) > 7.5):
        #Desactiva el rele de la oxigenación
        print("Concentración de oxigeno ACEPTABLE =",dato)
        GPIO.output(17,GPIO.HIGH)
        time.sleep(3600)
    else:
        print("Ok",dato)
        GPIO.output(17,GPIO.HIGH)
        #time.sleep(5)
    
    mariadb_connection.commit()
    
    
    
    
    
    
    
