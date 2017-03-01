# Evan Wiederspan
# Advanced Python Lab 7: Producer and Consumer threads
# 2-24-2017
from random import randrange 
from time import sleep 
from queue import Queue, Empty
from myThread import MyThread

NITEMS = 5
NREADERS = 3
WRITEDELAY = 2
finishedWriting = False

def writeQ(queue, item):     
    print('producing object {} for Q...'.format(item))     
    queue.put(item, True)     
    print("size now {}".format(queue.qsize()))

def readQ(queue, name):
    # needs to be marked as global so that it knows were not trying to make a local variable
    global finishedWriting
    while True:
        try:
            val = queue.get(False)
            print('{} consumed object {} from Q... size now {}'.format(name, val, queue.qsize()))  
            return val
        # thrown when queue is empty
        except Empty:
            if not finishedWriting:
                print("{} is polling an empty queue".format(name))
                sleep(WRITEDELAY)
            else:
                return None

def writer(queue, loops):
    # needs to be marked as global so that it knows were not trying to make a local variable
    global finishedWriting
    for i in range(loops):
        sleep(randrange(1, 3))
        writeQ(queue, i)
    finishedWriting = True

def reader(queue, loops, name):
    # read will handle sleeping if the queue is empty
    # and will return None if the writer is finished
    # it intentionally does nothing with the data it returns, except
    # for making sure that it is not None     
    while readQ(queue, name) != None:
        pass

def main():    
    q = Queue(NITEMS)
    # create one write and NREADERS reader threads
    threads = [MyThread(writer, (q, NITEMS), 'writer')] + [MyThread(reader, (q, NITEMS, 'reader-' + str(i)), 'reader-' + str(i), True) for i in range(1,NREADERS+1)]   

    for t in threads:         
        t.start()

    for t in threads:         
        t.join()
    print('all done')

if __name__ == '__main__':
    main()