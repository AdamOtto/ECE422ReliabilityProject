"""
HTTP client simulator. It simulate a number of concurrent users and calculate the response time for each request.
"""

import requests
import time
import threading
import sys

if len(sys.argv) < 4:
    print('To few arguments; you need to specify 3 arguments.')
    print('Default values will be used for server_ip, no of users and think time.\n')
    swarm_master_ip = '204.209.76.156'  # ip address of the Swarm master node
    no_users = 6  # number of concurrent users sending request to the server
    think_time = 0  # the user think time (seconds) in between consequent requests
else:
    print('Default values have be overwritten.')
    swarm_master_ip = sys.argv[1]
    no_users = int(sys.argv[2])
    think_time = float(sys.argv[3])


class MyThread(threading.Thread):
    def __init__(self, name, counter, numUsers):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
        self.numUsers = numUsers

    def run(self):
        print("Starting " + self.name + str(self.counter))
        workload(self.name + str(self.counter), (self.numUsers - self.counter) * 4 )

class workLoadThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("Starting workload thread\n")
        global numRequests
        global no_users
        t2 = t0 = time.time()
        while threadDone < no_users+1:
            t1 = time.time()
            time.sleep(sleepTime)
            t2 = time.time()

            f = open('workload.txt', 'a')
            f.write(str(t2 - t0) + ',' + str(numRequests / (t2 - t1)) + '\n')
            f.close()
            numRequests = 0

def lastTask():
    global ts
    for x in range(0, 5):
        global numRequests
        numRequests += 1
        tryOver = True
        while tryOver == True: #
            t0 = time.time()
            try:
                r = requests.get('http://' + swarm_master_ip + ':8000/')
                tryOver = False
            except:
                tryOver = True
        t1 = time.time()

        global numRequests
        numRequests += 1

        rs = r.text.split('.')
        #print(rs)
        if isInt(int(rs[3])):
            f = open('appSize.txt', 'a')
            f.write(str(t1 - ts) + ',' + rs[3].rstrip() + '\n')
            f.close()
        f = open('responseTime.txt', 'a')
        f.write(str(t1 - ts) + ',' + str(t1 - t0) + '\n')
        f.close()

        time.sleep(5)
    global  threadDone
    threadDone += 1

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def workload(user, max):
    global ts
    #ts = time.time()
    #while True:
    for x in range(0, max):
        #t0 = time.time()
        global numRequests
        numRequests += 1
        tryOver = True
        while tryOver == True: #
            t0 = time.time()
            try:
                r = requests.get('http://' + swarm_master_ip + ':8000/')
                tryOver = False
            except:
                tryOver = True
        #print(r.text)
        t1 = time.time()

        global numRequests
        numRequests += 1

        rs = r.text.split('.')
        #print(rs)
        if isInt(int(rs[3])):
            f = open('appSize.txt', 'a')
            f.write(str(t1 - ts) + ',' + rs[3].rstrip() + '\n')
            f.close()
        f = open('responseTime.txt', 'a')
        f.write(str(t1 - ts) + ',' + str(t1 - t0) + '\n')
        f.close()

        print("Response Time for " + user + " = " + str(t1 - t0))
        time.sleep(think_time)
    global  threadDone
    threadDone += 1


numRequests = 0
sleepTime = 5
ts = 0
threadDone = 0
if __name__ == "__main__":
    threads = []
    workLoadT = workLoadThread()
    for i in range(no_users):
        threads.append(MyThread("User", i, no_users))
    workLoadT.start()
    ts = time.time()
    for i in range(no_users):
        threads[i].start()
        time.sleep(10)
    for i in range(no_users):
        threads[i].join()

    lastTask()