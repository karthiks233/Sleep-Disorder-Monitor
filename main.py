#!/usr/bin/env python
import time
import os
import spidev
import RPi.GPIO as GPIO
#import IoTSend
import numpy
import httplib, urllib
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = 'quot;AC28ca66f76bb6294049e2c0ceda413ea0"';
auth_token = 'quot;f33bb1bfb8a1804630e5e936c4664d0a"';

client = Client(account_sid, auth_token)

buzzer = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(buzzer,False)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=5000

##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##
##----------------------------------------------------------------------
sleep = 2
key ='39;U9EFHEHXROFSKG4P'; # Thingspeak channel to update
# ----------------------------------------------------------------------
def send_IoTData(field1,field2,field3,field4):
try:
params = urllib.urlencode({'39;field1'39;: field1, '39;field2'39;: field2, '39;field3'39;: field3,'39;field4'39;:
field4, '39;key'39;:key })
headers = {";Content-typZZe";: ";application/x-www-form-
urlencoded";,";Accept";: ";text/plain";}
conn = httplib.HTTPConnection(";api.thingspeak.com:80";)

conn.request(";POST";, ";/update";, params, headers)
response = conn.getresponse()
print (response.status, response.reason)
data = response.read()
conn.close()
except:
return

def send_IoTDataField1(field1):
try:
params = urllib.urlencode({'39;field1'39;: field1, '39;key'39;:key })
headers = {";Content-typZZe";: ";application/x-www-form-
urlencoded";,";Accept";: ";text/plain";}
conn = httplib.HTTPConnection(";api.thingspeak.com:80";)

conn.request(";POST";, ";/update";, params, headers)
response = conn.getresponse()
print (response.status, response.reason)
data = response.read()
conn.close()
except:
return

def send_IoTDataField2(field2):
try:
params = urllib.urlencode({'39;field2'39;: field2, '39;key'39;:key })
headers = {";Content-typZZe";: ";application/x-www-form-
urlencoded";,";Accept";: ";text/plain";}
conn = httplib.HTTPConnection(";api.thingspeak.com:80";)

conn.request(";POST";, ";/update";, params, headers)
response = conn.getresponse()
print (response.status, response.reason)
data = response.read()
conn.close()
except:
return

def send_IoTDataField3(field3):
try:
params = urllib.urlencode({'39;field3'39;: field3, '39;key'39;:key })
headers = {";Content-typZZe";: ";application/x-www-form-
urlencoded";,";Accept";: ";text/plain";}
conn = httplib.HTTPConnection(";api.thingspeak.com:80";)

conn.request("POST";, ";/update";, params, headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
conn.close()
except:
return

def send_IoTDataField4(field4):
try:
params = urllib.urlencode({'39;field4'39;: field4, '39;key'39;:key })

headers = {";Content-typZZe";: ";application/x-www-form-
urlencoded";,";Accept";: ";text/plain";}
conn = httplib.HTTPConnection(";api.thingspeak.com:80";)

conn.request(";POST";, ";/update";, params, headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
conn.close()
except:
return
##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##

# Define delay between readings
delay = 1
####

def ReadChannel(channel):
adc = spi.xfer2([1,(8+channel)&lt;&lt;4,0])
data = ((adc[1]&amp;3) &lt;&lt; 8) + adc[2]
return data

# rounded to specified number of decimal places.
def ConvertVolts(data,places):

volts = (data * 3.3) / float(1023)
volts = round(volts,places)
return volts

# number of decimal places.

while True:

ECG_level = ReadChannel(1)
print(";ECG:%.2f";%(ECG_level))
time.sleep(1)
send_IoTDataField1(ECG_level)
if(ECG_level&gt;160):
print('39;ECG level id high'39;)
GPIO.output(buzzer,True)
time.sleep(2)
GPIO.output(buzzer,False)
client.api.account.messages.create(
to=";+91-8296352875";,
from_=";+19783064025"; , #+1 210-762-4855";
body="; person in danger"; )
noise_level = ReadChannel(0)
print(";noise:%.2f";%(noise_level))
time.sleep(1)
send_IoTDataField2(noise_level)

if(noise_level&gt;500):
print('person suffer from sleep appnea')

X_level = ReadChannel(2)
X_volts = ConvertVolts(X_level,2)

Y_level = ReadChannel(3)
Y_volts = ConvertVolts(Y_level,2)
print (";--------------------------------------------";)
print(";X_level :{} ";.format(X_level))
send_IoTDataField3(X_level)

print(";Y_level :{} ";.format(Y_level))
send_IoTDataField4(X_level)

if(X_level&gt;360):
    print('39;person is not having sleep'39;)
    GPIO.output(buzzer,True)
time.sleep(2)
GPIO.output(buzzer,False)

if(Y_level&gt;380):
print('39;person is not having sleep'39;)
GPIO.output(buzzer,True)
time.sleep(2)
GPIO.output(buzzer,False)
if((ECG_level&lt;160) and (noise_level&lt;500) and (X_level&lt;360) and (Y_level&lt;380)):
print('39;PERSON IS HEALTHY'39;)
