#!/usr/bin/env python2
import jsonrpclib

jsonrpclib.config.version = 1.0
cbeam = jsonrpclib.Server('http://10.0.1.27:4254')

cbeam.login('lynxis')
