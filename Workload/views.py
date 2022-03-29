from django.http import HttpResponse
from multiprocessing import Pool
from Workload.config import *
from oslo_concurrency import lockutils
from oslo_concurrency import processutils
from django.conf import settings
import os
import random

range_arr=range(BIG_ARR_LEN)

arr=[0 for i in range_arr]
thread_alloc=BIG_ARR_LEN//NUM_THREADS

block_size=FILE_SIZE//1024

main_list=[]


lockutils.set_defaults(settings.LOCK_PATH)

#@lockutils.synchronized('not_thread_process_safe', external=True)
def Writer():
    write_comm= "dd if=/dev/zero of=test.out bs={0} count=1024 oflag=direct".format(block_size)

    os.system(write_comm)

def func(threadid):
    start_idx=threadid*thread_alloc
    end_idx=start_idx+thread_alloc
    #memory workload
    for i in range(start_idx,end_idx):
        arr[i]+=1
    #cpu workload
    for n in random.sample(range_arr, thread_alloc):
        main_list.append(n)
    #I/O workload
    Writer()
    

def index(request):
    if os.path.exists(settings.FILE_PATH):
        os.remove(settings.FILE_PATH)
    p=Pool()
    jobs=[]
    for i in range(NUM_THREADS):
        process=p.apply_async(func,[i])
        jobs.append(process)
    p.close()
    
    for j in jobs:
        j.get()
    
    return HttpResponse("Success")
