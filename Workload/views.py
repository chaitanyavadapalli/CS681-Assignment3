from django.http import HttpResponse
from multiprocessing import Pool
from Workload.config import *

arr=[0 for i in range(BIG_ARR_LEN)]
thread_alloc=BIG_ARR_LEN//NUM_THREADS
thread_file_alloc=FILE_SIZE//NUM_THREADS


def func(threadid):
    counter=0
    start_idx=threadid*thread_alloc
    end_idx=start_idx+thread_alloc
    for i in range(start_idx,end_idx):
        arr[i]+=1
    f = open("file.dat", "w")
    f.seek(threadid*thread_file_alloc)
    f.write('\0'*thread_file_alloc)
    f.close()

def index(request):
    p=Pool()
    jobs=[]
    for i in range(NUM_THREADS):
        process=p.apply_async(func,[i])
        jobs.append(process)
    p.close()
    
    for j in jobs:
        j.get()
    
    return HttpResponse("Success")
