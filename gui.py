import serial.tools.list_ports
from tkinter import *
from tkinter import Tk
import winsound


ports = serial.tools.list_ports.comports()
serial_pico = serial.Serial()

port = "COM3"



serial_pico.baudrate = 115200
serial_pico.port = port
serial_pico.open()



points1 = 0
points2 = 0
kto_zaczyna = 1  # 1 - gracz 1 , 2 - gracz 2
fullscr = False

def serv(kto):
    global kto_zaczyna, points1, points2

    if points1 >= 10 and points2 >= 10:
        po_ile = 1
    else:
        po_ile = 3

    if kto == 0:
        return 0

    suma = points1 + points2

    kolejka = (suma // po_ile) + 1
    if kto_zaczyna == 1:
        if kolejka % 2 == 0:    #parzysta : serv ten kto zaczynał 
            if kto == 1:
                return 0
            else:
                return po_ile - (suma % po_ile) 
            
        else:                   #nieparzysta : serv ten któr nie zaczynał 
            if kto == 1:
                return po_ile - (suma % po_ile)
            else:
                return 0  
              
    elif kto_zaczyna == 2:

        if kolejka % 2 == 0:    #parzysta : serv ten kto zaczynał 
            if kto == 1:
                return po_ile - (suma % po_ile)
            else:
                return 0 
            
        else:                   #nieparzysta : serv ten któr nie zaczynał 
            if kto == 1:
                return 0
            else:
                return po_ile - (suma % po_ile) 
            

def zmiana():
    global  points1, points2
    points1_val.set(points1)
    points2_val.set(points2) 
    player1_serv.set(serv(1))
    player2_serv.set(serv(2)) 
    

def task():

    global points1, points2, kto_zaczyna


    if serial_pico.in_waiting:
        packet = serial_pico.readline()
        data = packet.decode('utf').rstrip('\n')

        clear_data = ""

        for i in data:
            if i != '\r':
                clear_data += i 
        if clear_data == "player_1_up":
            winsound.Beep(1000, 250)
            points1 += 1
            zmiana()
            

        if clear_data == "player_2_up":
            winsound.Beep(1000, 250)
            points2 += 1
            zmiana()


        if clear_data == "player_1_down" and points1 > 0:
            winsound.Beep(600, 300)
            points1 -= 1
            zmiana()            

        if clear_data == "player_2_down" and points2 > 0:
            winsound.Beep(600, 300)
            points2 -= 1
            zmiana()

        if clear_data == "reset":
            winsound.Beep(1500, 500)
            points2 = 0
            points1 = 0
            player1_serv.set(serv(0))
            player2_serv.set(serv(0))
            zmiana()

        if points1 >= 11 and points1 > points2:
            if points1 >= 10 and points2 >= 10:
                if points1 - points2 > 1:
                    state1.set("Wygrana")
                    state2.set("Przegrana")
                else:
                    state1.set("")
                    state2.set("")                     
            else:
                state1.set("Wygrana")
                state2.set("Przegrana")    

        elif points2 >= 11 and points2 > points1:
            if points1 >= 10 and points2 >= 10:
                if points2 - points1 > 1:
                    state2.set("Wygrana")
                    state1.set("Przegrana")
                else:
                    state1.set("")
                    state2.set("")    
            else:
                state2.set("Wygrana")
                state1.set("Przegrana")         
        else:
            state1.set("")
            state2.set("")    

        if points1 == 0 and points2 == 0:
            if clear_data == "player_1_down" and kto_zaczyna == 2:
                kto_zaczyna = 1
                winsound.Beep(600, 400)
            if clear_data == "player_2_down" and kto_zaczyna == 1:
                kto_zaczyna = 2
                winsound.Beep(600, 400)
        


        zmiana()

  

    root.after(10, task)

def reset ():
    global points1, points2

    winsound.Beep(1500, 500)
    points2 = 0
    points1 = 0
    player1_serv.set(serv(0))
    player2_serv.set(serv(0))
    zmiana()


root = Tk()

points1_val = StringVar()
points2_val = StringVar()

points1_val.set(points1)
points2_val.set(points2)

player1_serv = StringVar()
player2_serv= StringVar()

state1 = StringVar()
state2 = StringVar()

state1.set("")
state2.set("")


player1_serv.set(serv(1))
player2_serv.set(serv(2))

root.title("Ping Pong")
root.geometry("1500x900")


root.configure(background = "white")




gracz1_pkt = Label(root, textvariable = points1_val,font="Times 300",bg="white")
gracz1_pkt.place(x = 150, y = 10)

gracz2_pkt = Label(root, textvariable = points2_val, font="Times 300",bg="white")
gracz2_pkt.place(x = 950, y = 10)


gracz1_serv = Label(root, textvariable = player1_serv,font="Times 180")
gracz1_serv.place(x = 200, y = 500)

gracz2_serv = Label(root, textvariable = player2_serv, font="Times 180")
gracz2_serv.place(x = 1000, y = 500)


gracz1_win = Label(root, textvariable = state1,font="Times 50",bg="white")
gracz1_win.place(x = 200, y = 400)

gracz2_win = Label(root, textvariable = state2, font="Times 50",bg="white")
gracz2_win.place(x = 1000, y = 400)

reset_button = Button(root, text = "Reset", command = reset)
reset_button.place(x = 600, y = 400)

root.after(10, task)

root.mainloop()