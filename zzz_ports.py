# # import serial
# # from serial.tools.list_ports import comports
# # import os


# # ports = comports()

# # ports = comports()
# # ports = list(ports)
# # ports = sorted(ports)

# # print(type(ports[0].device))

# # for test in ports:
# #         try:
# #                 serial.Serial(test.device)
# #         except:
# #                 pass
# # # for test in ports:
# # #         if serial.Serial(test) != 'SerialException: Could not configure port: (5, \'Input/output error\')':
# # #                 print('oi')
# # # os.system('for tty in /dev/ttyS*; do stty -F $tty -a; done')


# from tkinter import *
# from tkinter import messagebox

# ws = Tk()
# ws.title('PythonGuides')
# ws.geometry('400x300')
# ws.config(bg='#4a7a8c')

# def askQuestion():
#     reply = messagebox.askyesno('confirmation', 'Are you sure you want to donate $10000 ?')
#     if reply == True:
#         messagebox.showinfo('successful','You are the Best!')
#     else:
#         messagebox.showinfo('', 'Maybe next time!')
       

# def askYesNo():
#     reply = messagebox.askyesno('confirmation', 'Do you want to quit this application?')
#     if reply == True:
#         messagebox.showinfo('exiting..', 'exiting application')
#         ws.destroy()
#     else:
#         messagebox.showinfo('', 'Thanks for Staying')
       

# btn1 = Button(
#     ws,
#     text='Transfer',
#     command=askQuestion,
#     padx=15,
#     pady=5
# )
# btn1.pack(expand=True, side=LEFT)

# btn2 = Button(
#     ws,
#     text='Exit',
#     command=askYesNo,
#     padx=20,
#     pady=5
# )
# btn2.pack(expand=True, side=RIGHT)

# ws.mainloop()


import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.