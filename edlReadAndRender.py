#run it with python edlReadAndRender.py [filename] [videoFormat]
import sys

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

filename = sys.argv[1]
videoFormat = sys.argv[2]

with open(filename) as f:
    content = f.readlines()
# strip newline character
content = [x.strip() for x in content] 

filenameSimple, fileExtension = filename.split('.')
f = open(filenameSimple+'.m3u', 'w')
f.write('#EXTM3U\n')
notNeeded, fileEndTime = content[-1].split(' to ')
f.write('#EXTINF:'+str(get_sec(fileEndTime))+','+filenameSimple+'.'+videoFormat+'\n')

for line in content:
	start, stop = line.split(' to ')
	f.write('#EXTVLCOPT:start-time='+str(get_sec(start))+'\n')
	f.write('#EXTVLCOPT:stop-time='+str(get_sec(stop))+'\n')
	f.write(filenameSimple+'.'+videoFormat+'\n')
f.close()