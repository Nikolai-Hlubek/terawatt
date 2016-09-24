import datetime
import sys

arg=''
if len(sys.argv)>1:
    arg=sys.argv[1]

f=open('stopping.txt', 'a')
f.write(str(round(datetime.datetime.timestamp(datetime.datetime.now())))+', '+arg+'\n')
f.close()
