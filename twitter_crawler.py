"""
This source code is based on Python-Twitter(https://github.com/bear/python-twitter).
"""

import twitter
import codecs
import time
import os

class BtTwitterCralwer:

    langFilter = []
    failCnt = 0

    THRES = 100
    LONG_SLEEP = 60 * 5 # Twitter rate limits time

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)

    def getTimeline(self, userid, filename=None, count=200):
        if filename != None:
            f = codecs.open(filename, 'a', 'utf-8')

        result = []

        try:
            statuses = self.api.GetUserTimeline(screen_name=userid, count=count)
            self.failCnt = 0
        except twitter.error.TwitterError:
            if filename != None:
                f.close()
            self.failCnt += 1
            print "fail to get...(" + str(self.failCnt) + ")"
            return None

        for s in statuses:
            if len(self.langFilter) == 0 or (s.lang in self.langFilter):
                f.write(userid + "\t" + s.created_at + "\t" + s.lang + "\t" + "\n")
            result.append(s.text)

        if filename != None:
            f.close()

        return result

    """
    API Rate limits
    """
    def getRateLimitStatus(self):
        try:
            statuses = self.api.GetRateLimitStatus()
            s = statuses['resources']['statuses']['/statuses/user_timeline']['remaining']
            return int(s)
        except twitter.error.TwitterError:
            return 0

    def getUserId(self, timelines):
        result = []

        for line in timelines:
            tokens = line.split(' ')

            for token in tokens:
                if token.startswith('@') and len(token) > 1:
                    if token.endswith(':'):
                        token = token[:-1]

                    result.append(token)

        return result

    def crawl(self, seedIds, filename, idFilename, interval=1000.0, begin=0):
        ids = seedIds
        currentIndex = begin
        lastMassiveFailIndex = -1

        try:
            os.remove(filename)
        except OSError:
            pass

        while currentIndex < len(ids):
            remaining = self.getRateLimitStatus()
            if remaining == 0:
                print "### meet the limit... take long sleep... ###"
                time.sleep(self.LONG_SLEEP)
                self.saveIds(ids, currentIndex, idFilename)

                continue
            currentId = ids[currentIndex]

            print "get timeline from " + currentId + "(" + str(currentIndex + 1) + "/" + str(len(ids)) + ")"
            timelines = self.getTimeline(currentId, filename)

            if timelines != None:
                newIds = self.getUserId(timelines)

                for newId in newIds:
                    if not (newId in ids):
                        ids.append(newId)

                if currentIndex % 1000 == 0:
                    self.saveIds(ids, currentIndex, idFilename)
            else:
                if self.failCnt == 1:
                    lastMassiveFailIndex = currentIndex
                if self.failCnt > self.THRES:
                    currentIndex = lastMassiveFailIndex
                    lastMassiveFailIndex += 1

            time.sleep(interval / 1000.0)
            currentIndex += 1

        return ids, currentIndex

    def saveIds(self, ids, index, filename):
        f = codecs.open(filename, 'w', 'utf-8')
        f.write(str(index) + "\n")
        for id in ids:
            f.write(id + "\n")

        f.close()

    def loadIds(self, filename):
        try:
            ids = []

            f = codecs.open(filename, 'r', 'utf-8')

            index = int(f.readline())

            while True:
                tmp = f.readlines()

                for t in tmp:
                    if t.endswitch('\n'):
                        t = t[:-1]

                    if t == '':
                        tmp.remove(t)
                    else:
                        ids.append(t)
                        print t

                if len(tmp) == 0:
                    break

            f.close()

            print str(len(ids)) + " IDs are loaded."

            return ids, index
        except IOError:
            return [], -1

if __name__ == '__main__':
    crawler = BtTwitterCralwer(consumer_key="7PfWHL33szlVW24dp5dFKZYdI",
                               consumer_secret="3QQgVcdezhScRk59feRCbKFNTKvTf2HE4Z1G8hyU8SaZR0rEET",
                               access_token_key="43056838-02IGXWGRoBAdrR610t9zJ9JK9jr4lnfW1wcz0FTo6",
                               access_token_secret="FaZU5GkYv36u8KPZ1fOzdTJU3ttZ01rZ6BRn8ktMYtlRv")
    crawler.langFilter.append('en')

    seedIds, index = crawler.loadIds("ids.txt")

    if len(seedIds) == 0:
        seedIds = ["@cnnbrk", "@elonmusk"]
        index = 0

    ids, index = crawler.crawl(seedIds, "result.txt", "ids.txt", interval=2000, begin=index)
