#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2015 Andrei Skopenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
This script schedule downtime for all services associated with
local host in Icinga 2. Default scheduled downtime 15 mins.

Requires:
    Mk Livestatus should be enabled in Icinga 2.

Config format:
cat >> /etc/icinga2-schedule-downtime.conf << END
mon_host = 'icinga2.domain.com'
mon_port = 6558
END
'''


import socket
import os
import time
import sys


CONFIG_FILE = '/etc/icinga2-schedule-downtime.conf'


def main():
    ''' main '''

    # schedule downtime for local server
    config = {'host_name': socket.gethostname()}

    if os.path.isfile(CONFIG_FILE):
        data = {}
        try:
            execfile(CONFIG_FILE, {}, data)
        except (SyntaxError, OSError, IOError):
            print 'cant read config %s' % CONFIG_FILE
            exit()

        config.update(data)
    else:
        print 'not found config %s' % CONFIG_FILE
        exit()

    # downtime duration can be set from args
    if len(sys.argv) > 1:
        try:
            config['duration'] = int(sys.argv[1]) * 60
        except ValueError:
            print 'cant get downtime period'
            exit()
    else:
        # 15 mins
        config['duration'] = 900

    # author will the same as the logged system user
    if 'SUDO_USER' not in os.environ:
        if 'USER' not in os.environ:
            print 'cant detect user'
            exit(1)
        else:
            config['author'] = os.environ['USER']
    else:
        config['author'] = os.environ['SUDO_USER']

    # scheduled downtime start time
    config['start_time'] = int(time.time())

    # scheduled downtime end time
    config['end_time'] = config['start_time'] + config['duration']

    # scheduled downtime comment
    config['comment'] = 'automate scheduled downtime'

    # If the "fixed" argument is set to one (1), downtime will
    # start and end at the times specified by the "start" and "end" arguments.
    # Otherwise, downtime will begin between the "start" and "end" times
    # and last for "duration" seconds.
    config['fixed'] = 1

    # The service downtime entries can be triggered by another downtime entry
    # if the "trigger_id" is set to the ID of another scheduled downtime entry.
    # Set the "trigger_id" argument to zero (0) if the downtime for the
    # services should not be triggered by another downtime entry.
    config['trigger_id'] = 0

    # connect to icinga2 Mk Livestatus
    sock = socket.socket()
    try:
        sock.connect((config['mon_host'], config['mon_port']))

        # write command to socket
        cmd = '''COMMAND [%(start_time)s] SCHEDULE_HOST_SVC_DOWNTIME;''' \
              '''%(host_name)s;%(start_time)s;%(end_time)s;%(fixed)s''' \
              ''';%(trigger_id)s;%(duration)s;%(author)s;%(comment)s''' \
              '''\n\n''' % config

        sock.send(cmd)
        # Close sending direction. That way
        # the other side knows we are finished.
        sock.shutdown(socket.SHUT_WR)
    except socket.error, exp:
        exit('Error connecting to %(mon_host)s:%(mon_port)s : ' % config + str(exp))

    print 'shwduled downtime for %s mins' % (config['duration'] / 60)


if __name__ == "__main__":
    main()
