#!/usr/bin/env python
import time
import serial

import mysql.connector
import mysecrets

mydb = mysql.connector.connect(
  host="localhost",
  user=mysecrets.user,
  password=mysecrets.user,
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
# ZK           *Kesselzusand
columnnames_db = ["T_K-IST", "T_K-SOLL", "T_RG", "T_P-oben", "T_P-mitte", "T_P-unten", "KS_Zustand"]



# possible states: idle, data1, data2
state = "idle"
lbl1 = []
lbl2 = []
data1_str = []
data2_str = []
data1_received = False

def write_to_db(data1_str, data2_str):
     global mydb, columnnames_db

     mycursor = mydb.cursor()

     sql = "INSERT INTO " + mysecrets.databasetable + "("
     for i in range(len(columnnames_db)):
          if i > 0:
               sql += ","
          sql += columnnames_db[i]
     sql += ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
     val = (data1_str[0], data1_str[1], data1_str[3], data1_str[8], data1_str[9], data1_str[10], data1_str[11])
     mycursor.execute(sql, val)

     mydb.commit()

     print(mycursor.rowcount, "record inserted.")

def handle_line(line):
     global state, lbl1, lbl2, data1_str, data2_str, data1_received

     #discard any empty line and dotted lines
     if(len(line) < 5 \
          or line.strip().startswith("-----")\
               or line.strip().startswith('Datum')):
          return

     print(line)

     if state == "idle":
          if line.strip().startswith('TKi'):
               state = "data1"
               lbl1 = line.split()
          elif line.strip().startswith('KLP'):
               state = "data2"
               lbl2 = line.split()
     elif state == "data1":
          print('Data1 received')
          data1_str = line.split()
          #data1 = []
          #for lbl, data in zip(lbl1, data1_str):
          #     #print(lbl + ": " + str(float(data)))
          #     data1.append(float(data))
          #print(data1)
          state = "idle"
          data1_received = True
     elif state == "data2":
          print('Data2 received')
          data2_str = line.split()
          #data2 = []
          #for lbl, data in zip(lbl2, data2_str):
          #     print(lbl + ": " + str(float(data)))
          #     data2.append(float(data))
          #print(data2)

          if data1_received:
               #write data to database
               write_to_db(data1_str, data2_str)
               data1_received = False
          state = "idle"
          

     

def main():

     #read from file
     with open('example_message.txt', encoding='utf8') as f:
          for line in f:
               handle_line(line)
     return

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
          x = ser.readline()
          x_barray = bytearray(x)
          for i in range(len(x_barray)):
               if x_barray[i] == 0xfc:
                    x_barray[i] = 0x00
          x_str = x_barray.decode('UTF-8')
          handleLine(x_str)



if __name__ == "__main__":
     main()


