#!/usr/bin/python3

import os

cfg = open("config/squid.conf")
c = cfg.read()
cfg.close()

print( c % { "pwd" : os.getcwd() }  )
