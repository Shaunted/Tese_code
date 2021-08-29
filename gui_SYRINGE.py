import tkinter as tk
from tkinter import Label, StringVar, Text, Variable, ttk, messagebox
from PIL import ImageTk, Image
import serial
from serial.tools.list_ports import comports



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

    def flow_command(self, event):
        pass


    def start_command(self):
        pass

    def reset_command(self):
        pass

        # values = str.splitlines()

    def __create_widgets(self):
        self.title = Label(self, text='Syringe Pump control menu',
                           background='gray66', anchor='nw')
        self.title.grid(column=0, row=0, sticky='w')

        self.aval_ports = ['/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3', '/dev/ttyS4', '/dev/ttyS5', '/dev/ttyS6', '/dev/ttyS7'\
            , '/dev/ttyS8', '/dev/ttyS9', '/dev/ttyS10', '/dev/ttyS11', '/dev/ttyS12', '/dev/ttyS13', '/dev/ttyS14', '/dev/ttyS15']
        self.com = 0

        self.reset_Button = tk.Button(self, background='gray66', bd=0,
                                highlightthickness=0, command=self.reset_command, text = 'RESET')
        self.reset_Button.grid(column=0, row=5, sticky='w')

        self.start_Button = tk.Button(self, background='gray66', bd=0,
                                highlightthickness=0, command=self.start_command, text= 'START')
        self.start_Button.grid(column=0, row=4, sticky='e')

        self.flow_rate = tk.Entry(self, background='gray66', text= 'input desired flowrate')
        self.flow_rate.bind('<Key-Return>', self.flow_command)
        self.flow_rate.grid(column=0, row=3, sticky='we', padx=(20, 0))

        # # Button states
        # self.state_button = True
        # # Button images
        # self.stop = ImageTk.PhotoImage(Image.open(
        #     'stop.png').resize((51, 51), Image.ANTIALIAS))



        # self.menu = ttk.Combobox(
        #     self, values=self.aval_ports)
        # self.menu.bind("<<ComboboxSelected>>", self.callback)
        # self.menu.grid(row=1, columnspan=1, sticky='we', padx=(20, 0), pady=10)

        # self.entry_frame = tk.Frame(self)
        # self.entry_frame.config(background='gray66')
        # self.entry_frame.grid(column=0, row=3, sticky='we', padx=(20, 0))
        # self.pwm_label = tk.Label(
        #     self.entry_frame, text='Pump speed', background='gray66')
        # self.pwm_label.pack(side='left', padx=(0, 5))
        # self.pwm = tk.Entry(self.entry_frame)
        # self.pwm.bind('<Key-Return>', self.entry_callback)
        # self.pwm.pack(side='left')
        # self.button = tk.Button(self, background='gray66', bd=0,
        #                         highlightthickness=0, command=self.button_command, image=self.stop)
        # self.button.grid(column=0, row=4, sticky='e')

        # self.info_pwm = tk.Label(self, text='PWM: No value')
        # self.info_pwm.grid(column=0, row=5, sticky='w')

        # self.info_flow = tk.Label(self, text='Flow: No value')
        # self.info_flow.grid(column=0, row=6, sticky='w')

        # self.info_temp = tk.Label(self, text='Temperature: No value')
        # self.info_temp.grid(column=0, row=7, sticky='w')

        # self.req_button = tk.Button(
        #     self, text='Request information', background='gray66', command=self.request)
        # self.req_button.grid(column=0, row=8, sticky='e')


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

        # create the button frame
        PUMP_frame = PUMPFrame(self)
        PUMP_frame.grid(column=1, row=0, sticky='ne')

        logo_frame = LogoFrame(self)
        logo_frame.grid(column=0, row=0, sticky='nw')

        for widget in self.winfo_children():
            # if widget != logo_frame:
            widget.grid(padx=30, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()

