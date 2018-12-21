import sys,io,os
from ffmpeg_adaptor import FFMpeg_adaptor
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename,asksaveasfile
from PIL import ImageTk, Image
import threading,time

ffmpegAdaptor = None
mutex = False

def int2Time(var):
    second = var%60
    minute = (var/60)%60
    hour = var/3600
    return str(int(hour)).zfill(2)  + ":"+str(int(minute)).zfill(2)  + ":"+str(int(second)).zfill(2) 

def float2Time(var):
    ms = str(float(var%60) - int(var%60))[2]
    second = var%60
    minute = (var/60)%60
    hour = var/3600
    return str(int(hour)).zfill(2)  + ":"+str(int(minute)).zfill(2)  + ":"+str(int(second)).zfill(2) + "."+ str(ms)

def time2float(time):
    return(int(time[0:2])*3600+int(time[3:5])*60+ int(time[6:8]))
    
class ProgressBar(ttk.Progressbar):
    '''
    root : tkinter.Tk()
    '''
    def __init__(self,root,log_file = None,total = 1):
        self.style = ttk.Style(root)
        self.style.layout('text.Horizontal.TProgressbar', 
                 [('Horizontal.Progressbar.trough',
                   {'children': [('Horizontal.Progressbar.pbar',
                                  {'side': 'left', 'sticky': 'ns'})],
                    'sticky': 'nswe'}), 
                  ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure('text.Horizontal.TProgressbar', text='0 %')
        self.variable = tk.DoubleVar(root)
        self.log_file = log_file
        self.total = total
        self.root = root;
        super().__init__(root, style='text.Horizontal.TProgressbar', variable=self.variable)
        self.cur_progress = {}
        self.cur_progress['progress'] = 'continue'
        self.finish = False
    def reset(self,log_file = None,total = 1):
        self.log_file = log_file
        self.total = total
        self.variable.set(0)
        self.cur_progress['progress'] = 'continue'
        self.style.configure('text.Horizontal.TProgressbar', text='0 %')
        self.finish = False
    def update(self,finish = False):
        #print("update " + self.cur_progress['progress'])
        if finish:
            self.variable.set(100)
            updating = False
            self.finish = True
        elif self.cur_progress['progress'] == 'continue':
            r = self.log_file.readline()
            updating = True
            #print(r.strip())
            while r:
                cur_info = r.split('=')
                key = cur_info[0].strip()
                value = cur_info[1].strip()
                self.cur_progress[key] = value
                if key == 'out_time':
                    #print(self.total)
                    #print(self.cur_progress[key])
                    per = time2float(self.cur_progress[key] )/self.total *100
                    #print(per)
                    self.variable.set(per)
                r = self.log_file.readline()
                
        elif self.cur_progress['progress'] == 'end':
            self.log_file.close()
            self.variable.set(100)
            updating = False
            self.finish = True
        self.style.configure('text.Horizontal.TProgressbar',
                              text='{0:.2f} %'.format(self.variable.get()))  # update label
        if updating:
            self.root.after(100, self.update)
        
class TimeScale():
    def __init__(self,master,leading,img,text = "00:00:00"):

        '''
        OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO   
        O                                       O
        O                                       O
        O                ttk.Frame              O
        O                                       O
        O                                       O
        OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

        StartTime: ------I----------   XX:XX:XX.X
        ^(ttk.Label)    ^(ttk.Scale)   ^(ttk.Label)
                          
        '''
        # "ttk.Frame"
        self.master = master
        
        # "StartTime:" // "EndTime:"
        self.leading = leading
        self.labelHeader = ttk.Label(self.master,text = leading)
        self.labelHeader.config(text = self.leading)
        self.labelHeader.pack(side = LEFT)
        


        # "ttk.Label", for presenting image
        self.img = img
        #

        # "ttk.Scale"
        self.scale = ttk.Scale(master,from_=0, to=0, orient=HORIZONTAL,command = self.onScaleChange)
        self.scale.bind("<ButtonRelease-1>", self.onClickUp)
        self.scale.pack(side = LEFT,expand = True,fill = X, padx= 5 )
        
        # "ttk.Label" for presenting time
        self.text = text
        self.labelTime = ttk.Label(self.master,text = text)
        self.labelTime.pack()
        self.labelTime.pack(side = RIGHT)

        # "videoPath"
        self.filePath = None
        self.dur = 0
        self.var = 0

        self.base100ms = False
    def setScale(self,dur = None,var = None):
       
        if dur != None and var !=None:
             self.dur = dur
             self.var = var
        self.text = float2Time(self.var/10)
        #print(self.dur,self.var)
        if (self.base100ms == True):
            #print("a",self.dur,self.var,self.text)
            self.scale.config(to=self.dur,value = self.var)
            self.labelTime.config(text = self.text)
        else:
            #print("b",self.dur,self.var,self.text[0:8])
            self.scale.config(to=self.dur/10,value = self.var/10)
            self.labelTime.config(text = self.text[0:8])

    def setText(self,text):
        self.text = text
        self.labelTime.config(text = self.text)
        self.labelTime.pack()
        
    def onScaleChange(self,var):
        self.var = int(self.scale.get())
        if self.base100ms == False:
           self.var = self.var*10
           
        self.text = float2Time(self.var/10)
        if self.base100ms == False:
            self.labelTime.config(text = self.text[0:8])
        else:
            self.labelTime.config(text = self.text)
        
    def onClickUp(self, event):
        self.changeImg()
        
    def changeImg(self):
        if self.filePath != None:
            try:
                out = ffmpegAdaptor.getFrame(self.text)
                tmp_img = Image.open(io.BytesIO(out))
                tmp_img = ImageTk.PhotoImage(tmp_img)
                self.img.config(image = tmp_img)
                self.img.image = tmp_img
                self.img.pack()
            except OSError as e:
                print(e)
        
        
class UI:
    def __init__(self, title):

        ''' self.master : Tk()
        ====================================================================================================
        =                                                                                                  =
        =                                      self.frameImg = Frame                                       =
        =                                                                                                  =
        =    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO        OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO    =
        =    O                                       O        O                                       O    =
        =    O                                       O        O                                       O    =
        =    O                ttk.Frame              O        O                ttk.Frame              O    =
        =    O                                       O        O                                       O    =
        =    O                                       O        O                                       O    =
        =    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO        OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO    =
        =                                                                                                  =
        =    StartTime: ------I----------   XX:XX:XX.X        EndTime: ------I----------   XX:XX:XX.X      =
        =    ^(ttk.Label)    ^(ttk.Scale)   ^(ttk.Label)      ^(ttk.Label)    ^(ttk.Scale)   ^(ttk.Label)  =
        =                                                                                                  =
        ====================================================================================================
        ====================================================================================================
        =                                                ==                                                =
        =                                                ==                                                =
        =                                                ==                                                =
        =         self.frameControl:ttk.Frame            ==             self.frameInfo = ttk.Frame         =
        =                                                ==                                                =
        =                                                ==                                                =
        =                                                ==                                                =
        ====================================================================================================        

        '''

        
        '''
        OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO        OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO   
        O                                       O        O                                       O
        O                                       O        O                                       O
        O                ttk.Frame              O        O                ttk.Frame              O
        O                                       O        O                                       O
        O                                       O        O                                       O
        OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO        OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

        StartTime: ------I----------   XX:XX:XX.X        EndTime: ------I----------   XX:XX:XX.X
        ^(ttk.Label)    ^(ttk.Scale)   ^(ttk.Label)      ^(ttk.Label)    ^(ttk.Scale)   ^(ttk.Label)
                          
        '''
        self.master = Tk()
        self.master.title(title)

        gui_style = ttk.Style()
        gui_style.configure('My.TFrame',foreground='gray',background='black')
        self.frameImg = Frame(self.master)
        self.frameImg.grid(row = 0,columnspan = 2)
        
        self.frameControl = ttk.Frame(self.master)
        self.frameControl.grid(row = 1,column = 0,sticky = W+N)
        
        self.frameInfo = ttk.Frame(self.master,width=480,height=100,relief = 'solid')
        self.frameInfo.grid(row = 1,column = 1,sticky = W)
        self.frameInfo.grid_propagate(0) #  force a widget to be a certain size


        self.frameStartImg = ttk.Frame(self.frameImg,width=384,height=216,relief = 'solid',style = 'My.TFrame')
        self.frameStartImg.grid(row =0,column = 0,padx=5, pady=5)
        self.frameStartImg.pack_propagate(0)
        self.frameStartItems = Frame(self.frameImg)
        self.frameStartItems.grid(row = 1,column = 0,sticky = EW,padx= 8 )
        self.labelStartImg = Label(self.frameStartImg)
        self.scaleStartTime = TimeScale(self.frameStartItems,"StartTime:",self.labelStartImg)

        
        self.frameEndImg = ttk.Frame(self.frameImg,width=384,height=216,relief = 'solid',style = 'My.TFrame')
        self.frameEndImg.grid(row =0,column = 1,padx=5, pady=5)
        self.frameEndImg.pack_propagate(0)
        self.frameEndItems = Frame(self.frameImg)
        self.frameEndItems.grid(row = 1,column = 1,sticky = EW,padx= 8 )
        self.labelEndImg = Label(self.frameEndImg)
        self.scaleEndTime = TimeScale(self.frameEndItems,"EndTime:",self.labelEndImg)



        
        self.frameControl = ttk.Frame(self.master)
        self.frameControl.grid(row = 1,column = 0,sticky = W+N)

        self.checkSelect = StringVar()
        self.checkButton = Checkbutton(self.frameControl,text = "base = 100ms",command = self.onChangeSelectBotton,var = self.checkSelect)
        self.checkButton.grid(row = 0,column = 0,sticky = W+N,padx = 8)
        self.checkButton.deselect()
        self.checkButton.config(state=DISABLED)

        
        self.buttonInputFile = ttk.Button(self.frameControl, text="Select File", command=self.onClickButtonInputFile)
        self.buttonInputFile.grid(row = 1,column = 0,sticky = W,padx = 12)
        self.buttonTrim = ttk.Button(self.frameControl, text="Trim", command=self.onClickButtonTrim)
        self.buttonTrim.grid(row = 2,column = 0,sticky = W,padx = 12)
        self.labelRepeatTime = Label(self.frameControl, text="Repeat Time(1~100) = ")
        self.labelRepeatTime.grid(row = 2,column = 1,sticky = W+N)
        
        self.entryRepeatTime = StringVar()
        self.textRepeatTime = ttk.Entry(self.frameControl, textvariable = self.entryRepeatTime,width =3,justify='center')
        self.textRepeatTime.grid(row = 2,column = 2,sticky = W+N)
        self.entryRepeatTime.set('1')
        self.buttonExtract = ttk.Button(self.frameControl, text="Extract", command=self.onClickButtonExtract)
        self.buttonExtract.grid(row = 3,column = 0,sticky = W,padx = 12)




        self.labeInfo = Label(self.frameInfo, text = "Video Info :",font='Helvetica 12 bold')
        self.labeInfo.grid(row = 0,columnspan = 2,padx = 2,pady = 1,sticky = W)
        self.dictInfo = {}
        self.labelResolution = Label(self.frameInfo,width = 30,anchor = W, text = "Resolution : ")
        self.labelResolution.grid(row = 1,column = 0,padx = 8,sticky = EW)
        self.labelFrameRate = Label(self.frameInfo, text = "Frame Rate : ")
        self.labelFrameRate.grid(row = 2,column = 0,padx = 8,sticky = W)
        self.labelFrameNum = Label(self.frameInfo, text = "Frame Number : ")
        self.labelFrameNum.grid(row = 1,column = 1,padx = 8,sticky = W)
        self.labelDur = Label(self.frameInfo, text = "Duration : ")
        self.labelDur.grid(row = 2,column = 1,padx = 8,sticky = W)
        self.filePath = None

        self.style = ttk.Style(self.master)

        # create progressbar
        self.pbar = ProgressBar(self.master)
        self.pbar.grid(row = 2,columnspan = 2,sticky=E+W+N+S,padx = 2)

    def onClickButtonInputFile(self):
        path = askopenfilename()
        if not path:
            return
        self.filePath = path
        #self.entryInputFile.set(self.filePath)
        global ffmpegAdaptor
        
        ffmpegAdaptor = FFMpeg_adaptor(self.filePath)
        #print(ffmpegAdaptor.getDuration())
        duration = int(float(ffmpegAdaptor.getDuration()))

        #print(duration)
        self.scaleStartTime.filePath = self.filePath
        self.scaleStartTime.setScale(dur = duration*10, var = 0)
        self.scaleStartTime.changeImg()
        
        self.scaleEndTime.filePath = self.filePath
        #print("duration = " + str(duration))
        self.scaleEndTime.setScale(dur = duration*10,var = duration*10)
        self.scaleEndTime.changeImg()
        self.checkButton.config(state=ACTIVE)

        info = ffmpegAdaptor.video_stream
        self.setInfo(info)
        self.pbar.reset()
        #self.master.mainloop()
        #print(getDuration(text))
    def onClickButtonTrim(self):
        if (self.filePath == None):
            return
        
        f = asksaveasfile(mode='w', defaultextension=".mp4")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        f.close()
        os.remove(f.name)
        ffmpegAdaptor = FFMpeg_adaptor(self.filePath)
        s_time = self.scaleStartTime.text
        t_time = float2Time(self.scaleEndTime.var/10-self.scaleStartTime.var/10)
        e_time = self.scaleEndTime.text
        #print("s_time "+ str(s_time))
        #print("t_time "+ str(t_time))
        try:
            repeat = int(self.entryRepeatTime.get())
        except ValueError as e:
            repeat = 1
        try:
            tmp_log = "_log"
            log_file = open(tmp_log,'w')
            log_file.close()
            self.pbar.reset(log_file = open(tmp_log,'r'),total = time2float(t_time)*repeat)
            #print((time2float(t_time)-time2float(s_time))*repeat)
            ffmpegAdaptor.trim(s_time,t_time,log_file = tmp_log,out_filename = "tmp.mp4")
            self.pbar.update()
            def repeat_video():
                while self.pbar.finish == False:
                    #print("processing~")
                    time.sleep(0.1)
                try:
                    ffmpegAdaptor.repeat("tmp.mp4",repeat,f.name)
                except Exception as e:
                    print(e.stdout)
                os.remove("tmp.mp4")
                os.remove(tmp_log)
            processThread = threading.Thread(target=repeat_video) 
            processThread.start()
               
        except Exception as e:
            print(e.stdout)
            print(e.stderr)
    def onClickButtonExtract(self):
        if (self.filePath == None):
            return
        save_file = asksaveasfile(mode='w')
        if save_file is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        global ffmpegAdaptor
        ffmpegAdaptor = FFMpeg_adaptor(self.filePath)
        s_time = self.scaleStartTime.text
        t_time = float2Time(self.scaleEndTime.var/10-self.scaleStartTime.var/10)
        log_file = 'log.txt'
        name = save_file.name
        fpath =  ffmpegAdaptor.getAllFrame(s_time,t_time,name,log_file = log_file,format = '.png')

        self.pbar.log_file = open(fpath,'r')
        self.pbar.total = time2float(t_time)
        self.pbar.update()
        save_file.close()
        os.remove(save_file.name)
        

    def onChangeSelectBotton(self):
        
        global ffmpegAdaptor
        self.scaleStartTime
        if (ffmpegAdaptor == None):
            return
        if self.checkSelect.get() == "1":
            #print("select")
            self.scaleStartTime.base100ms = True
            self.scaleEndTime.base100ms = True
            self.scaleStartTime.setScale()
            self.scaleEndTime.setScale()
        else:
            #print("de_select")
            self.scaleStartTime.base100ms = False
            self.scaleEndTime.base100ms = False
            self.scaleStartTime.setScale()
            self.scaleEndTime.setScale()
        pass
    def setInfo(self,info):
        resolution = "Resolution : " + str(info['width'])+"x"+str(info['height'])
        self.labelResolution.config(text = resolution)
        framerate = "Frame Rate : " + str(info['avg_frame_rate'])
        self.labelFrameRate.config(text = framerate)
        try:
            framenum = "Frame Number : " + str(info['nb_frames'])
        except KeyError as e:
            framenum = "Frame Number : n/a"
        self.labelFrameNum.config(text = framenum)
        dur = "Duration : : " + str(float2Time(float(info['duration'])))[0:8]
        self.labelDur.config(text = dur)
        pass


    def runMainLoop(self):
        self.master.mainloop()
    
        



