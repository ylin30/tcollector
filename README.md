tcollector is a framework to collect data points and store them in OpenTSDB.
It allows you to write simple collectors that it'll run and monitor.  It also
handles the communication with the TSDs.

For more info, see the [TCollector Documentation](http://www.opentsdb.net/tcollector.html)

[![Build Status](https://travis-ci.org/OpenTSDB/tcollector.svg?branch=master)](https://travis-ci.org/OpenTSDB/tcollector)

# Customizations:
1. Support python3
2. Add collects/0/docker_stats.py to collect cpu/mem/io metrics of docker containers.

# Usages:

## 1. Prerequsite: 

* Make sure python3 is installed as (/usr/bin/python3)

## 2. To use TCollector to collect metrics, simply download it and run,
    
     git clone https://github.com/ylin30/tcollector.git
     cd tcollector
     ./tcollector start --host <hostname(default:localhost)> --port <port(default: 4242)>
     
To stop tcollector:

     pi@raspberrypi:~/tcollector $ ./tcollector stop
     /home/pi/tcollector/tcollector.py running
     Stopping /home/pi/tcollector/tcollector.py
     Waiting for /home/pi/tcollector/tcollector.py to die..
     /home/pi/tcollector/tcollector.py running
     Stopping /home/pi/tcollector/tcollector.py
     Waiting for /home/pi/tcollector/tcollector.py to die..
    
## 3. We suggest to install sysstat to support 'mpstat' which collects nice-reading cpu metrics.

For Ubuntu:

    apt-get install sysstat

For Centos:

    yum install sysstat
## 4. To test a individual collector:

There are many builtin collectors in subfolders:
> * tcollector/collectors/0: 
> > * each collector is a long-running process.
> * tcollector/collectors/<number> (e.g., 300, 900): 
> > * each collector will run periodically every (e.g., 300, 900) seconds.
    
To test an individual collector:
    
    pi@raspberrypi:~/tcollector/collectors $ PYTHONPATH=.. python 0/sysload.py
    cpu.usr 1638919195 0.0 cpu=0
    cpu.nice 1638919195 0.0 cpu=0
    cpu.sys 1638919195 0.27 cpu=0
    cpu.irq 1638919195 0.0 cpu=0
    cpu.idle 1638919195 99.67 cpu=0
   
To dry run the whole tcollector:
    
    pi@raspberrypi:~/tcollector $ ./tcollector start -d
    Starting /usr/bin/python3 /home/pi/tcollector/tcollector.py -d
   
It will print on screen all output supposed to be sent to remote TSDB:
    
    ...
    put nfs.client.rpc 1638919763 0 op=getattr version=3 host=raspberrypi
    put nfs.client.rpc 1638919763 0 op=setattr version=3 host=raspberrypi
    put nfs.client.rpc 1638919763 0 op=lookup version=3 host=raspberrypi
    ...
