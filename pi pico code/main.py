from machine import Pin
import time

led = Pin(25,Pin.OUT)
button_1 = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_2 = Pin(17, Pin.IN, Pin.PULL_DOWN)

#kto zaczyna
while True:
    if button_1.value():
        print("zaczyna gracz 1")
        break
    elif button_2.value():
        print("zaczyna gracz 2")
        break
    
time.sleep(1)

counter = 0

while True:
    
    #obsługa gracza 1 
    if button_1.value():
        time.sleep(0.01)
        if button_1.value():
            while True:
                counter += 1
                if button_1.value() == 0 and counter <= 150:
                    print("player_1_up")
                    break
                    
                if button_1.value() and button_2.value() == 0 and counter > 150:
                    print("player_1_down")
                    break
                
                if button_1.value() and button_2.value() and counter > 300:
                    print("reset")
                    break
                
                time.sleep(0.01)
        time.sleep(0.5)        
        while button_1.value() or button_2.value():
            time.sleep(0.01)
                
                
        counter = 0          
                
    #obsługa gracza 2 
    if button_2.value():
        time.sleep(0.01)
        if button_2.value():
            while True:
                counter += 1
                if button_2.value() == 0 and counter <= 150:
                    print("player_2_up")
                    break
                    
                if button_2.value() and button_1.value() == 0 and counter > 150:
                    print("player_2_down")
                    break
                
                if button_2.value() and button_1.value() and counter > 300:
                    print("reset")
                    break
                
                time.sleep(0.01)
            time.sleep(0.5)    
            while button_1.value() or button_2.value():
                time.sleep(0.01)
                
        counter = 0              
                
                
                