# HeiSO_guntamatic_reader

*(Part of project HeiSO)*

Python script for reading operating data of a **GUNTAMATIC BMK biomass converter** and saving it into a **MySQL** database on an **Raspberry Pi**.
The boiler sends its operating data every 10 seconds via its serial RS232 interface. So the Raspberry Pi just need to read the data and save it.

Tested with GUNTAMATIC Spezialheizkessel BMK40 (BJ 2008, HAICO Zentraleinheit 7.3I/O 55.1-TAURUS, SW. Vers: V1.0h)
<img src="https://user-images.githubusercontent.com/36072504/157074498-77abc48d-92bc-413f-a5a4-66ef43855495.png" height="300px">     <img src="https://user-images.githubusercontent.com/36072504/157075022-8b63f3b2-83e1-4d5c-8b9e-4e7c5fb033e1.png" height="300px"> 


## Hardware

On the boiler, the interface is designed as an RJ45 socket, which is why a special cable is needed to map the lines to a standardized SUB-D 9-pin socket. In my design I created only a very short adapter cable with a RJ45 jack instead of a RJ45 plug, as shown in the drawing below, to be able to use a standard Ethernet patch cable to connect the GUNTAMATIC biomass converter to my Raspberry Pi box a few meters away.

The pin mapping is as follows:

|RJ45   | SUB-D (female)  |description   |
|---|---|---|
|8   |5   |GND   |
|6   |2   |RX   |
|5   |3   |TX   |

![image](https://user-images.githubusercontent.com/36072504/157071015-22a067dd-5bea-4661-a558-8260ffe9c703.png) (source: GUNTAMATIC)


For the connection to the Raspberry Pi a standard RS232 Serial Port to TTL Digital Converter Module is needed (e.g: https://www.ebay.de/itm/281353512577) 
![image](https://user-images.githubusercontent.com/36072504/157070491-f4058956-79ce-4551-a098-801203999cd3.png)

## Software

On the Raspberry Pi the serial interface must be configured as follows:

|Name|Setting|
|---|---|
|**Baudrate**	|19200|
|**Parity**	|NONE|
|**Stop Bits**	|1|
|**Data Bits**	|8|
|**Flow Control**	|NONE|

The output looks similar to that:

![image](https://user-images.githubusercontent.com/36072504/157072256-863d018d-4665-4a5d-95df-6bd5ecb0086e.png)

The will script [guntamatic_serial_reader.py](https://github.com/techniccontroller/HeiSO_guntamatic_reader/blob/main/guntamatic_serial_reader.py) will parse this output and save some of the data to a MySQL database on Raspberry Pi. A tutorial how to install MySQL database on Raspberry Pi can be found here: https://pimylifeup.com/raspberry-pi-mysql/. 

The login credentials for the database are saved in the separate file *mysecrets.py* (an example of this file can be found in [mysecrets_example.py](https://github.com/techniccontroller/HeiSO_guntamatic_reader/blob/main/mysecrets_example.py)).

