import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from ffmpeg_adaptor import FFMpeg_adaptor
from view import TimeScale
import tkinter as tk
from tkinter import ttk
from tkinter import *

title = "Use Scale TO Get Thumbnail At Particular time"

root = tk.Tk()
root.title(title)

gui_style = ttk.Style()
gui_style.configure('My.TFrame',foreground='gray',background='black')

frameImg = ttk.Frame(root,width=384,height=216,relief = 'solid',style = 'My.TFrame')
frameImg.grid(row =0,column = 0,padx=5, pady=5)
frameImg.pack_propagate(0)
frameItems = tk.Frame(root)
frameItems.grid(row = 1,column = 0,sticky = EW,padx= 8 )
labelImg = Label(frameImg)
scaleTime = TimeScale(frameItems,"Time:",labelImg)
