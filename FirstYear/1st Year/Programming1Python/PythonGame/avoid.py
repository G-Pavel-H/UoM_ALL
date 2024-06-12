from tkinter import *
from random import *
import time

objects = []
def configure_window():
    window.geometry("1280x720")
    window.configure(background="black")
def movetheguy(event):
    position = my_canvas.coords(theguy)
    if event.keysym == 'Left' and (position[0]-(80/2)) > 0:
        x = -25
        y = 0
        my_canvas.move(theguy, x, y)
    elif event.keysym == 'Right' and (position[0]+(80/2)) < 1280:
        x = 25
        y = 0
        my_canvas.move(theguy, x, y)
def moveobjRect():
    for i in objects:
        position_i = my_canvas.bbox(i)
        pushup = randint(720, 1000)
        pushup = 0 - pushup
        if position_i[1] >= 720:
            my_canvas.move(i, 0, pushup)
        else:
            y = 5
            my_canvas.move(i, 0, y)
    window.after(25, moveobjRect)
def checkcollision():
    for i in objects:
        positionrect = my_canvas.coords(i)
        positiontheguy = my_canvas.coords(theguy)
        if ((positionrect[0]+200) >= (positiontheguy[0]-40)) and ((positionrect[1]+100) >= (positiontheguy[1]-80)):
            print("collision detected")
        else: window.after(1, checkcollision)
def createobjects():
    global objects
    spawnrect = 0
    y = 0
    heightrect = 50
    for i in range(randint(3, 8)):
        widthrect = randint(80, 100)
        object = my_canvas.create_rectangle(spawnrect, y,(spawnrect+widthrect),
        heightrect, outline="green", fill = 'green')
        objects.append(object)
        decision = randint(0, 1)
        decrease = 300
        increase = 20
        if decision == 1:
            y -= decrease
        else:
            y += increase
        spawnrect += randint(250, 300)
        heightrect = y + 50
    return  objects
    time.sleep(25)

window = Tk()
configure_window()
my_canvas = Canvas(window, width = '1280', height = '720', bg = 'black')
my_canvas.pack()
theguyimg = PhotoImage(file="Images/theguy.png")
theguy = my_canvas.create_image(640,720, anchor=S, image=theguyimg)

for i in range(10):
    createobjects()

my_canvas.bind_all('<Key>', movetheguy)
#window.after(25, checkcollision)
window.after(100, moveobjRect)

window.mainloop()
