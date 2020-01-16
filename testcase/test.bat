ffmpeg -i "C:/Users/nvt03346/Desktop/315 test/Analog.mp4" -ss 00:00:00.0 -t 00:00:12.0 -async 1 -c  copy "C:/Users/nvt03346/Desktop/315 test/Analog3.mp4"
pause


ffmpeg -f concat -i tmp_list.tmp -c copy "C:\\Users\\nvt03346\\Desktop\\315 test\\a.mp4"
pause