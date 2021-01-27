import tkinter as tk
from tkinter import *
import sys, time
sys.path.append("..")
from hardwareinterface.HwInterface import HwInterface
from decimal import Decimal

# przygotuj modul do komunikacji
hardWareInt = HwInterface()
hardWareInt.port = 'COM7'
hardWareInt.openComm()
# przejdz jeden cykl komunikacji dla wyczyszczenia bufora
hardWareInt.measTemp()
time.sleep(1)
meas = hardWareInt.getTemp()

HEIGHT = 500
WIDTH = 600
dane = []


def Start_measurement(L5,T1,T2,T3,T4,T5,C1,C2,C3,C4):

    time_range=Value_get(T5)
    time_stamp=0
    num=0

    t1=Decimal(Value_get(T1))
    t2=Decimal(Value_get(T2))
    t3=Decimal(Value_get(T3))
    t4=Decimal(Value_get(T4))

    for time_stamp in range (time_range):
        #!!!!!!!!!!!!!!!
        #wywolanie funkcji measAndGetTemp()
        hardWareInt.measTemp()
        time.sleep(1)
        meas = hardWareInt.getTemp()
        dane.append(meas) #przykladowo wpisuje time_stamp

        C1.update()
        C2.update()
        C3.update()
        C4.update()


        if dane[time_stamp]>=t1:
            C1.config(bg="red")
        else:
            C1.config(bg="light gray")
        if dane[time_stamp]>=t2:
            C2.config(bg="red")
        else:
            C2.config(bg="light gray")
        if dane[time_stamp]>=t3:
            C3.config(bg="red")
        else:
            C3.config(bg="light gray")
        if dane[time_stamp]>=t4:
            C4.config(bg="red")
        else:
            C4.config(bg="light gray")


        L5.config(text=str(dane[time_stamp]))
        L5.update()

        time_stamp=time_stamp+1

    f = open("dane.txt", "w")
    for num in range(time_range):
        f.write("\n")
        f.write(str(dane[num]))
        num = num + 1
    f.close()



def Value_get(T):
    string_answer = T.get()
    int_answer = int(string_answer)
    return int_answer


root = tk.Tk()

root.title('Termometr')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='light gray')
canvas.pack()

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.33, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)


L5 = tk.Label(root, bd =5, bg="light grey")
L5.place(relx=0.51, rely=0.625, relwidth=0.29, relheight=0.2)

# Entry places
T1 = Entry(root, bd =5)
T1.place(relx=0.3, rely=0.45, relwidth=0.05, relheight=0.05)
T2 = Entry(root, bd =5)
T2.place(relx=0.3, rely=0.55, relwidth=0.05, relheight=0.05)
T3 = Entry(root, bd =5)
T3.place(relx=0.3, rely=0.65, relwidth=0.05, relheight=0.05)
T4 = Entry(root, bd =5)
T4.place(relx=0.3, rely=0.75, relwidth=0.05, relheight=0.05)
T5 = Entry(root, bd =5)
T5.place(relx=0.7, rely=0.45, relwidth=0.05, relheight=0.05)

# Sygnals
C1 = tk.Canvas(root, bg="light grey", height=10, width=10)
oval1 = C1.create_oval(1, 1, 1, 1)
C1.place(relx=0.2, rely=0.45, relwidth=0.05, relheight=0.05)
C2 = tk.Canvas(root, bg="light grey", height=10, width=10)
oval1 = C2.create_oval(1, 1, 1, 1)
C2.place(relx=0.2, rely=0.55, relwidth=0.05, relheight=0.05)
C3 = tk.Canvas(root, bg="light grey", height=10, width=10)
oval1 = C3.create_oval(1, 1, 1, 1)
C3.place(relx=0.2, rely=0.65, relwidth=0.05, relheight=0.05)
C4 = tk.Canvas(root, bg="light grey", height=10, width=10)
oval1 = C4.create_oval(1, 1, 1, 1)
C4.place(relx=0.2, rely=0.75, relwidth=0.05, relheight=0.05)


# Buttons
Start_button = tk.Button(root, text="Start", bd = 5, command=lambda:Start_measurement(L5,T1,T2,T3,T4,T5,C1,C2,C3,C4))
Start_button.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.1)

var = StringVar()
var.set("Celsius")
L1 = tk.Label(root, bd =5, textvariable=var)
L1.place(relx=0.35, rely=0.45, relwidth=0.1, relheight=0.05)
L2 = tk.Label(root, bd =5, textvariable=var)
L2.place(relx=0.35, rely=0.55, relwidth=0.1, relheight=0.05)
L3 = tk.Label(root, bd =5, textvariable=var)
L3.place(relx=0.35, rely=0.65, relwidth=0.1, relheight=0.05)
L4 = tk.Label(root, bd =5, textvariable=var)
L4.place(relx=0.35, rely=0.75, relwidth=0.1, relheight=0.05)

var1 = StringVar()
var1.set("Measurement in Celsius:")
L6 = tk.Label(root, bd =5, textvariable=var1)
L6.place(relx=0.5, rely=0.55, relwidth=0.3, relheight=0.05)

var2 = StringVar()
var2.set("Time set in sec:")
L7 = tk.Label(root, bd =5, textvariable=var2)
L7.place(relx=0.5, rely=0.45, relwidth=0.2, relheight=0.05)


root.mainloop()
