#!/usr/bin/python

import index
import json
import ConfigParser

c = ConfigParser.ConfigParser()
c.read(u"config.ini")
path = unicode(c.get(u"main", u"path"), "utf-8")
index.update(db = u"metadata.sqlite", root = path)

statistics = index.statistics(db = u"metadata.sqlite")
json_stat = json.dumps(statistics, ensure_ascii = False, indent = 2)
json_stat = "DATA = " + json_stat + ";"
open("statistics.js", "w").write(json_stat.encode("utf-8"))
