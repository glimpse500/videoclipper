import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from ffmpeg_adaptor import FFMpeg_adaptor
import unittest
class TestFFMpegAdaptorMethods(unittest.TestCase):
    def test_getDuration(self):
        ff = FFMpeg_adaptor("testVideo//video1.mp4")
        self.assertEqual(int(float(ff.getDuration())), 20)
        
if __name__ == '__main__':
    #unittest.main()
    ff = FFMpeg_adaptor("testVideo//video1.mp4")
    try:
        ff.repeat("testVideo/tmp.mp4",10,'loop.mp4')
    except Exception as e:
        print(e.stdout)
