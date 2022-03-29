from django.http import HttpResponse
from multiprocessing import Pool
from Workload.config import *
from oslo_concurrency import lockutils
from oslo_concurrency import processutils
from django.conf import settings
import os
import random
import uuid

range_arr=range(BIG_ARR_LEN)

arr=[0 for i in range_arr]
thread_alloc=BIG_ARR_LEN//NUM_THREADS

block_size=FILE_SIZE//1024

main_list=[]


lockutils.set_defaults(settings.LOCK_PATH)

#@lockutils.synchronized('not_thread_process_safe', external=True)
def Writer():
    file_name=str(uuid.uuid4())+".out"
    write_comm= "dd if=/dev/zero of={0} bs={1} count=1024 oflag=direct".format(file_name,block_size)
    os.system(write_comm)
    os.remove(file_name)

def func(threadid):
    start_idx=threadid*thread_alloc
    end_idx=start_idx+thread_alloc
    #memory workload
    for i in range(start_idx,end_idx):
        arr[i]+=1
    #cpu workload
    for n in range(start_idx,end_idx):
        main_list.append(n)
    #I/O workload
    Writer()
    

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

