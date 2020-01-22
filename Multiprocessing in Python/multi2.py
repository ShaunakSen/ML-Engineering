from multiprocessing import Pool

def job(num):
    return num*2

if __name__ == '__main__':
    p = Pool(processes=20) # set up the Pool object, which will have 20 processes
    data = p.map(job, [i for i in range(10000)])
    p.close()
    print (data)
