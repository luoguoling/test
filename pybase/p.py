from multiprocessing import Pool
from time import time,sleep
pool = Pool(processes=10)
result = []
def grap_url(url):
    print "grap %s" % url
    sleep(10)
    print "end grap %s" % url
urls = ["http://www.baidu.com","http://www.jd.com","www.z.cn","www.sohu.com"]
start = time()
for a in urls:
    res = pool.apply_async(grap_url,(a,))
    result.append(res.get())
print time() - start
