import ffmpeg,sys
probe = ffmpeg.probe('testVideo//video1.mp4')
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
width = int(video_stream['width'])
height = int(video_stream['height'])

print(video_stream['duration'])
