from gpiozero import Button, OutputDevice
import time
import requests

maglock = OutputDevice(4)
release = Button(17)
URL = "http://192.168.43.33:1880/door-access/validate"

# URL = "http://192.168.43.188:1880/booking/form"

maglock.off()
# maglock.on()
# time.sleep(5)
def opendoor():
    maglock.on()
    print("DOOR IS OPEN")
    time.sleep(10)
    maglock.off()
    print("DOOR IS LOCKED")

def button_open():
    maglock.on()
    print("DOOR IS OPEN")
    time.sleep(10)
    maglock.off()
    print("DOOR IS LOCKED")

while True:
    release.when_pressed = button_open
    time.sleep(0.1)
    access_id = input("Please your access id: ")
    print(access_id)
    # print(type(booking_id))

    PARAMS = {'access_id':access_id}
    r = requests.post(url = URL, json = PARAMS) 
    data = r.json()
    access = data[0]['access_id']
    print(access) 

    if access_id == access:
        opendoor()
    else:
        print("Unknown ticket")