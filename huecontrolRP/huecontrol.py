import RPi.GPIO as GPIO
from time import time
import requests

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

switchUrl = 'http://192.168.1.24/api/TNNz2qfpYYwzo3KLPCMy5zpkeXWexhiRQsNwGYte/lights/1/state'
stateUrl = 'http://192.168.1.24/api/TNNz2qfpYYwzo3KLPCMy5zpkeXWexhiRQsNwGYte/lights/1/'


CODES = {
    "0xffa25d": "ON/OFF",
    "0xff629d": "PLUS",
    "0xffe21d": "STOP",
    "0xff22dd": "PREV",
    "0xff02fd": "PLAY/PAUSE",
    "0xffc23d": "NEXT",
    "0xffe01f": "DOWN",
    "0xffa857": "MINUS",
    "0xff906f": "UP",
    "0xff6897": "0",
    "0xff9867": "EQ",
    "0xffb04f": "REPT",
    "0xff30cf": "1",
    "0xff18e7": "2",
    "0xff7a85": "3",
    "0xff10ef": "4",
    "0xff38c7": "5",
    "0xff5aa5": "6",
    "0xff42bd": "7",
    "0xff4ab5": "8",
    "0xff52ad": "9",
}

def switchLight():
    res = requests.get(stateUrl).json()
    stateLight =  res['state']['on']
    
    stateMessage = 'The light is going '
    data = ''

    if stateLight:
        stateMessage = stateMessage + 'off'
        data = '{"on":false}'

    else:
        stateMessage = stateMessage + 'on'
        data = '{"on":true}'

    print stateMessage

    r = requests.put(switchUrl, data = data)

    #print r.json()

def changeBrightness(command):
    res = requests.get(stateUrl).json()
    currentBrighness =  res['state']['bri']

    stateMessage = 'Turning brightness '
    data = ''

    if currentBrighness:
        if command == 'UP':
            stateMessage = stateMessage + 'up'
            if currentBrighness + 30 <= 255:
                currentBrighness += 30
            else:
                currentBrighness = 255
            data = '{"bri":%s}' %(currentBrighness)

        elif command == 'DOWN':
            stateMessage = stateMessage + 'down'
            if currentBrighness - 30 >= 0:
                currentBrighness -= 30
            else:
                currentBrighness = 0
            data = '{"bri":%s}' %(currentBrighness)

    print stateMessage

    r = requests.put(switchUrl, data = data)


def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def binary_aquire(pin, duration):
    # aquires data as quickly as possible
    t0 = time()
    results = []
    while (time() - t0) < duration:
        results.append(GPIO.input(pin))
    return results


def on_ir_receive(pinNo, bouncetime=150):
    # when edge detect is called (which requires less CPU than constant
    # data acquisition), we acquire data as quickly as possible
    data = binary_aquire(pinNo, bouncetime/1000.0)
    if len(data) < bouncetime:
        return
    rate = len(data) / (bouncetime / 1000.0)
    pulses = []
    i_break = 0
    # detect run lengths using the acquisition rate to turn the times in to microseconds
    for i in range(1, len(data)):
        if (data[i] != data[i-1]) or (i == len(data)-1):
            pulses.append((data[i-1], int((i-i_break)/rate*1e6)))
            i_break = i
    # decode ( < 1 ms "1" pulse is a 1, > 1 ms "1" pulse is a 1, longer than 2 ms pulse is something else)
    # does not decode channel, which may be a piece of the information after the long 1 pulse in the middle
    outbin = ""
    for val, us in pulses:
        if val != 1:
            continue
        if outbin and us > 2000:
            break
        elif us < 1000:
            outbin += "0"
        elif 1000 < us < 2000:
            outbin += "1"
    try:
        return int(outbin, 2)
    except ValueError:
        # probably an empty code
        return None


def destroy():
    GPIO.cleanup()


if __name__ == "__main__":
    setup()
    try:
        print("Starting IR Listener")
        while True:
            print("Waiting for signal")
            GPIO.wait_for_edge(21, GPIO.FALLING)
            code = on_ir_receive(21)
            if code:
                key = str(hex(code))
                try:
                        inputButton = CODES[key]
                        print inputButton
                        
                        if inputButton == "UP" or inputButton == "DOWN":
                            changeBrightness(inputButton)
                        else:
                            switchLight()
                except:
                        print 'Chiave non esistente'
            else:
                print("Invalid code")
    except KeyboardInterrupt:
        pass
    except RuntimeError:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        pass
    print("Quitting")
    destroy()


