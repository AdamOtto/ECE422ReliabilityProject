
"""
A simple web application; return the number of time it has been visited and also the amount of time that took to
run the difficult function.
"""
import subprocess
import sys
from flask import Flask,request,g
from redis import Redis
import random
import time

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
def difficult_function():
    t0=time.time()
    output=1
    difficulty = random.randint(1000000, 2000000)
    for i in range(difficulty):
        output = output * difficulty
        output = output / (difficulty - 1)
    t1 = time.time()
    compute_time = t1 - t0
    return compute_time
@app.route('/')
def hello():
    count = redis.incr('hits')
    s=redis.get('scale')
    if s:
        s=int(s)
    else:
        s=1
    computation_time = difficult_function()
    return 'Hi There! I have been seen {} times. I have solved the problem in {} seconds.{}\n'.format(count,computation_time,s)
@app.route('/scale',methods=['POST'])
def p():
    n=request.form.get('scale')
    c=redis.set('scale',n)                
    return 'updated {}.\n'.format(n)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
