import winsound
import time

tone = {'-1':262,'-1+':278,'-2':294,'-3-':312,'-3':330,'-4':349,'-4+':370.5,\
        '-5':392,'-5+':416,'-6':440,'-7-':467,'-7':494,\
    '1':523,'1+':554,'2':588,'3-':622,'3':660,'4':698,'4+':740,'5':784,\
        '5+':831,'6':880,'7-':932,'7':988,\
        '+1':1047,'+1+':1111,'+2':1175,'+3-':1247,'+3':1319,'+4':1397,'+4+':1483,\
        '+5':1568,'+5+':1664,'+6':1760,'+7-':1868,'+7':1976}

note={'2':1000,'3':800,'4':700,'8':400,'12':600,'16':200}

def play(key,t):
    winsound.Beep(tone[key],note[t])

def readSong(file):
    song = []
    with open(file,'r')as f :
        keys = f.readlines()
        for i in keys:
            if len(i)>1:
                i = i.split()
                song.append(i)
    return song

def playSong(name):
    print('*****%s*****'%name)
    s = readSong(name+'.txt')
    for i in s:
        if i[0]=='s':
            time.sleep(int(i[1])/10)
        else:
            #print(i[0],end=' ')
            play(i[0],i[1])
    
if __name__ == '__main__':
    playSong('那些你很冒险的梦')
            
