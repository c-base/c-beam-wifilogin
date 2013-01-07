#!/usr/bin/env python
import jsonrpclib
import re
import ldap

class Config:
    basedn = 'ou=crew,dc=c-base,dc=org'
    uri = 'ldap://<LDAPLOGIN>'
    numberAttr = 'uidNumber'
    nameAttr = 'uid'
    wlanAttr = 'wlanPresence'

def openConnection():
    cfg = Config()
    return ldap.initialize(cfg.uri)

def getLdapArgForFilter(ldapfilter, searchAttr):
    cfg = Config
    connection = openConnection()
    searchingAttr = list([searchAttr])
    entry = connection.search_s( cfg.basedn, ldap.SCOPE_SUBTREE, ldapfilter, searchingAttr)
    if len(entry) == 1:
        if len(entry[0][1]) == 1:
            return entry[0][1][searchAttr][0]
    return None


def getUserWantsWlanPresence(userName):
    cfg = Config
    ldapfilter = "(%s=%s)" % (cfg.nameAttr, userName)
    wantWlanPresence = getLdapArgForFilter(ldapfilter, cfg.wlanAttr)
    if wantWlanPresence == 'TRUE':
        return True
    else:
        return False


def logme(log):
    print(log)

jsonrpclib.config.version = 1.0
cbeam = jsonrpclib.Server('http://c-leuse:4254')

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
        user = (match.groupdict()['username']).lower()
        logme("checking for user %s\n" % user)
        if user in userwantsme:
            logme("user %s is in manual list\n" % user)
            cbeam.wifi_login(user)
        elif getUserWantsWlanPresence(user):
            logme("user %s over ldap\n" % user)
            cbeam.wifi_login(user)
            cbeam.wifi_login(user)
