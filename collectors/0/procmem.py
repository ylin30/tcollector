#!/usr/bin/env python
# This file is part of tcollector.
# Copyright (C) 2010-2013  The tcollector Authors.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.
#
"""Process memory for TSDB"""

import sys
import time
import re
import psutil  # Required to 'pip install psutil'

from collectors.lib import utils

interval = 15  # seconds
proc_names_monitored = ('tt', 'ticktock', 'influxd', 'postgres', 'taosd', 'victoria-metrics-prod', 'java') # names must be unique


# Loop all processes to find matched process by names.
# Using tag pid to differentiate processes with the same name.
def send_memory(ts):
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
           if p.name() in proc_names_monitored:
            	print("proc.mem.rss %d %d proc=%s pid=%d" % (ts, p.memory_info().rss, p.name(), p.pid))
            	print("proc.mem.data %d %d proc=%s pid=%d" % (ts, p.memory_info().data, p.name(), p.pid))
            #else:
            #    print("proc not in dic: %s" % p.name)
        except Exception:
            pass

# Create a dict directly with name as key. So it required processes must have unique names.
# It will be faster since we don't need to loop all processes.
def send_memory_uniq_name(ts):
    procs = {p.name(): p.info for p in psutil.process_iter(['pid', 'memory_info'])}
    
    for name in proc_names_monitored:
        print("proc.mem.rss %d %d proc=%s" % (ts, procs[name]['memory_info'].rss, name))
        print("proc.mem.data %d %d proc=%s" % (ts, procs[name]['memory_info'].data, name))

def main():
    """procmem main loop"""

    utils.drop_privileges()

    while True:
        ts = int(time.time())

        send_memory(ts)

        sys.stdout.flush()
        time.sleep(interval)

if __name__ == "__main__":
    sys.exit(main())
