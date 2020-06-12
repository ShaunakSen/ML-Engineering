from multiprocessing import Pool

def job(num):
    return {'OK':[1,2,3]}

if __name__ == '__main__':
    p = Pool(processes=20) # set up the Pool object, which will have 20 processes
    data = p.map(job, [i for i in range(50)])
    print (type(data))
    p.close()
    print (data)
