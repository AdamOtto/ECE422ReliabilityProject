import docker
import time
from redis import Redis
import requests

client=docker.from_env()
services=client.services
redis=Redis(host='10.2.10.244',port=6379)

try:
    c=redis.get('scale')
except:
    redis.set('scale',1)

if __name__ == "__main__":
    l=[1,2,4,8]
    index=0
    pre=redis.get('hits')
    while(True):
        time.sleep(10)
        webs=services.list(filters={'name':'app_name_web'})
        now=redis.get('hits')
        scale=int(redis.get('scale'))
        if scale != l[index]:
            index=l.index(scale)
        diff = int(now)-int(pre)
        print diff
        print scale
        if diff>2*scale and index<3:
            index=index+1
            dc={'Replicated':{'Replicas':l[index]}}
            web=webs[0]
            web.update(mode=dc)
            redis.set('scale',l[index])

        elif diff<2 and index >= 1:
            index=index-1
            dc={'Replicated':{'Replicas':l[index]}}
            web=webs[0]
            web.update(mode=dc)
            redis.set('scale',l[index])
        print("now in {}".format(l[index]))
        pre=now
