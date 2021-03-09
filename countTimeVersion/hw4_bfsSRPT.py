from SRPT import SRPT
import heapq as hq
import pyexcel, math, string,sys,time

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


class heapNode:
    fixed=[]
    toSet=[]
    value=0
    def __init__(self,fixed,toSet,value):
        self.fixed=fixed
        self.toSet=toSet
        self.value=value
        
    def printInfo(self):
        print('<<Node>>')
        print('fixed:',self.fixed)
        print('toSet:',self.toSet)
        print('approValue:',self.value)
    
    def getFixed(self):
        return self.fixed


class MyHeap():
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
        if (left <= len(self.minHeap)-1) and (self.minHeap[i].value > self.minHeap[left].value):
            smallest = left
        else:
            smallest = i
        if (right <= len(self.minHeap)-1) and (self.minHeap[smallest].value > self.minHeap[right].value):
            smallest = right
        if (smallest != i):
            self.minHeap[i] = self.minHeap[smallest]
            self.minHeap[smallest] = temp
            self.adjustTree(smallest)
        else:
            return  # the BT is already a min heap
    
    def heapify(self):
        for i in reversed(range(1,math.floor(len(self.minHeap)/2)+1)):
            self.adjustTree(i)

    def insertKey(self, key):
        # print('insert:')
        # key.printInfo()
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
            # if (self.minHeap[parentIndex][2] > self.minHeap[i][2]):
            if (self.minHeap[parentIndex].value > self.minHeap[i].value):
                self.minHeap[i] = self.minHeap[parentIndex]
                self.minHeap[parentIndex] = temp
                self.adjustUpward(parentIndex)
            else:  # smallest is at index i/2, no swap, and recursion stop
                return

upperBound=sys.maxsize
record=[]
nodeVisited=0 #number of nodes visited

def bestfs(number):
    global upperBound,record,nodeVisited
    data = pyexcel.get_sheet(file_name="test instance.xlsx")
    del data.column[0]

    jobs = list(data.columns())
    jobs = jobs[0:number]
    for job in jobs:
        job_index = int(jobs.index(job))+1
        job_name = nameJob(job_index+1)
        job.insert(0, job_name)  # add an index for every job
    #jobs=[['A',6, 0], ['B',2, 2], ['C',3, 2], ['D',2, 6], ['E',5, 7], ['F',2, 9]]
    
    upperBound=cmax(jobs)
    record=jobs

    jobHeap=MyHeap()
    startTime=time.time()
    for job in jobs:
        value=SRPT([job],[x for x in jobs if x != job])
        jobHeap.insertKey(heapNode([job],[x for x in jobs if x != job],value))
        nodeVisited+=1
    # jobHeap.heapify()  
    
    while len(jobHeap.minHeap)>1:  #heap index starts from 1
        # nodeVisited+=1
        # print('\n\njobHeapLen',len(jobHeap.minHeap)-1)
        currentJob=jobHeap.minHeap[1]
        # print('currentJob:')
        # currentJob.printInfo()
        jobHeap.delMin()
        # jobHeap.heapify()
        if len(currentJob.toSet)==1:
            if currentJob.value<upperBound:
                upperBound=currentJob.value
                record=currentJob.fixed+currentJob.toSet
                # print('*** UB > SRPT result, fixed=',currentJob.fixed+currentJob.toSet,'update UB at ',currentJob.toSet[0] )
            # else: 
                # print('*** UB < SRPT result, fixed=',currentJob.fixed+currentJob.toSet,'\ndelete branch at ',currentJob.toSet[0] ,'***')
                # print('currentJob value:',currentJob.value,' UB:',upperBound)
        else: 
            if currentJob.value<upperBound:
                for i in currentJob.toSet:
                    newFixed=currentJob.fixed+[i]
                    newToSet=[x for x in currentJob.toSet if x!=i].copy()#[x for x in currentJob.toSet if x not in newFixed]
                    copyList=newToSet.copy()
                    cmaxOfFixed=cmax(currentJob.fixed+[i])
                    '''condition 1'''
                    skip=False
                    for j in newToSet:
                            if i[2]>j[2] and cmaxOfFixed>cmax(currentJob.fixed+[j]):  
                                #若目前head比toSet中的某節點晚到，且head+原fixed運作的時間 比 head+某點 的cmax慢
                                skip=True
                                break
                    if skip:                       
                        continue

                    '''condition 2'''
                    if len(copyList)<=len(copyList+newFixed)/2 :
                        temp=[[-job[2],job]for job in newToSet] #lambda job:
                        hq.heapify(temp)                      
                        if cmaxOfFixed>=-temp[0][0]:
                            copyList.sort(key = lambda x: int(x[1]))
                            currList=newFixed+copyList
                            newValue=cmax(currList)                            
                            if newValue<upperBound:
                                record=currList
                                upperBound=newValue                                
                            continue
                    if len(copyList)!=1:
                        newValue=SRPT(newFixed,copyList)
                    else:
                        newValue=cmax(newFixed+copyList)
                    if newValue<upperBound:
                        jobHeap.insertKey(heapNode(newFixed,newToSet,newValue))
                    nodeVisited+=1
                    # print('*** UB > SRPT result, add node fixed=',newFixed,' toSet=',newToSet ,' with value ',newValue,' to heap.***')
                # jobHeap.heapify()
    endTime=time.time()
    return endTime-startTime
            
            # else:
                # print('*** UB < SRPT result, fixed=',currentJob.fixed,'\ndelete branch at ',currentJob.fixed[len(currentJob.fixed)-1] ,'***')
                # print('currentJob value:',currentJob.value,' UB:',upperBound)


def runBfs(number):
    print('<<BFS>>',sep="")
    elapseTime=bestfs(number)
    print("Result: ",number," jobs","\ncmax value:",upperBound)
    print("Job seq: ",record)  
    print('Number of nodes visited: ',nodeVisited)
    print("Elapse time: ", elapseTime)

runBfs(17)