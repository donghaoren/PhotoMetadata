#!/usr/bin/python

import index
import ConfigParser

c = ConfigParser.ConfigParser()
c.read(u"config.ini")
path = unicode(c.get(u"main", u"path"), "utf-8")
index.update(db = u"metadata.sqlite", root = path)
