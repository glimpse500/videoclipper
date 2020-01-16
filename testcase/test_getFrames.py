import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from ffmpeg_adaptor import FFMpeg_adaptor
from view import ProgressBar
import tkinter as tk
from tkinter import ttk

import unittest
class TestFFMpegAdaptorMethods(unittest.TestCase):
    def test_getDuration(self):
        ff = FFMpeg_adaptor("output.mp4")
        self.assertEqual(int(float(ff.getDuration())), 20)

def time2float(time):
    #print(time[0:2]  + " "+ time[3:5] + " " + time[6:8])
    return(int(time[0:2])*3600+int(time[3:5])*60+ int(time[6:8]))


if __name__ == '__main__':
    log_file = 'log.txt'
    ff = FFMpeg_adaptor("testVideo//video1.mp4")
    t1 = '00:00:00'
    t2 = '00:00:02'
    ff.getAllFrame(t1,t2,"photo//test_",log_file,'.png')

    root = tk.Tk()

    process_file = open('log//block.txt','r')
    pbar = ProgressBar(root,log_file = process_file,total = time2float(t2)-time2float(t1))
    pbar.pack()
    pbar.update()

    root.mainloop()
