#****************************************************************************************************************************************************
# Library Imports
#****************************************************************************************************************************************************
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from traits.api import HasTraits, Button, Enum, Int, Float, Str
from traitsui.api import Item, View, Group, Image, ImageEditor, StatusItem
import struct
import serial
from serial.tools.list_ports import comports


#****************************************************************************************************************************************************
# Header: guiExample()
# Tasks: Class for the GUI example
#****************************************************************************************************************************************************
class guiExample(HasTraits):
    logo = Image('ist.png')
    statusSpacer = Str('')
    status = Str('Disconnected')    
    connect = Button()
    start = Button()
    parameter1 = Int(0)   
    parameter2 = Enum('Value 1', 'Value 2', 'Value 3')
    parameter3 = Float(0.0)       
    result1 = Int(0)
    result2 = Str('Result')    
    view = View(
        Group(
            Item('logo', editor = ImageEditor(), show_label = False, width = 100),
            Group(
                Item('connect', show_label = False, width = 200),
                Item('start', show_label = False, width = 200),
                orientation = 'vertical'
            ),
            Group(
                Item('parameter1', label = 'Parameter 1', show_label = True, width = 200),
                Item('parameter2', label = 'Parameter 2', show_label = True, width = 200),
                Item('parameter3', label = 'Parameter 3', show_label = True, width = 200),
                orientation = 'vertical'
            ),
            Group(
                Item('result1', show_label = True, width = 200),
                Item('result2', show_label = True, width = 200),
                orientation = 'vertical'
            ),
            orientation = 'horizontal'
        ),
        title = 'SEP MEE 2019/20',
        width = 1000, height = 200,
        resizable = True,
        statusbar = [StatusItem(name = 'statusSpacer', width=0.8), StatusItem(name = 'status', width=0.2)]
    )

    def __init__(self):
        super(guiExample, self).__init__()
        self.connected = False

    # This is the callback running every time the start button is pressed
    def _start_fired(self):
        print 'Start button just got pressed'
        # Change the results
        self.result1 = self.result1 + 1
        self.result2 = 'OK'

    # This is the callback running every time the parameter 1 is changed
    def _parameter1_changed(self):
        print 'Parameter 1 changed to ', self.parameter1

    # This is the callback running every time the parameter 1 is changed
    def _parameter2_changed(self):
        print 'Parameter 2 changed to ', self.parameter2

    # This is the callback running every time the parameter 1 is changed
    def _parameter3_changed(self):
        print 'Parameter 3 changed to ', self.parameter3

    # This is the callback running every time the connect button is pressed
    def _connect_fired(self):
        print 'Connect button just got pressed'
        ports = comports()
        ports = list(ports)
        for test_port in ports:
            if test_port[1].find('USB Serial Device') >= 0:
                self.port = serial.Serial(test_port, 115200, timeout = 2)
                self.status = 'Connected'
                self.connected = True

    def serial_receive_example(self):
        if self.connected:
            # The next three lines read a 32 bits integer from the serial port
            data = self.port.read(4)
            tmp = struct.unpack('I', data)
            self.result1 = tmp
            # The next three lines read a string from the serial port
            data = self.port.readline()
            self.result2 = data

    def serial_send_example(self):
        if self.connected:
            # The next two lines sends a 32 bits integer through the serial port        
            tmp = struct.pack('I', self.parameter1)
            self.port.write(tmp)   
            # The next two lines sends a string through the serial port 
            tmp = self.parameter2
            self.port.write(tmp)


#**********************************************************************************************************
# Header: main
# Tasks: Entry point, defines and configure a TraitsUI GUI
#**********************************************************************************************************
if __name__ == "__main__":

    guiHandler = guiExample ()    
    guiHandler.configure_traits()