from tkinter import *
import tkinter as tk
from tkinter import ttk


class KeyBingingTest(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Key Binding Test")
        self.geometry("800x100")


        # label container
        self.frame1 = ttk.Frame(master=self)
        self.frame1.grid(row=1, column=0)

        self.test = ttk.Label(self.frame1, text="Initial text")
        self.test.grid(column=0, row=1)
        self.bind_all("<Key>", self._testing_function)

        self.frame2 = ttk.Frame(master=self)
        self.frame2.grid(row=1, column=1)
        self.btnf2 = ttk.Button(self.frame2, text="test button frame2")
        self.btn2f2 = ttk.Button(self.frame2, text="test button2 frame2")
        self.btnf2.grid(row=1, column=0, sticky="e", padx=100, pady=2)
        self.btn2f2.grid(row=1, column=1, sticky=tk.W, padx=100, pady=2)

        self.frame3 = ttk.Frame(self)
        self.frame3.grid(row=2, column=0)
        self.frame_31 = ttk.Frame(self.frame3)
        self.frame_31.grid()
        self.btnf31 = ttk.Button(self.frame_31, text="test button frame 31")
        self.btn2f31 = ttk.Button(self.frame_31, text="test button2 frame 31")
        self.btnf31.grid(row=1, column=0)
        self.btn2f31.grid(row=1, column=1)




    def _testing_function(self, event):
        self.test.config(text="Key_pressed: " + event.char)




if __name__ == "__main__":
    new_test = KeyBingingTest()
    new_test.mainloop()