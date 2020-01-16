import subprocess,re,sys,os,io,time,shlex

import ffmpeg
from threading import Thread

def threaded_cmd(command):
    process = subprocess.call(command,
                               stdin = subprocess.PIPE,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               shell=True)
class Error(Exception):
    def __init__(self, cmd, stdout, stderr):
        super(Error, self).__init__('{} error (see stderr output for detail)'.format(cmd))
        self.stdout = stdout
        self.stderr = stderr
class FFMpeg_adaptor():
    def __init__(self,path):
        self.path = path
        try:
            probe = ffmpeg.probe(path)
        except ffmpeg.Error as e:
            #print(e.stderr, file=sys.stderr)
            sys.exit(1)
        self.video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    def getDuration(self):
        return self.video_stream['duration']
    def getFrameNum(self):
        return self.video_stream['nb_frames']
    def getFrame(self,time):
        out, err = (
            ffmpeg
            .input(self.path,ss = time)
            .filter('scale', size='384:216', force_original_aspect_ratio='increase')
            .output('pipe:', vframes=1, format='image2', vcodec='bmp',q = 25)
            .run(capture_stdout=True)
        )
        #print(type(out))
        return out
    def getAllFrame(self,s_time,t_time,out_filename,log_file = 'log.txt',format = '.bmp'):

        log = 'log//'+log_file
        f = open(log,'w')
        f.close()
        command = ['ffmpeg','-progress',log,'-ss',s_time,'-t',t_time,'-i',self.path,out_filename+'_%04d'+format,'2>&1']
        print(command)
        process = subprocess.Popen(command,stdin = None,stdout = None,stderr = None,shell=True)
        return log

    def repeat(self,input_file,repeat_time,output_file):

        tmp_list = "list.tmp"
        f = open(tmp_list,"w")
        for i in range(0,repeat_time):
            f.write("file "+ input_file + "\n")
        f.close()
        command = ['ffmpeg','-f','concat','-i',tmp_list,'-c','copy',output_file]
        print(command)
        process = subprocess.Popen(command,stdin = subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out, err = process.communicate(None)
        retcode = process.poll()
        if retcode:
            raise Error('ffmpeg', out, err)
        os.remove(tmp_list)
        #os.remove(trim_file)        
        return out,err
    def trim(self,s_time,t_time,log_file = "_log",out_filename = "tmp.mp4"):
        trim_file = out_filename
        
        tmp_trim_video = "trim.mp4"
        tmp_video = "tmp.mp4"
        trim_file = os.getcwd() + "\\" + tmp_trim_video

        command = ['ffmpeg','-progress',log_file,'-ss' ,s_time, '-i', self.path,  '-t', t_time, '-avoid_negative_ts', '1' , tmp_video,'2>&1']
        print(command)
        process = subprocess.Popen(command,stdin = None,stdout = None,stderr = None,shell=True)


    def merge(self):

        subprocess.check_output("dir C:", shell=True)
        subprocess.call("ffmpeg -f concat -i list.txt -c copy HarryPotterCUT_loop.mp4")

