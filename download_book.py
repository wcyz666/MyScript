# -*- coding:utf-8 -*-  

import urllib2, Queue, threading, os
import time
BASE_URL = "http://www.pep.com.cn/oldimages/pic_"
EXT = ".jpg"
is_done = False
num_worker_threads = 500

class ConsumerThread(threading.Thread):
    def __init__(self):
        super(ConsumerThread,self).__init__()
        return

    def run(self):
        global is_done
        while True:
            file_num, dir = queue.get()
            filename = dir + "/" + file_num + EXT
            url = BASE_URL + file_num + EXT
            req = urllib2.Request(url)
            req.add_header('User-Agent', r"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
            opener = urllib2.build_opener()

            try:
                with open(filename, "wb") as fp:
                    fp.write(opener.open(req).read())
                print filename + " is done!"
            except:
                is_done = True
                os.remove(filename)
                print "Task finished"

Books = {
    u"美术": {
        "start":149225,
        "end":149347
    }
}

queue = Queue.Queue(100)
for i in range(num_worker_threads):
     t = ConsumerThread()
     t.daemon = True
     t.start()


for (dir, interval) in Books.items():
    start = interval['start']
    end = interval['end']
    try:
        os.mkdir(dir)
    except WindowsError:
        pass
    while start <= end:
        try:
            queue.put((str(start), dir), timeout=30)
            start += 1
        except:
            break
    queue.join()
    queue.empty()
    is_done = False
    print dir + " is done!"

