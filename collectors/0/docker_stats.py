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
"""Docker stats for TSDB"""

import sys
import time
import re
import docker

from collectors.lib import utils

interval = 5  # seconds

def send_cpu(ts, container_name, stats):
    UsageDelta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    SystemDelta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    cpu_percentage = (UsageDelta / SystemDelta) * 100
    
    print("docker.cpu %d %.2f container=%s" % (ts, cpu_percentage, container_name))


def send_mem(ts, container_name, stats):
    usage = stats['memory_stats']['usage'];
    limit = stats['memory_stats']['limit'];
    mem_percentage = (usage / limit) * 100
    
    print("docker.memory %d %.2f container=%s" % (ts, mem_percentage, container_name))

def send_disk_io(ts, container_name, stats):
    io_array = stats['blkio_stats']['io_service_bytes_recursive']
    read_bytes = 0
    write_bytes = 0
    for io in io_array:
        if io['op'] == "Read":
            read_bytes = io['value']
        elif io['op'] == "Write":
            write_bytes = io['value'];

    print("docker.read.byte %d %d container=%s" % (ts, read_bytes, container_name))
    print("docker.write.byte %d %d container=%s" % (ts, write_bytes, container_name))

def main():
    """docker_stats main loop"""

    utils.drop_privileges()

    client = docker.from_env()

    while True:
        ts = int(time.time())

        for container in client.containers.list():
            stats = container.stats(stream=False)
            send_cpu(ts, container.name, stats)
            send_mem(ts, container.name, stats)
            send_disk_io(ts, container.name, stats)

        sys.stdout.flush()
        time.sleep(interval)

if __name__ == "__main__":
    sys.exit(main())
