from tkinter import *
from tkinter import ttk

class TimeScale():
   def __init__(self):
      pass

      
def sel(var):
   selection = "Value = " + str(int(float(var)))
   label.config(text = selection)

root = Tk()
label = Label(root)
label.pack()
#var = DoubleVar()
scale = ttk.Scale( root, from_=0, to=200, orient=HORIZONTAL, command= sel)
scale.pack(anchor=CENTER)

root.mainloop()
