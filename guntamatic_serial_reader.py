#!/usr/bin/env python
import time
import serial

import mysql.connector
import mysecrets

mydb = mysql.connector.connect(
  host="localhost",
  user=mysecrets.user,
  password=mysecrets.password,
  database=mysecrets.databasename
)

# all data from data1, used values for db marked with *:
# TKist        *Kessel ist Temperatur 
# Tksoll       *Kessel soll Temperatur 
# Tkreg        Kessel soll wenn außerhalb der Rauchgasgrenzen 
# RGT          *Rauchgastemperatur 
# CO2 ist      CO2 Istwert 
# CO2 soll     CO2 Sollwert 
# SZ           Drehzahl Saugzuggebläse
# TB           Temperarur Boiler
# Po           *Puffer oben
# Pm           *Puffer mitte 
# Pu           *Puffer unten
# Prim ist 	Primärluft ist
# Prim soll 	Primärluft soll
# Sec ist 	Sekundärluft ist
# Sec soll 	Sekundärluft soll
# ZK           *Kesselzusand
columnnames_db = ["T_K_IST", "T_K_SOLL", "T_RG", "T_P_oben", "T_P_mitte", "T_P_unten", "KS_Zustand"]



# possible states: idle, data1, data2
state = "lbl1"
lbl1 = []
lbl2 = []
data1_str = []
data2_str = []

def write_to_db(data1_str, data2_str):
     global mydb, columnnames_db

     mycursor = mydb.cursor()

     sql = "INSERT INTO " + mysecrets.databasetable + "("
     for i in range(len(columnnames_db)):
          if i > 0:
               sql += ","
          sql += columnnames_db[i]
     sql += ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
     val = (data1_str[0], data1_str[1], data1_str[3], data1_str[8], data1_str[9], data1_str[10], data1_str[15])
     mycursor.execute(sql, val)

     mydb.commit()

     #print(mycursor.rowcount, "record inserted.")

def handle_line(line):
     global state, lbl1, lbl2, data1_str, data2_str

     #discard any empty line and dotted lines
     if(len(line.strip()) < 5 \
          or line.strip().startswith("-----")\
               or line.strip().startswith('Datum')):
          return

     #print(line.strip())

     if state == "lbl1":
          if line.strip().startswith('TKi'):
               state = "data1"
               lbl1 = line.split()
     elif state == "data1":
          #print("State data1")
          data1_str = line.split()
          state = "lbl2"
     elif state == "lbl2":
          #print("State lbl2")
          if line.strip().startswith('KLP'):
               state = "data2"
               lbl2 = line.split()
     elif state == "data2":
          #print("State data2")
          data2_str = line.split()
          #write data to database
          write_to_db(data1_str, data2_str)
          state = "lbl1"
          

     

def main():

     ##read from file
     #with open('example_message.txt', encoding='utf8') as f:
     #     for line in f:
     #          handle_line(line)
     #return

     #read from serial
     ser = serial.Serial(
          port='/dev/ttyS0',
          baudrate = 19200,
          parity=serial.PARITY_NONE,
          stopbits=serial.STOPBITS_ONE,
          bytesize=serial.EIGHTBITS,
          timeout=1
     )


     while 1:
          # read line from serial port
          x = ser.readline()
          # convert line to bytearray
          x_barray = bytearray(x)
          # remove the character 'ü' -> avoid problems
          for i in range(len(x_barray)):
               if x_barray[i] == 0xfc:
                    x_barray[i] = 0x00
          # decode bytearray as UTF-8 string
          x_str = x_barray.decode('UTF-8')
          # parse line to extract values
          handle_line(x_str)



if __name__ == "__main__":
     main()


