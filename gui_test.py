import tkinter as tk
from PIL import ImageTk, Image

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        
        self.state = True
        self.config(bg='gray10')
        self.hi_there = tk.Button(self, activebackground = 'forest green',activeforeground = 'white', bd = 5 ,bg ='forest green', width= 20, heigh=10, text='Start', fg = 'white')
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", bg='pink' ,fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    # def 

    def say_hi(self):
        self.state = not self.state
        print(self.hi_there["state"])
        if self.state:
            self.hi_there.config(relief='raised', bg = 'forest green', text='Start')
        else:
            self.hi_there.config(relief="sunken", bg = 'red3', text='Stop')
        print("hi there, everyone!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title('SASS Control System')
    root.config(bg='gray10')
    # screen_w = root.winfo_screenwidth()
    # screen_h = root.winfo_screenheight()
    # center_x = int(screen_w/2 - 500)
    # center_y = int(screen_h/2 - 250)
    # root.geometry(f'1000x500+{center_x}+{center_y}')
    root.iconphoto(False, tk.PhotoImage(file='ist.png'))

    img = ImageTk.PhotoImage(Image.open('ist.png').resize((250,97), Image.ANTIALIAS))
    canvas = tk.Canvas(root, bg="gray10", width=250, height=97, bd=0,highlightthickness=0)
    canvas.pack(anchor='s', side='left')
    canvas.create_image(0,0,image = img, anchor='nw')



    # panel = tk.Label(root, image = img, bg='#0000ffff')
    # panel.place(x=0, y=250)
    app = Application(master=root)
    app.mainloop()

