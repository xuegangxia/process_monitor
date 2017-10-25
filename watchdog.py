# -*- coding: utf-8 -*-  
#!/usr/bin/python    
  
import os 
import json
import time
import subprocess 
import sys

def kill_proc(name):  
    cmd = 'ps -ef | grep ' + name  
    f = os.popen(cmd)  
    txt = f.readlines()  
    success = 0
    failed = 0

    for line in txt:  
        print line.strip()
        colum = line.split()  
        pid = colum[1]  
        subname = colum[-1]
        cmd = "kill -9 %d" % int(pid)  
        if name == subname:
            break;
        rc = os.system(cmd)  
        if rc == 0 : 
            success = success+1
            print "stop \"%s\" success!!" % subname  
        else:
            failed = failed+1
            print "stop \"%s\" failed!!" % subname 
    print "success %d  failed %d" %(success,failed)

if __name__ == '__main__':
    firsttime = 1
    while 1:
        cmdline = 'ps -ef | grep %s' % (sys.argv[1])
        res = subprocess.Popen(cmdline,stdout=subprocess.PIPE,shell=True)    
        attn=res.stdout.readlines()    
        counts=len(attn) 
        
        print counts  
        if counts<3:
            print "======================================================"
            now_time = time.strftime('%Y-%m-%dT%H:%M:%S+08:00',time.localtime(time.time()))
            if firsttime == 1:
                content = "%s started at %s \n" % (sys.argv[1],now_time)
                firsttime = 0
            else :
                content = "%s dumped at %s \n" % (sys.argv[1],now_time)
            with open('./dumperror.txt', 'a+') as f:
                f.write(content)

            kill_proc(sys.argv[1])
            time.sleep(5)
            cmdline = 'nohup python ./start.py & ' 
            os.system(cmdline)
        else:
            print "monitor success!!!"

        time.sleep(10)
