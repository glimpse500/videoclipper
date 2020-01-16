import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 


videoPath = "testVideo//video1.mp4"

from ffmpeg_adaptor import FFMpeg_adaptor
import unittest
class TestFFMpegAdaptorMethods(unittest.TestCase):
    def test_getDuration(self):
        ff = FFMpeg_adaptor(videoPath)
        self.assertEqual(int(float(ff.getDuration())), 331)
        
if __name__ == '__main__':
    unittest.main()
