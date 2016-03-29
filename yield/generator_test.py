# -*- coding: utf-8 -*-
import time

def tail(f):
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def print_matches(matchtext):
    print "Looking for", matchtext
    while True:
        line = (yield)
        if matchtext in line:
            print line

matchers = [
    print_matches("python"),
    print_matches("quido"),
    print_matches("jython"),
    print_matches("한글")
]

for m in matchers: m.next()

wwwlog = tail(open("access-log"))
for line in wwwlog:
    for m in matchers:
        m.send(line)
