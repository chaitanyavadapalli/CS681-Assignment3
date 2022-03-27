from django.http import HttpResponse
from multiprocessing import Pool
from Workload.config import *
from oslo_concurrency import lockutils
from oslo_concurrency import processutils
from django.conf import settings
import os


arr=[0 for i in range(BIG_ARR_LEN)]
thread_alloc=BIG_ARR_LEN//NUM_THREADS
thread_file_alloc=FILE_SIZE//NUM_THREADS


lockutils.set_defaults(settings.LOCK_PATH)

@lockutils.synchronized('not_thread_process_safe', external=True)
def Writer(file_name,data):
    with open(file_name, 'a') as dest_file:
        dest_file.write(data)

def func(threadid):
    start_idx=threadid*thread_alloc
    end_idx=start_idx+thread_alloc
    for i in range(start_idx,end_idx):
        arr[i]+=1
    test_data='\0'*thread_file_alloc
    Writer(settings.FILE_PATH,test_data)
    

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
