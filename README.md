# wifi auto-login into c-beam
Parse freeradius log to do some strange things based on that input.

We use it to annouce member of c-base to the on-board system. *opt-in*

Contains:
    wifi_login.py - pipe cat who logs you in
    wifi_login.rsyslog.conf - rsyslog config
    wifi_login.supervisord - supervisor config

## How to install it
freeradius server must use syslog interface to log.
Change your radiusd.conf to following:
    log {
        destination = syslog
        logdir = syslog
        file = ${logdir}/radius.log
        syslog_facility = daemon
    }
+ simple install
    #!/bin/sh
    cp wifi_login.py /usr/local/bin/
    cp wifi_login.rsyslog.conf /etc/rsyslog.d/
    cp wifi_login.supervisor.conf /etc/supervisor/conf.d/
    /etc/init.d/supervisor reload

## ToDo
  * use a ldap field for opt-in
  * use accounting instead of auth to annouce users
  * logoff based on accounting infomation?!

