import threading, random
from time import sleep
from traceback import print_tb

class something:

    def __init__(self, a):
        self.a = a

    def sum(self,b):
        print(f'Sum of {self.a} and {b} is: {self.a+b}')

def sayHi():
    sleep(2)
    print("Hi dude")
    sleep(2)
    print("What's up?")
    sleep(2)

def sum(a,b):
    print(f"Sum of {a} and {b} is {a+b}")
    sleep(1)

def somethingSum(something, b):

    something.sum(b)


some = something(10)

"""
t1 = threading.Thread(name="debugger", target=somethingSum, args=[some,2])
t1.start()
t1.join()
"""

for i in range(10):

    t =  threading.Thread(name="debugger", target=sum, args=[random.randint(1,10),random.randint(1,100)])
    t.start()
    
   
