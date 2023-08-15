#!usr/bin/python

from tkinter import *

class Punchout(Tk):
    def __init__(self):
        super().__init__()

        self.widget_width = 200
        self.widget_height = 50

        self.title("Punchout Session")
        self.topFrame = Frame(self, width=self.widget_width, height=self.widget_height)
        self.topFrame.pack()
        self.bottomFrame = Frame(self, width=self.widget_width, height=self.widget_height)
        self.bottomFrame.pack()
        self.close_button()

        self.center_window()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - self.widget_width) / 2)
        y_position = int((screen_height - self.widget_height) / 2)
        self.geometry(f"{self.widget_width}x{self.widget_height}+{x_position}+{y_position}")

    def close_button(self):
        self.generate = Button(self.bottomFrame, text="Generate", command=self.generate_session)
        self.generate.grid(row=1, column=0)
        self.close = Button(self.bottomFrame, text="Close", command=self.close_window)
        self.close.grid(row=1, column=1)
    
    def generate_session(self):
        pass

    def close_window(self):
        self.destroy()

if __name__ == "__main__":
    punchout = Punchout()
    punchout.mainloop()