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

    #############################################
    #   Drop down menu callback function.       #
    #   Gets value chosen in the menu           #
    #   and opens serial port with that value   #
    def callback(self, event):
        print(self.menu.get())
        self.com = self.menu.get()
        self.port = serial.Serial(self.com, 115200, timeout=2)


    #############################
    # Button callback functions #
    #############################

    #########################################################
    #   Pump button                                          #
    #   Checks if comport was chosen, if not issues warning #
    #   Switches images depending on the state              #
    #   If off-to-on, sends turning on command              #
    #   If opposite sends turning off command               #
    def button_pump_command(self):
        if self.com == 0:
            messagebox.showwarning('Warning', 'Please select COM port')
        else:
            self.state_pump = not self.state_pump    
            if self.state_pump:     # Checks state variable to check if on or off
                self.pump.config(image=self.off_switch)
                self.port.write('F0'.encode())
            else:
                self.pump.config(image=self.on_switch)
                self.port.write('F1'.encode())


    #########################################################
    #   Fan button                                          #
    #   Checks if comport was chosen, if not issues warning #
    #   Switches images depending on the state              #
    #   If off-to-on, sends turning on command              #
    #   If opposite sends turning off command               #
    def button_fan_command(self):
        if self.com == 0:
            messagebox.showwarning('Warning', 'Please select COM port')
        else:
            self.state_fan = not self.state_fan
            if self.state_fan:     # Checks state variable to check if on or off
                self.fan.config(image=self.off_switch)
                self.port.write('G0'.encode())
            else:
                self.fan.config(image=self.on_switch)
                self.port.write('G1'.encode())

    def __create_widgets(self):

        # Menu Title
        self.title = Label(self, text='SASS Collector Control',
                           background='gray66', anchor='nw')
        self.title.grid(column=0, row=0, sticky='w')

        # List containing COM ports
        self.aval_ports = ['/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3', '/dev/ttyS4', '/dev/ttyS5', '/dev/ttyS6', '/dev/ttyS7',
                           '/dev/ttyS8', '/dev/ttyS9', '/dev/ttyS10', '/dev/ttyS11', '/dev/ttyS12', '/dev/ttyS13', '/dev/ttyS14', '/dev/ttyS15',
                           '/dev/ttyS16', '/dev/ttyS17', '/dev/ttyS18', '/dev/ttyS19', '/dev/ttyS20']

        # Variable to check if comport chosen or not
        self.com = 0

        # Button states
        self.state_pump = True
        self.state_fan = True
        # Button images
        self.on_switch = ImageTk.PhotoImage(Image.open(
            'on_switch.png').resize((51, 51), Image.ANTIALIAS))
        self.off_switch = ImageTk.PhotoImage(Image.open(
            'off_switch.png').resize((51, 51), Image.ANTIALIAS))

        # Drop down mennu init and config
        self.menu = ttk.Combobox(
            self, values=self.aval_ports)
        self.menu.set('Please choose the COM port')
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
        self.fan = tk.Button(self.fan_frame, background='gray66', bd=0,
                             highlightthickness=0, command=self.button_fan_command, image=self.off_switch)
        self.fan.pack(side='left')



class PUMPFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.config(bg='gray66', highlightthickness=2,
                    highlightbackground='black')
        self.__create_widgets()


    #############################################
    #   Drop down menu callback function.       #
    #   Gets value chosen in the menu           #
    #   and opens serial port with that value   #
    def callback(self, event):
        print(self.menu.get())
        self.com = self.menu.get()
        self.port = serial.Serial(self.com, 115200, timeout=2)

    #########################################################
    #   Stop button callback function                       #
    #   Checks if comport chosen, if not, issue warning     #
    #   Sends written value to serial port                  #
    def entry_callback(self, event):
        if self.com == 0:
            messagebox.showwarning('Warning', 'Please select COM port')
        else:
            self.port.write(int(self.pwm.get()).to_bytes(3, 'big'))
            self.pwm.delete(0, tk.END)


    #########################################################
    #   Stop button callback function                       #
    #   Checks if comport chosen, if not, issue warning     #
    #   Sends value 0 to turn off pump                      #
    def button_command(self):
        if self.com == 0:
            messagebox.showwarning('Warning', 'Please select COM port')
        else:
            self.port.write(int(0x0).to_bytes(3, 'big'))


    #########################################################
    #   Request button callback function                    #
    #   Checks if comport chosen, if not, issue warning     #
    #   Sends request message and reads the received info   #
    #   and then displays it on the info menu               #
    def request(self):
        if self.com == 0:
            messagebox.showwarning('Warning', 'Please select COM port')
        else:
            self.port.write(int(0xFF).to_bytes(1, 'big'))
            self.values = list(self.port.read_until())
            self.info_pwm.config(text='PWM: ' + str((self.values[5]<<8)|self.values[4]))
            self.info_flow.config(text='Flow: ' + str((self.values[7]<<8)|self.values[6]))


    def __create_widgets(self):
        self.title = Label(self, text='Pump Control and View Menu',
                           background='gray66', anchor='nw')
        self.title.grid(column=0, row=0, sticky='w')
        
        # Button states
        self.state_button = True
        # Button images
        self.stop = ImageTk.PhotoImage(Image.open(
            'stop.png').resize((51, 51), Image.ANTIALIAS))


        # List containing COM ports
        self.aval_ports = ['/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3', '/dev/ttyS4', '/dev/ttyS5', '/dev/ttyS6', '/dev/ttyS7',
                           '/dev/ttyS8', '/dev/ttyS9', '/dev/ttyS10', '/dev/ttyS11', '/dev/ttyS12', '/dev/ttyS13', '/dev/ttyS14', '/dev/ttyS15',
                           '/dev/ttyS16', '/dev/ttyS17', '/dev/ttyS18', '/dev/ttyS19', '/dev/ttyS20']
        
        # Variable to check if comport chosen or not        
        self.com = 0


        # Drop down mennu init and config
        self.menu = ttk.Combobox(
            self, values=self.aval_ports)
        self.menu.set('Please choose the COM port')
        self.menu.bind("<<ComboboxSelected>>", self.callback)
        self.menu.grid(row=1, columnspan=1, sticky='we', padx=(20, 0), pady=10)

        # Entry frame, labels and buttons init
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


        # Info menu init
        self.info_pwm = tk.Label(self, text='PWM: No value')
        self.info_pwm.grid(column=0, row=5, sticky='w')

        self.info_flow = tk.Label(self, text='Flow: No value')
        self.info_flow.grid(column=0, row=6, sticky='w')

        self.info_temp = tk.Label(self, text='Temperature: No value')
        self.info_temp.grid(column=0, row=7, sticky='w')


        # Request button init
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
        # self.geometry('400x150')  # Use if a certain window size is required

        # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        # background of the root window
        self.config(bg='gray66')

        self.__create_widgets()

    def __create_widgets(self):

        # create the input frame
        SASS_frame = SASSFrame(self)
        SASS_frame.grid(column=0, row=1, sticky='sw')

        # create the button frame
        PUMP_frame = PUMPFrame(self)
        PUMP_frame.grid(column=1, row=0, sticky='ne')

        logo_frame = LogoFrame(self)
        logo_frame.grid(column=0, row=0, sticky='nw')

        for widget in self.winfo_children():
            widget.grid(padx=30, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
