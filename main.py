# Created by the man himself, William Otsuro, probably he have a John now XD.
# Still depressed, a hater, and colder.
# Still dedicated to Arisu, and of course, Mathematics! :P
# As of May 23, 2024, this code is dedicated to all whom teachers who voted for us to be in expo!
# This is the real trademark of Limuel John Aboga, with the bytename, William John Otsuro
from machine import Pin, PWM
import socket
from time import sleep
import network
from ds1302 import DS1302

ds = DS1302(Pin(10), Pin(11), Pin(12)) # (CLK, DAT, RST)
alarm = Pin(15, Pin.OUT)
m1_ln4 = PWM(Pin(16))
m1_ln3 = PWM(Pin(17))
m2_ln2 = PWM(Pin(18))
m2_ln1 = PWM(Pin(19))
m3_ln4 = PWM(Pin(20))
m3_ln3 = PWM(Pin(21))
m4_ln2 = PWM(Pin(22))
m4_ln1 = PWM(Pin(26))

m1_ln4.frequency(1000)
m1_ln3.frequency(1000)
m2_ln2.frequency(1000)
m2_ln1.frequency(1000)
m3_ln4.frequency(1000)
m3_ln3.frequency(1000)
m4_ln2.frequency(1000)
m4_ln1.frequency(1000)

#max is 65025
def run_m(mach, ln_even, ln_odd):
    if mach == 1:
        m1_ln4.duty(ln_even)
        m1_ln3.duty(ln_odd)
    if mach == 2:
        m2_ln2.duty(ln_even)
        m2_ln1.duty(ln_odd)
    if mach == 3:
        m3_ln4.duty(ln_even)
        m3_ln3.duty(ln_odd)
    if mach == 4:
        m4_ln2.duty(ln_even)
        m4_ln1.duty(ln_odd)

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
        print(f"{request}\n")
        
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

    return value

request = str(request) + str(p_request)
request = request.replace("'b'", "")
sched = []
schedules = []
weeks = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
alpha = ["A", "B", "C", "D"]

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

print(sched)
constant = 99
m_constant = 0
run = 0
while True:
    while week() == constant:
        pass
    
    list = sched[week()]
    
    for i in list:
        while True:
            if time() == i.upper():
                if m_constant == 0:
                    run_m(1, 0, 65025)
                    sleep(5)
                    run_m(1, 0, 0)
                if m_constant == 1:
                    run_m(2, 65025, 0)
                    sleep(5)
                    run_m(2, 0, 0)
                if m_constant == 2:
                    run_m(3, 0, 65025)
                    sleep(5)
                    run_m(3, 0, 0)
                if m_constant == 3:
                    run_m(4, 65025, 0)
                    sleep(5)
                    run_m4(4, 0, 0)
                    m_constant = -1
                m_constant = m_constant + 1
                alarm.high()
                sleep(10)
                
                alarm.low()
                
                break
    constant = week()
    run = run + 1
    if run == 6:
        run = 0
        machs_e = [2, 4]
        machs_o = [1, 3]
        for i in machs_o:
            run_m(i, 65025, 0)
        for i in machs_e:
            run_m(i, 0, 65025)
        sleep(5)
        machs = machs_e + machs_o
        for i in machs:
            run_m(i, 0, 0)