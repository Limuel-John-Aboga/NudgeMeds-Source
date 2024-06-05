# Created by the man himself, William Otsuro, probably he have a John now XD.
# Still depressed, a hater, and colder.
# Still dedicated to Arisu, and of course, Mathematics! :P
# Thank you to the people who appreciated our product!
from machine import Pin
import socket
from time import sleep
import network
from ds1302 import DS1302
import stepper


ds = DS1302(Pin(10), Pin(11), Pin(12)) #(CLK, DAT, RST)
alarm = Pin(15, Pin.OUT)
motor = stepper.HalfStepMotor.frompins(16, 17, 18, 19)
    
data = open("data.txt", "r").readlines()
ssid = data[0].replace("\n", "")
password = data[1]
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
ap.active(False)
ap.active(True)

h_addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(h_addr)
s.listen(1)
while True:
    try:
        client, addr = s.accept()
        request = client.recv(4096)
        response = open("home.html", "r").read()
        if str(request).find("POST") != -1:
            if str(request).find("/config") != -1:
                p_request = str(request) + "%%"
                pos_eq = p_request.find("ssid=")
                pos_am = p_request.find("&password=")
                pos_pe = p_request.find("'%%")
                ssid = ""
                password = ""
                for i in range(pos_eq + 5, pos_am):
                    ssid = ssid + p_request[i]
                for i in range(pos_am + 10, pos_pe):
                    password = password + p_request[i]
                f = open("data.txt", "w")
                f.write(ssid + "\n")
                f.close()
                f = open("data.txt", "a")
                f.write(password)
                f.close()
                response = open("closing-wf.html", "r").read()    
            if str(request).find("/schedule") != -1:
                p_request = client.recv(4096)
                client.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
                client.send(open("closing-sc.html", "r").read())
                client.close()
                s.close()
                ap.active(False)
                break
        if str(request).find("GET") != -1:
            if str(request).find("/config") != -1:
                response = open("config.html", "r").read()
            if str(request).find("/schedule") != -1:
                response = open("schedule.html", "r").read()
            if str(request).find("/report") != -1:
                response = open("report.html", "r").read()
            if str(request).find("/home") != -1:
                response = open("home.html", "r").read()
            if str(request).find("/manual") != -1:
                response = open("manual.html", "r").read()
            if str(request).find("/update") != -1:
                response = open("update.html", "r").read()
        client.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        client.send(response)
        client.close()
        
    except:
        break

def values(alpha, week, req):
    val = "event" + str(alpha) + "_" + str(week) + "="
    finder = req.find(val)
    value = req[finder + 11] + req[finder + 12] + ":" + req[finder + 16] + req[finder + 17] + " " + req[finder + 19] + req[finder + 20]
    if req[finder + 20] == "&":
        value = "0" + req[finder + 11] + ":" + req[finder + 15] + req[finder + 16] + " " + req[finder + 18] + req[finder + 19]
    if req[finder + 11].upper() == "N":
        value = "None"

    return value

request = str(request) + str(p_request)
request = request.replace("'b'", "")
request = request.replace("'", "&")
sched = []
schedules = []
weeks = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
alpha = ["A", "B", "C", "D"]

print(request)

const = 0
for w in weeks:
    for a in alpha:
        schedules.append(values(a, w, request))
    sched.append(schedules)
    schedules = []

def week():
    week = ds.weekday()
    if week == 7:
        ds.weekday(weekday=0)
        
        week = ds.weekday
        
    return week
    
def time():
    hour = ds.hour()
    minute = ds.minute()
    meridiem = "AM"
    if ds.hour() > 12:
        hour = ds.hour() - 12
        meridiem = "PM"
    if ds.hour() == 0:
        hour = ds.hour() + 12
    if len(str(hour)) != 2:
        hour = "0" + str(hour)
    if len(str(minute)) != 2:
        minute = "0" + str(minute)
        
    time = str(hour) + ":" + str(minute) + " " + meridiem
    
    return time

motor.reset()
constant = 99
m_const = 0
angle = 0
val = 1
a_const = True
while True:
    while week() == constant:
        pass
    
    list = sched[week()]
    
    for i in list:
        while True:
            if i == "None":
                i = time()
                a_const = False
            if time() == i.upper():
                if m_const == 0:
                    angle = 75
                if m_const == 1:
                    angle = 140
                if m_const == 2:
                    angle = 230
                if m_const == 3:
                    angle = 285
                motor.step_until_angle(angle)
                if a_const == False:
                    val = 0
                alarm.value(val)
                sleep(5)
                alarm.value(0)
                val = 1
                m_const = m_const + 1
                break
                
    motor.step_until_angle(0)
    constant = week()
    m_const = 0