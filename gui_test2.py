import tkinter as tk
from tkinter import Label, StringVar, Text, Variable, ttk
from PIL import ImageTk, Image
import serial
from serial.tools.list_ports import comports


class SASSFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.config(bg='gray66', highlightthickness=2,
                    highlightbackground='black')
        self.__create_widgets()

    def callback(self, event):
        print(self.menu.get())
        self.com = self.menu.get()

    def __create_widgets(self):
        self.title = Label(self, text='SASS Collector Control',
                           background='gray66', anchor='nw')
        self.title.grid(column=0,row=0)

        self.ports = comports()
        self.ports = sorted(list(self.ports))

        self.aval_ports = []
        self.com = 0

        self.state_pump = True
        self.state_fan = True

        self.on_switch = ImageTk.PhotoImage(Image.open(
            'on_switch.png').resize((51,51), Image.ANTIALIAS))
        self.off_switch = ImageTk.PhotoImage(Image.open(
            'off_switch.png').resize((51,51), Image.ANTIALIAS))


        for test in self.ports:
            try:
                serial.Serial(test.device)
                self.aval_ports.append(test.device)
            except:
                pass
        # self.variable = StringVar(self)
        # self.variable.set(self.aval_ports[0])

        self.menu = ttk.Combobox(
            self, values=self.aval_ports)
        self.menu.bind("<<ComboboxSelected>>", self.callback)
        self.menu.grid(row=1,columnspan=2, sticky='e')

        self.pump_label = tk.Label(self, text='Pump', background='gray66').grid(column=0,row=2, columnspan=2, sticky='we')
        self.pump = tk.Button(self, background='gray66', bd=0,highlightthickness=0 ,command=self.button_pump_command, image=self.on_switch)
        self.pump.grid(column=0,row=2,columnspan=2, sticky='e')

        self.fan_label = tk.Label(self, text='Fan', background='gray66').grid(column=0,row=3, columnspan=2, sticky='we')
        self.fan = tk.Button(self, background='gray66', bd=0, highlightthickness=0,command=self.button_fan_command, image=self.on_switch)
        self.fan.grid(column=0,row=3,columnspan=2, sticky='e')



        # for widget in self.winfo_children():
        #     if widget != self.title:
        #         if widget == (self.pump) or (self.fan):
        #             widget.grid(padx=(0,0), pady=(10, 0))   
        #         else:                
        #             widget.grid(padx=(30,5), pady=(10, 0))

    def button_pump_command(self):
        self.state_pump = not self.state_pump
        print(self.pump["state"])
        if self.state_pump:
            self.pump.config(image=self.on_switch)
        else:
            self.pump.config(image=self.off_switch)
        print(self.com)

    def button_fan_command(self):
        self.state_fan = not self.state_fan
        print(self.fan["state"])
        if self.state_fan:
            self.fan.config(image=self.on_switch)
        else:
            self.fan.config(image=self.off_switch)
        print(self.com)

        # # Find what
        # tk.Label(self, text='Find what:').grid(column=0, row=0, sticky=tk.W)
        # keyword = tk.Entry(self, width=30)
        # keyword.focus()
        # keyword.grid(column=1, row=0, sticky=tk.W)

        # # Replace with:
        # tk.Label(self, text='Replace with:').grid(
        #     column=0, row=1, sticky=tk.W)
        # replacement = tk.Entry(self, width=30)
        # replacement.grid(column=1, row=1, sticky=tk.W)

        # # Match Case checkbox
        # match_case = tk.StringVar()
        # match_case_check = tk.Checkbutton(
        #     self,
        #     text='Match case',
        #     variable=match_case,
        #     command=lambda: print(match_case.get()))
        # match_case_check.grid(column=0, row=2, sticky=tk.W)

        # # Wrap Around checkbox
        # wrap_around = tk.StringVar()
        # wrap_around_check = tk.Checkbutton(
        #     self,
        #     variable=wrap_around,
        #     text='Wrap around',
        #     command=lambda: print(wrap_around.get()))
        # wrap_around_check.grid(column=0, row=3, sticky=tk.W)


class PUMPFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.config(bg='gray66', highlightthickness=2,
                    highlightbackground='black')
        self.__create_widgets()

    def callback(self, event):
        print(self.menu.get())

    def __create_widgets(self):
        self.title = Label(self, text='Pump Control and View Menu',
                           background='gray66', anchor='nw')
        self.title.pack(fill='x')

        self.ports = comports()
        self.ports = sorted(list(self.ports))

        self.aval_ports = []

        for test in self.ports:
            try:
                serial.Serial(test.device)
                self.aval_ports.append(test.device)
            except:
                pass

        # self.variable = StringVar(self)
        # self.variable.set(self.aval_ports[0])

        self.menu = ttk.Combobox(
            self, values=self.aval_ports)
        self.menu.bind("<<ComboboxSelected>>", self.callback)
        self.menu.pack()

        for widget in self.winfo_children():
            if widget != self.title:
                widget.pack(padx=30, pady=10)

    # def __create_widgets(self):
    #     tk.Button(self, text='Find Next').grid(column=0, row=0)
    #     tk.Button(self, text='Replace').grid(column=0, row=1)
    #     tk.Button(self, text='Replace All').grid(column=0, row=2)
    #     tk.Button(self, text='Cancel').grid(column=0, row=3)

    #     # for widget in self.winfo_children():
    #     #     widget.grid(padx=0, pady=3)


class LogoFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()

    def __create_widgets(self):
        self.img = ImageTk.PhotoImage(Image.open(
            'ist.png').resize((250, 97), Image.ANTIALIAS))
        self.canvas = tk.Canvas(
            self, bg="gray66", width=250, height=97, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.img, anchor='nw')


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SASS/Pump control system')
        # self.geometry('400x150')

        # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        # background of the root window
        self.config(bg='gray66')

        self.__create_widgets()

    def __create_widgets(self):

        # create the input frame
        input_frame = SASSFrame(self)
        input_frame.grid(column=0, row=1, sticky='sw')

        # create the button frame
        button_frame = PUMPFrame(self)
        button_frame.grid(column=1, row=0, sticky='ne')

        logo_frame = LogoFrame(self)
        logo_frame.grid(column=0, row=0, sticky='nw')

        for widget in self.winfo_children():
            # if widget != logo_frame:
            widget.grid(padx=30, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
