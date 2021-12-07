tcollector is a framework to collect data points and store them in OpenTSDB.
It allows you to write simple collectors that it'll run and monitor.  It also
handles the communication with the TSDs.

For more info, see the [TCollector Documentation](http://www.opentsdb.net/tcollector.html)

[![Build Status](https://travis-ci.org/OpenTSDB/tcollector.svg?branch=master)](https://travis-ci.org/OpenTSDB/tcollector)

Customizations:
1. Support python3
2. Add collects/0/docker_stats.py to collect cpu/mem/io metrics of docker containers.

Usages:

1. Prerequsite: 

* Make sure python3 is installed as (/usr/bin/python3)

2. To use TCollector to collect metrics, simply download it and run,

    git clone https://github.com/OpenTSDB/tcollector.git
    cd tcollector
    ./tcollector start --host <hostname(default:localhost)> --port <port(default: 4242)>
    
3. We suggest to install sysstat to support 'mpstat' which collects nice-reading cpu metrics.

* For Ubuntu:
    apt-get install sysstat

* For Centos:
    yum install sysstat

