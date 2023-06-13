import time
import os
import serial
import math
from datetime import date
from datetime import datetime


#//////////////////////////////////////////////////////
# set serial port & disable reset on port open
# otherwise OAT will forget time&date when KSTARS connects
#/////////////////////////////////////////////////////

serialport = "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0"
os.system('stty -F /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 -hupcl')

#////////////////////////////////////
# open serial port & check connection
#///////////////////////////////////

print("Opening serial port on " + serialport + '...')
ser = serial.Serial(serialport, 19200, timeout = .2)
time.sleep(0)                                           #wait for reboot
ser.write(str.encode(':GVP#:GVN#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))

if (response_utf) == ('') :
    print('Could not communicate with OAT, quitting...')
    quit()

else:  print(str(response_utf) + ' is online!') 

#////////////////////////////////////
# Set site coordinates
#///////////////////////////////////

print("Home Site LAT is 38*34")     # Show your Home Latitude in DM (DegreesMinutes) format
print("Home Site LONG is 90*33")    # Show your Home Longitude

ser.write(str.encode(':St38*34#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))

ser.write(str.encode(':Sg270*33#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))


#////////////////////////////////////
# Set Time
#///////////////////////////////////

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
#print("Current Time =", current_time)

ser.write(str.encode(':SL' + str(current_time) + '#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('Site local time successfully set to: ' + str(current_time))
else: print('Could not set local time...')

#////////////////////////////////////
# Set Date
#///////////////////////////////////

today = date.today()

# mm/dd/y
d3 = today.strftime("%m/%d/%y")
#print("Current Date =", d3)

ser.write(str.encode(':SC' + str(d3) + '#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))
response_set = (''.join(filter(str.isdigit, response_utf)))
if int(response_set) == 1:
    print('Site date successfully set to: ' + str(d3))
    response_strip = response_utf.strip("1")
    print(str(response_strip) + ' done!') 
else: print('Could not set site date...')


#////////////////////////////////////
# Set UTC Offset
#///////////////////////////////////

ts = time.time()
utc_offset = (datetime.fromtimestamp(ts) -
              datetime.utcfromtimestamp(ts)).total_seconds()

utc_offset_hour = int(utc_offset / 3600)

if  utc_offset_hour > 0:
    utc_offset_hour_str = str(utc_offset_hour)
    utc_offset_hour_zero = utc_offset_hour_str.zfill(2)
    utc_offset_hour_sign = '+' + str(utc_offset_hour_zero)
elif  utc_offset_hour < 0:
    utc_offset_hour_str = str(abs(utc_offset_hour))
    utc_offset_hour_zero = utc_offset_hour_str.zfill(2)
    utc_offset_hour_sign = '-' + str(utc_offset_hour_zero)
else:
    utc_offset_hour_sign = str('+00')


ser.write(str.encode(':SG' + str(utc_offset_hour_sign) + '#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('Site UTC offset successfully set to: ' + str(utc_offset_hour_sign))
else: print('Could not set UTC offset...')
#print("Current UTC offset =", utc_offset_hour_sign)


#////////////////////////////////////
# Set current position as Home
#///////////////////////////////////

print('Setting current orientation as Home Point')
ser.timeout = None
ser.write(str.encode(':SHP#'))
response = ser.read(1)
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('Done!')
else: print('Could not set Home Point...')


#////////////////////////////////////
# Stop and exit
#///////////////////////////////////

#print('Stoping all motors...')
#ser.write(str.encode(':Q#'))

ser.close() 

print("////////////////////////////////")
print("/// OAT configuration is     ///")
print("/// completed. Disable Time  ///")
print("/// and Location updating    ///")
print("/// in KSTARS before         ///")
print("/// connecting to OAT!!!     ///")
print("////////////////////////////////")
