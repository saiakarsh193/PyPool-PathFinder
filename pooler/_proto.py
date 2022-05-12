import tkinter as tk
from utils import *

mainwindow = tk.Tk()
mainwindow.title('Pool Sim')
mainwindow.geometry('1200x600')
mainwindow.config(bg=colToHash(255, 0, 0))
canvas_width = 1000
canvas_height = 500
cnv = tk.Canvas(master=mainwindow, width=canvas_width, height=canvas_height, bg=colToHash(100))
cnv.place(x=10, y=10)
# cnv.create_line(0, 0, 100, 100, fill=colToHash(0, 0, 255), arrow='last')
rec1 = cnv.create_rectangle(100, 100, 300, 300, activefill=colToHash(0, 200, 0))

def task():
    print(1)
    cnv.move(rec1, 50, 0)
    # mainwindow.update()
    mainwindow.after(2000, task)

mainwindow.after(2000, task)
mainwindow.mainloop()