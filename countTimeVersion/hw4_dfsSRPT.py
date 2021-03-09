from SRPT import SRPT
import pyexcel, math, string,sys,time
import heapq as hq
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

upperBound=sys.maxsize
record=[]
nodeVisited=0
def dfs(toSet,fixed):
    global upperBound,record,nodeVisited    
    if not toSet:
        raise Exception("0 job awaited. Please recheck. \nEither all jobs being sorted, or there's no job for sorting.")
    # nodeVisited+=1

    if (len(toSet)==1):
        # print("\nBottom\ntoSet=",toSet,' Fixed=',fixed) 
        now=cmax(fixed+toSet)
        if now<upperBound:
            record=fixed+toSet
            # print("***get a complete seq, origin UB: ",upperBound,', new UB=',now,"***\n")
            upperBound=now
        # else:
            # print("***get a complete seq bigger than UB, UB unchanged***\n")        
        return

    for i in range(len(toSet)):
        head=toSet[i]
        nodeVisited+=1
        # print("\ntoSet=",toSet,' Fixed=',fixed,'\n head=',head)
        copyList=toSet.copy()
        del copyList[i:i+1]
        cmaxOfNewFixed=cmax(fixed+[head])
        # copyList2=copyList.copy()
        '''condition 1'''
        skip=False
        for j in copyList:
            if head[2]>j[2] and cmaxOfNewFixed>cmax(fixed+[j]):
                skip=True
                break
        if skip:
            continue  

        '''condition 2'''
        if len(copyList)<=len(fixed+toSet)/2 :
            temp=[[-job[2],job]for job in toSet] #lambda job:
            hq.heapify(temp)                      
            if cmaxOfNewFixed>=-temp[0][0]:
                copyList.sort(key = lambda x: int(x[1]))
                currList=fixed+[head]+copyList
                newValue=cmax(currList)                            
                if newValue<upperBound:
                    record=currList
                    upperBound=newValue
                continue


        if copyList:
            # if(cmax(fixed+[head])+SRPT(fixed+[head],copyList)<=upperBound):
            if(SRPT(fixed+[head],copyList)<upperBound):
                dfs((toSet[:i]+toSet[i+1:]),fixed+[head])
                continue
            # else:
                # print("UB= ",upperBound," cmax with SRPT=",SRPT(fixed+[head],copyList2))
                # print("UB= ",upperBound," cmax=",cmax(fixed+[head])+SRPT(fixed+[head],copyList2))
                # print("*** fixed",fixed+[head], " ,branch deleted at node ",head,'***\n')
    return
    

def runDfs(number):
    global upperBound,record
    data = pyexcel.get_sheet(file_name="test instance.xlsx")
    del data.column[0]

    jobs = list(data.columns())
    for job in jobs:
        job_index = int(jobs.index(job))+1
        job_name = nameJob(job_index+1)
        job.insert(0, job_name)  # add an index for every job
   
    jobs = jobs[0:number]
    #jobs=[['A',6, 0], ['B',2, 2], ['C',3, 2], ['D',2, 6], ['E',5, 7], ['F',2, 9]]
    print('<<DFS>>',sep="")
    startTime=time.time()
    dfs(jobs,[])
    endTime=time.time()
    print("Result: ",number," jobs","\ncmax value:",upperBound)
    print("Job seq: ",record)
    print("Elapse time: ",endTime-startTime)
    print('Node visted:', nodeVisited)

runDfs(17)

