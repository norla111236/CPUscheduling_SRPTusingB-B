import pyexcel
import math
import string
import time

'''create heap structure, and its function methods
   set the index of heap root, 1.
   minHeap is the array to store the heap. 
   meanHeap[0] stores nothing, minHeap[1:len(minHeap)-1] stores the heap.
   heapSize is len(minHeap)-1.
'''

class MyHeap:
    minHeap = [0]  # minHeap[1:] stores the heap #heapSize

    # def minHeapify(self,index):
    def delMin(self):
        if (len(self.minHeap) > 2):  # (len(minHeap)!=1) and (len(minHeap)!=2)
            self.minHeap[1] = self.minHeap[len(self.minHeap)-1]
            del self.minHeap[len(self.minHeap)-1]
            self.adjustTree(1)
        elif len(self.minHeap) == 2:
            del self.minHeap[1]
        else:
            return  # do nothing

    def adjustTree(self, i):  # recursive function
        # the node at index i being the root,
        # adjust the tree to be a min heap
        temp = self.minHeap[i]
        left = 2*i
        right = 2*i+1
        if (left <= len(self.minHeap)-1) and (self.minHeap[i][1] > self.minHeap[left][1]):
            smallest = left
        else:
            smallest = i
        if (right <= len(self.minHeap)-1) and (self.minHeap[smallest][1] > self.minHeap[right][1]):
            smallest = right
        if (smallest != i):
            self.minHeap[i] = self.minHeap[smallest]
            self.minHeap[smallest] = temp
            self.adjustTree(smallest)
        else:
            return  # the BT is already a min heap

    def insertKey(self, key):
        self.minHeap.append(key)
        index = len(self.minHeap)-1
        # print('insertKeyIndex: ',index)
        if len(self.minHeap) > 2:
            self.adjustUpward(index)

    def adjustUpward(self, i):  # recursive function
        if(i < 2):
            if (i == 0):
                raise Exception(
                    'Index in array index 0. Error. Heap starts from element 1.')
            else:  # index i ==1
                return  # at root, don't have to do adjustments
        else:  # index i >=2
            # doesn't matter whether the newly inserted key is at left or right child, because the origin arraay is a sorted minheap
            # the newly inserted heap only have to do comparison and swap with its parent, if swap is needed
            temp = self.minHeap[i]
            # print('insertKeyIndex: ',i)
            parentIndex = math.floor(i/2)
            # print('insertKeyParentIndex: ',parentIndex)
            # smallest is at index i, do swap, and continue recursion
            if (self.minHeap[parentIndex][1] > self.minHeap[i][1]):
                self.minHeap[i] = self.minHeap[parentIndex]
                self.minHeap[parentIndex] = temp
                self.adjustUpward(parentIndex)
            else:  # smallest is at index i/2, no swap, and recursion stop
                return


def nameJob(index):
    job_name = ''
    tens = math.floor(index/26)
    units = index % 26
    mapping = dict(zip(range(1, 26), string.ascii_uppercase))
    mapping[0] = 'Z'
    if (tens > 0):
        job_name += mapping.get(tens)
    job_name += mapping.get(units)
    return job_name


def cmax(job):
    # print('cmax jobs_fixed:',job)
    Cmax = job[0][1] + job[0][2]
    for i in range(1, len(job)):
        if(job[i][2] <= Cmax):
            Cmax += job[i][1]
        else:
            Cmax = job[i][2]
            Cmax += job[i][1]
    return Cmax


def sumOfC(job):
    # print('cmax jobs_fixed:',job)
    currTime = job[0][1] + job[0][2]
    sumOfC=currTime
    for i in range(1, len(job)):
        if(job[i][2] <= currTime):
            currTime += job[i][1]
        else:
            currTime = job[i][2]
            currTime += job[i][1]
        sumOfC+=currTime
    return sumOfC


def SRPT(fixed,jobs,cmaxOfFixed):  #jobs: jobs that haven't been sort  #cmaxFromFixed: the complete time from already fixed jobs 
    jobs=sorted(jobs, key = lambda x: x[2])
    currTime =cmaxOfFixed #cmaxFromFixed#cmax(fixed)
    objValue = 0
    jobHeap = MyHeap()

    if len(jobs) != 0:
        if jobs[0][2]>=currTime:
            currTime = jobs[0][2]

        jobHeap.insertKey([jobs[0][0], jobs[0][1]])
        del jobs[0]
    else:
        raise Exception("There's no job info in xlsx file.")

    while len(jobs) != 0:
        if (jobs[0][2] == currTime):
            jobHeap.insertKey([jobs[0][0], jobs[0][1]])
            del jobs[0]
        # put the most recent job that haven't enter the heap into jobHeap, if needed.
        elif (jobs[0][2] > currTime):
            if len(jobHeap.minHeap) != 1:  # no need to send job into heap
                jobHeap.minHeap[1][1] -= 1
                currTime += 1
                if(jobHeap.minHeap[1][1] == 0):
                    objValue += currTime
                    jobHeap.delMin()
            else:  # send a job into jobHeap.
                currTime = jobs[0][2]
                jobHeap.insertKey([jobs[0][0], jobs[0][1]])
                del jobs[0]
        else:  
            while len(jobs)>0 and jobs[0][2]<currTime:
                jobHeap.insertKey([jobs[0][0], jobs[0][1]])
                del jobs[0]

    while len(jobHeap.minHeap) != 1:  # no need to send job into heap
        jobHeap.minHeap[1][1] -= 1
        currTime += 1
        if(jobHeap.minHeap[1][1] == 0):
            objValue += currTime
            jobHeap.delMin()

        # print('jobs\n', jobs)
        # print('jobHeap\n', jobHeap.minHeap)
        # print('currTime: ', currTime, '\n')

    # print('\nNumber of jobs: ', number)
    # print("The minimum value of total processing time is ", currTime)
    # print("The objective value is ", objValue)
    objValue+=cmaxOfFixed
    return objValue
