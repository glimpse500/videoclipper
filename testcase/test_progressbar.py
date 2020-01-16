import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style(root)
# add label in the layout
style.layout('customer.Progressbar', 
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}), 
              ('Horizontal.Progressbar.label', {'sticky': ''})])
# set initial text
style.configure('text.Horizontal.TProgressbara', text='0 %')
# create progressbar
variable = tk.DoubleVar(root)
cbar = ttk.Progressbar(root, style='customer.Progressbar', variable=variable)
cbar.pack()

def increment():
    
    variable.set(variable.get()+5)
    style.configure('customer.Progressbar', 
                    text='{:g} %'.format(variable.get()))  # update label
    root.after(200, increment)

increment()

root.mainloop()
