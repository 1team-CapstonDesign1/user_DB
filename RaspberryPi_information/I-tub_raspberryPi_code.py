import RPi.GPIO as GPIO
import time
import spidev
import smbus
import os
import glob
import requests, json
import pymysql
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

db = pymysql.connect (
    user='bf1138ba34c820',
    passwd = '22ac05b88712768',
    host='us-cdbr-iron-east-01.cleardb.net',
    db = 'heroku_6295f565c172990',
    charset='utf8'
)

bus = smbus.SMBus(1)
add = 0x48

idx = 0

switch = 17

GPIO.setup(switch, GPIO.IN)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#GPIO PIN
IN1 = 19  #37 pin
IN2 = 13  #35 pin
IN3 = 6   #31 pin
IN4 = 5   #29 pin

servo = 22

GPIO.setup(servo, GPIO.OUT)

p = GPIO.PWM(servo, 50)
p.start(0)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# servo motor controll def
def setServoPos(degree):
    if (degree > 180):
        degree = 180

    duty = 3 + (degree*(12-3)/180.0)
    p.ChangeDutyCycle(duty)
    
# 모터 제어 함수
def setMotorContorl(INA, INB, stat):
    #앞으로
    if stat == 'FORWARD':
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
    #뒤로
    elif stat == 'BACKWORD':
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
    #정지
    elif stat == 'STOP':
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.LOW)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

def read_ADC():
    bus.read_byte(add)
    analog = bus.read_byte(add)
    return analog

servo_cnt = 0
cursor = db.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM u_db WHERE u_last = 1"
start = 0

water = 0
temperature = 0

while True:
    try:
        if (start == 0):
            sql = "SELECT * FROM u_db WHERE u_last = 1"
            len = cursor.execute(sql)
            for val in cursor:
                print(val)
                water = val['u_water']
                temperature = val['u_temperature']
            
            if (len > 0):
                setServoPos(90)
                time.sleep(1)
                setServoPos(0)
                start = 1
        
        if (len > 0):
            bus.write_byte(add, 0x00)
            ain0 = read_ADC()
            setMotorContorl(19, 13, 'FORWARD')
            setMotorContorl(6, 5, 'FORWARD')
            print("temperature value = %3d" % read_temp())
            print("moisture value = %3d" % (ain0))
            

            if (ain0 >= water + 50):
                servo_con(0)
                setMotorContorl(19, 13, 'STOP')
                setMotorContorl(6, 5, 'STOP')
                sql = 'UPDATE u_db set u_last=0 where u_last=1'
                cursor.execute(sql)
                start = 0
                db.commit()
            
        else:
            print('sensor close')

        print(len)
        time.sleep(1)
        db.commit()
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        GPIO.cleanup()
        print(e)
