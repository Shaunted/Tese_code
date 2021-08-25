import tkinter as tk
from tkinter import Label, StringVar, Text, Variable, ttk, messagebox
from PIL import ImageTk, Image
import serial
from serial.tools.list_ports import comports


class SASSFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=3)
        self.config(bg='gray66', highlightthickness=2,
                    highlightbackground='black')
        self.__create_widgets()

    def callback(self, event):
        print(self.menu.get())
        self.com = self.menu.get()
        self.port = serial.Serial(self.com, 115200, timeout=2)

    def __create_widgets(self):

        # Menu Title
        self.title = Label(self, text='SASS Collector Control',
                           background='gray66', anchor='nw')
        self.title.grid(column=0, row=0, sticky='w')

        # Ports initialization and variables
        # self.ports = comports()
        # self.ports = sorted(list(self.ports))

        # Acrescentar ports do SASS2300 quando tiver
        self.aval_ports = ['/dev/ttyS3', '/dev/ttyS4']
        self.com = 0

        # Button states
        self.state_pump = True
        self.state_fan = True
        # Button images
        self.on_switch = ImageTk.PhotoImage(Image.open(
            'on_switch.png').resize((51, 51), Image.ANTIALIAS))
        self.off_switch = ImageTk.PhotoImage(Image.open(
            'off_switch.png').resize((51, 51), Image.ANTIALIAS))

        # Port listing
        # for test in self.ports:
        #     try:
        #         serial.Serial(test.device)
        #         self.aval_ports.append(test.device)
        #     except:
        #         pass
        # self.variable = StringVar(self)
        # self.variable.set(self.aval_ports[0])

        # Drop down mennu init and config
        self.menu = ttk.Combobox(
            self, values=self.aval_ports)
        self.menu.bind("<<ComboboxSelected>>", self.callback)
        self.menu.grid(row=1, columnspan=1, sticky='we', padx=(20, 0), pady=10)

        # Pump frame, label and button init
        self.pump_frame = tk.Frame(self)
        self.pump_frame.config(background='gray66')
        self.pump_frame.grid(column=0, row=2, sticky='we', padx=(20, 0))
        self.pump_label = tk.Label(
            self.pump_frame, text='Pump', background='gray66')
        self.pump_label.pack(side='left', padx=(0, 5))
        self.pump = tk.Button(self.pump_frame, background='gray66', bd=0,
                              highlightthickness=0, command=self.button_pump_command, image=self.off_switch)
        self.pump.pack(side='left')

        # Fan frame, label and button init
        self.fan_frame = tk.Frame(self)
        self.fan_frame.config(background='gray66')
        self.fan_frame.grid(column=0, row=3, sticky='we', padx=(20, 0))
        self.fan_label = tk.Label(
            self.fan_frame, text='Fan', background='gray66')
        self.fan_label.pack(side='left', padx=(0, 11))
        # self.fan_label.grid(column=0,row=3, sticky='w', padx=(20,0)
        self.fan = tk.Button(self.fan_frame, background='gray66', bd=0,
                             highlightthickness=0, command=self.button_fan_command, image=self.off_switch)
        # self.fan.grid(column=0,row=3, sticky='we', padx=0)
        self.fan.pack(side='left')

    # Button callback functions

    def button_pump_command(self):
        self.state_pump = not self.state_pump
        print(self.pump["state"])
        if self.state_pump:
            self.pump.config(image=self.off_switch)
            self.port.write('F0'.encode())
        else:
            self.pump.config(image=self.on_switch)
            self.port.write('F1'.encode())
        print(self.com)

    def button_fan_command(self):
        self.state_fan = not self.state_fan
        print(self.fan["state"])
        if self.state_fan:
            self.fan.config(image=self.off_switch)
            self.port.write('G0'.encode())
        else:
            self.fan.config(image=self.on_switch)
            self.port.write('G1'.encode())
        print(self.com)


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
        self.com = self.menu.get()
        self.port = serial.Serial(self.com, 115200, timeout=2)

    def entry_callback(self, event):
        print('oi')
        if self.com == 0:
            messagebox.showwarning('Warning', 'Please select COM port')
        else:
            self.port.write(int(self.pwm.get()).to_bytes(3, 'big'))
            print(int(self.pwm.get()))
            self.pwm.delete(0, tk.END)


    def button_command(self):
        if self.com == 0:
            messagebox.showwarning('Warning', 'Please select COM port')
        else:
            print(self.com)
            self.port.write(int(0x0).to_bytes(3, 'big'))

    def request(self):
        self.port.write(int(0xFF).to_bytes(1, 'big'))
        self.values = list(self.port.read_until())
        print(self.values)
        self.info_pwm.config(text='PWM: ' + str((self.values[5]<<8)|self.values[4]))
        print((self.values[7]<<8)|(self.values[6]))
        self.info_flow.config(text='Flow: ' + str((self.values[7]<<8)|self.values[6]))

        # values = str.splitlines()

    def __create_widgets(self):
        self.title = Label(self, text='Pump Control and View Menu',
                           background='gray66', anchor='nw')
        self.title.grid(column=0, row=0, sticky='w')

        # self.ports = comports()
        # self.ports = sorted(list(self.ports))

        # Button states
        self.state_button = True
        # Button images
        self.stop = ImageTk.PhotoImage(Image.open(
            'stop.png').resize((51, 51), Image.ANTIALIAS))

        self.aval_ports = ['/dev/ttyS14', '/dev/ttyS4']
        self.com = 0

        self.menu = ttk.Combobox(
            self, values=self.aval_ports)
        self.menu.bind("<<ComboboxSelected>>", self.callback)
        self.menu.grid(row=1, columnspan=1, sticky='we', padx=(20, 0), pady=10)

        self.entry_frame = tk.Frame(self)
        self.entry_frame.config(background='gray66')
        self.entry_frame.grid(column=0, row=3, sticky='we', padx=(20, 0))
        self.pwm_label = tk.Label(
            self.entry_frame, text='Pump speed', background='gray66')
        self.pwm_label.pack(side='left', padx=(0, 5))
        self.pwm = tk.Entry(self.entry_frame)
        self.pwm.bind('<Key-Return>', self.entry_callback)
        self.pwm.pack(side='left')
        self.button = tk.Button(self, background='gray66', bd=0,
                                highlightthickness=0, command=self.button_command, image=self.stop)
        self.button.grid(column=0, row=4, sticky='e')

        self.info_pwm = tk.Label(self, text='PWM: No value')
        self.info_pwm.grid(column=0, row=5, sticky='w')

        self.info_flow = tk.Label(self, text='Flow: No value')
        self.info_flow.grid(column=0, row=6, sticky='w')

        self.info_temp = tk.Label(self, text='Temperature: No value')
        self.info_temp.grid(column=0, row=7, sticky='w')

        self.req_button = tk.Button(
            self, text='Request information', background='gray66', command=self.request)
        self.req_button.grid(column=0, row=8, sticky='e')


# IST logo framing
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
