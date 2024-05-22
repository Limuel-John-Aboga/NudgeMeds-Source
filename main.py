# Created by the man himself, William Otsuro, probably he have a John now XD.
# Still depressed, a hater, and colder.
# Still dedicated to Arisu, and of course, Mathematics! :P
from machine import Pin
import socket
from time import sleep
import network
from ds1302 import DS1302

ds = DS1302(Pin(10), Pin(11), Pin(12)) # (CLK, DAT, RST)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ssid = 'SmartPillBox config'
password = 'root1234'
ap.config(essid=ssid, password=password)
ap.active(False)
ap.active(True)

h_addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(h_addr)
s.listen(1)

# HTML starts here ---!
page1 = """
<!DOCTYPE html>
<!-- Made by the William Otsuro, probably he have a John now XD, but definitely he's back to hack! -->
<!-- He was a part of the NudgeMeds corporation now, and not anymore a low-lifee programmer -->
<!-- Still, a follower, a hater (alexis lingad be real cringe), and still a fan of Shiina Murakami <3 -->

<html>
	<head>
		<title>
			SmartBox Configuration Web
		</title>
	</head>

	<body>
		<form action="/" method="post">
				<center>
					<br><h1>Schedules</h1><br>
					<h2>MONDAY</h2>
					<strong><label for="eventA_Mon"> Schedule for A: </label></strong>
					<input type="text" id="eventA_Mon" name="eventA_Mon" required><br>
					
					<strong><label for="eventB_Mon"> Schedule for B: </label></strong>
					<input type="text" id="eventB_Mon" name="eventB_Mon" required><br>
					
					<strong><label for="eventC_Mon"> Schedule for C: </label></strong>
					<input type="text" id="eventC_Mon" name="eventC_Mon" required><br>
					
					<strong><label for="eventD_Mon"> Schedule for D: </label></strong>
					<input type="text" id="eventD_Mon" name="eventD_Mon" required><br><br>

					<h2>TUESDAY</h2>
					<strong><label for="eventA_Tue"> Schedule for A: </label></strong>
					<input type="text" id="eventA_Tue" name="eventA_Tue" required><br>
					
					<strong><label for="eventB_Tue"> Schedule for B: </label></strong>
					<input type="text" id="eventB_Mon" name="eventB_Tue" required><br>
					
					<strong><label for="eventC_Tue"> Schedule for C: </label></strong>
					<input type="text" id="eventC_Tue" name="eventC_Tue" required><br>
					
					<strong><label for="eventD_Tue"> Schedule for D: </label></strong>
					<input type="text" id="eventD_Tue" name="eventD_Tue" required><br><br>

					<h2>WEDNESDAY</h2>
					<strong><label for="eventA_Wed"> Schedule for A: </label></strong>
					<input type="text" id="eventA_Wed" name="eventA_Wed" required><br>
					
					<strong><label for="eventB_Wed"> Schedule for B: </label></strong>
					<input type="text" id="eventB_Wed" name="eventB_Wed" required><br>
					
					<strong><label for="eventC_Wed"> Schedule for C: </label></strong>
					<input type="text" id="eventC_Wed" name="eventC_Wed" required><br>
					
					<strong><label for="eventD_Wed"> Schedule for D: </label></strong>
					<input type="text" id="eventD_Wed" name="eventD_Wed" required><br><br>

					<h2>THURSDAY</h2>
					<strong><label for="eventA_Thu"> Schedule for A: </label></strong>
					<input type="text" id="eventA_Thu" name="eventA_Thu" required><br>
					
					<strong><label for="eventB_Thu"> Schedule for B: </label></strong>
					<input type="text" id="eventB_Thu" name="eventB_Thu" required><br>
					
					<strong><label for="eventC_Thu"> Schedule for C: </label></strong>
					<input type="text" id="eventC_Thu" name="eventC_Thu" required><br>
					
					<strong><label for="eventD_Thu"> Schedule for D: </label></strong>
					<input type="text" id="eventD_Thu" name="eventD_Thu" required><br><br>

					<h2>FRIDAY</h2>
					<strong><label for="eventA_Fri"> Schedule for A: </label></strong>
					<input type="text" id="eventA_Fri" name="eventA_Fri" required><br>
					
					<strong><label for="eventB_Fri"> Schedule for B: </label></strong>
					<input type="text" id="eventB_Fri" name="eventB_Fri" required><br>
					
					<strong><label for="eventC_Fri"> Schedule for C: </label></strong>
					<input type="text" id="eventC_Fri" name="eventC_Fri" required><br>
					
					<strong><label for="eventD_Fri"> Schedule for D: </label></strong>
					<input type="text" id="eventD_Fri" name="eventD_Fri" required><br><br>
	
					<h2>SATURDAY</h2>
					<strong><label for="eventA_Sat"> Schedule for A: </label></strong>
					<input type="text" id="eventA_Sat" name="eventA_Sat" required><br>
					
					<strong><label for="eventB_Sat"> Schedule for B: </label></strong>
					<input type="text" id="eventB_Sat" name="eventB_Sat" required><br>
					
					<strong><label for="eventC_Sat"> Schedule for C: </label></strong>
					<input type="text" id="eventC_Sat" name="eventC_Sat" required><br>
					
					<strong><label for="eventD_Sat"> Schedule for D: </label></strong>
					<input type="text" id="eventD_Sat" name="eventD_Sat" required><br><br>

					<h2>SUNDAY</h2>
					<strong><label for="eventA_Sun"> Schedule for A: </label></strong>
					<input type="text" id="eventA_Sun" name="eventA_Sun" required><br>
					
					<strong><label for="eventB_Sun"> Schedule for B: </label></strong>
					<input type="text" id="eventB_Sun" name="eventB_Sun" required><br>
					
					<strong><label for="eventC_Sun"> Schedule for C: </label></strong>
					<input type="text" id="eventC_Sun" name="eventC_Sun" required><br>
					
					<strong><label for="eventD_Sun"> Schedule for D: </label></strong>
					<input type="text" id="eventD_Sun" name="eventD_Sun" required><br>
	
					<br><input type="submit" value="Submit"><br><br>
		
				</center>
			</div>
		</form>
	</body>
</html>
"""

page2 = """
<!DOCTYPE html>
<hmtl>
    <body>
        <h1>Thank you, you may close the website now!</h1>
    </body>
</html>
"""
# HTML ends here ---!

request2 = ""
# Webserver hosting
while True:
    try:
        client, addr = s.accept()
        request1 = client.recv(4096)
        request1 = str(request1)
        pos_POST = request1.find("POST")
        
        if pos_POST == 2:
            request2 = client.recv(4096)
            response = page2
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            client.send(response)
            client.close()
            s.close()
            ap.active(False)
                
            break

        response = page1
        client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        client.send(response)
        client.close()
        
    except:
        break

# value function
def values(alpha, week, req):
    val = "event" + str(alpha) + "_" + str(week) + "="
    finder = req.find(val)
    value = req[finder + 11] + req[finder + 12] + ":" + req[finder + 16] + req[finder + 17] + " " + req[finder + 19] + req[finder + 20]  

    return value

request = str(request1) + str(request2)
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

#time function
def week():
    week = ds.weekday()
    if week == 7:
        ds.weekday(weekday=0)
        
        week = ds.weekday
        
    return week
    
def time():
    hour = ds.hour()
    meridiem = "AM"
    if ds.hour() > 12:
        hour = ds.hour() - 12
        meridiem = "PM"
    if ds.hour() == 0:
        hour = ds.hour() + 12
    if len(str(hour)) != 2:
        hour = "0" + str(hour)
        
    time = str(hour) + ":" + str(ds.minute()) + " " + meridiem
    
    return time

constant = 99
while True:
    while week() == constant:
        pass
    
    list = sched[week()]
    
    for i in list:
        while True:
            if time() == i:
                print("Alarm XDFC!")
                
                break
    constant = week()
    
            