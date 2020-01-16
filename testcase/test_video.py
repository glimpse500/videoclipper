import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from ffmpeg_adaptor import FFMpeg_adaptor


if __name__ == '__main__':
    ff = FFMpeg_adaptor('testVideo//video1.mp4')
    ff.trim('00:00:01','00:00:05',out_filename = 'output.mp4')    
