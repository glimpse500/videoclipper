ffmpeg -progress log//block.txt -f concat -i list.txt -c copy trim.mp4 2>&1
pause