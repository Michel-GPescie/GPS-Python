#!/usr/bin/python
#	GPS.py
# Ce fichier peut etre execute directement
#
#	autheur : Michel GOMEZ-PESCIE
#	licence : MIT


"""
	Fonctions:
		- signal_handler(_signal, _frame)
		- readGPS(_connection)
		- initSerialGPS()
		- run_as_main()
	Class:
		- TrameGPGGA
			Methods
				- format()
			Properties
				- self.time = {'H':time[:2], 'M':time[2:4], 'S':time[4:6]}
				- self.latitude = latitude
				- self.lat_Cardinal = lat_Cardinal
				- self.longitude = longitude
				- self.long_Cardinal = long_Cardinal
				- self.quality = quality
				- self.satellites = satellites
				- self.precision = precision
				- self.altitude = altitude
"""

import signal
import serial
import os

uart1="/dev/ttyO1"
uart2="/dev/ttyO2"
uart4="/dev/ttyO4"

##############################
# Handler pour SIGINT (CTRL+C)
#
def signal_handler(_signal, _frame):
	for connection in list_ser:
		connection.close()
	sys.exit(0)

# __________ END SIGNAL_HANDLER ______________________________

##############################################################
# Classe permettant de stocker les donnees d'une trame GPGGA et de formatter une sortie console
#
class TrameGPGGA:
	""" contient les donnees d'une trame GPS GPGGA 
	La fonction membre 'format()' permet d'extraire une chaine de caracteres contenant les infos """
	
	def __init__(self, time, latitude, lat_Cardinal, longitude, long_Cardinal, quality, satellites, precision, altitude):
		self.time = {'H':time[:2], 'M':time[2:4], 'S':time[4:6]}
		self.latitude = latitude
		self.lat_Cardinal = lat_Cardinal
		self.longitude = longitude
		self.long_Cardinal = long_Cardinal
		self.quality = quality
		self.satellites = satellites
		self.precision = precision
		self.altitude = altitude
	
	def format(self):
		return ('\n*------------------------------------------------*\n'\
				+ '*   $GPGGA %s h %s m %s s GMT	%s satellites    *\n' \
					% (self.time['H'], self.time['M'], self.time['S'], self.satellites) \
				+ '*   latitude  : %s %s                      *\n' \
					% (self.latitude, self.lat_Cardinal) \
				+ '*   longitude : %s %s                     *\n' \
					% (self.longitude, self.long_Cardinal) \
				+ '*   Quality: %s 		Precision: %s		 *\n' \
					% (self.quality, self.precision)\
				+ '*------------------------------------------------*\n')
		
		
# __________ END CLASS TRAMEGPGGA ______________________________

################################################################
# lit une trame GPS et retourne un object 'TrameGPGGA' #########
#
def readGPS(_connection):
	if not _connection.isOpen():
		_connection.open()
	data=''
	data_parts=[]
	foo = 0
	while (not data[:6] == '$GPGGA') and (foo < 10):
		print 'receiving GPS data...'
		data = _connection.readline()
		foo += 1
	
	data_parts = data.split(',')
	trame = TrameGPGGA(time=data_parts[1],
			latitude=data_parts[2],
			lat_Cardinal=data_parts[3],
			longitude=data_parts[4],
			long_Cardinal=data_parts[5],
			quality=data_parts[6],
			satellites=data_parts[7],
			precision=data_parts[8],
			altitude=data_parts[9])
	print 'GPS data received'
	return trame
	
# __________ END READGPS ______________________________

#######################################################
# Ouverture de l'uart1 /dev/ttyO1 @9600 bauds #########
#
def initSerialGPS():
	s = serial.Serial(port=uart1, baudrate=9600)
	if s.isOpen():
		print('%s open.' % uart1)
	else:
		print('Failing open %s' % uart1)
	
	return s
	
# __________ END INITSERIALGPS ______________________________

#############################################################
# Fonction if __name__ == '__main__': #######################
#
def run_as_main():
	serialConnection = initSerialGPS()
	trame = readGPS(serialConnection).format()
	print trame
	
# __________ END MAIN ______________________________


#	#	#	#	#	#	#
#	Execution
#	#	#	#	#	#	#

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	run_as_main()

