#!/usr/bin/env python
import jsonrpclib
import re
import ldap
import logging

LOG = logging.getLogger('wifi_login')

def setup_logging(debug = False):
    level = logging.INFO
    if debug:
        level = logging.DEBUG

    logger = logging.getLogger('wifi_login')
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

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

if __name__ == '__main__':
    jsonrpclib.config.version = 1.0
    cbeam = jsonrpclib.Server('http://10.0.1.27:4254/rpc/')

    # set to true to get debug infos including user sensitive data!
    setup_logging(False)

    userwantsme = []
    # example for a manual list without ldap
    #userwantsme.append('lynxis')
    #cbeam.login('lynxis')

    f = open('/var/run/rsyslog-freeradius.pipe', 'r')
    # alles zwischen den eckigen klammern nach Login OK
    # z.B. 
    # 'Sun Aug 12 04:27:51 2012 : Auth: Login OK: [lynxis] (from client intern port 0 cli 00-22-5F-DD-22-11)'
    regex = re.compile('(.*Login OK: \[)(?P<username>[^\]]*)(.*)')

    LOG.info("Starting wifi login")

    while True:
        line = f.readline()
        match = regex.match(line)
        if (match):
            LOG.info("Tick found a radius line with user info")
            user = (match.groupdict()['username']).lower()
            LOG.debug("checking for user %s\n" % user)
            if user in userwantsme:
                LOG.debug("user %s is in manual list\n" % user)
                try:
                    cbeam.wifi_login(user)
                except Exception as e:
                    LOG.error("exception caught: %s" % repr(e))
            elif getUserWantsWlanPresence(user):
                LOG.debug("user %s over ldap\n" % user)
                try:
                    cbeam.wifi_login(user)
                except Exception as e:
                    LOG.error("exception caught: %s" % repr(e))
