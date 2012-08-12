#!/usr/bin/env python2
import jsonrpclib
import re

jsonrpclib.config.version = 1.0
cbeam = jsonrpclib.Server('http://10.0.1.27:4254')

userwantsme = []
userwantsme.append('lynxis')

#cbeam.login('lynxis')

f = open('/var/run/rsyslog-freeradius.pipe', 'r')
# alles zwischen den eckigen klammern nach Login OK
# z.B. 
# 'Sun Aug 12 04:27:51 2012 : Auth: Login OK: [lynxis] (from client intern port 0 cli 00-22-5F-DD-22-11)'
regex = re.compile('(.*Login OK: \[)(?P<username>[^\]]*)(.*)')

while True:
    line = f.readline()
    match = regex.match(line)
    if (match):
        user = match.groupdict()['username']
        if user in userwantsme:
            cbeam.login(user)
