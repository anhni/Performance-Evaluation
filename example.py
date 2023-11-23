import random
import simpy
import numpy as np
from random import seed
import statistics

seed(29384)  # for seed of randint function
random_seed = 42  # for seed of other random generators
new_customers = 5  # Total number of customers in the system
interarrival = np.random.poisson(3, size=None)  # Generate new customers roughly every x seconds
maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)
patientNumber = 0
waitingTimes = []
serviceTimes = []
interarrivalTimes = []


def generator(env, number, interval):  # customer generator with interarrival times.
    """generator generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer %02d' % i)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)  # adds time to the counter, does not delete from the memory


def customer(env, name):
    # customer arrives to the system, waits and leaves
    arrive = env.now
    print('%7.4f : Arrival time of %s' % (arrive, name))
    yield env.process(system(env, name))

def system(env, name):
    # customer arrives to the system, waits and leaves
    if random.random() > 0.3:    
        yield env.process(notBookingQueue(env, name))
    else: 
        yield env.process(bookingQueue(env, name)) 
    

def bookingQueue(env, name):
    # customer arrives to the system, waits and leaves
    arrive = env.now
    service_time = random.expovariate(0.5)
    with server1.request() as req:      
        results = yield req | env.timeout(maxWaitingTimeOfCustomer)

        if req in results:
            print('%7.4f : Get in booking queue Time of %s' % (env.now, name))
            servertime = service_time
            yield env.timeout(servertime)
            serviceTimes.append(servertime)
            print('%7.4f : Get out booking queue Time of %s' % (env.now, name))
            # print('%7.4f Time Spent in the queue of %s' % (env.now - arrive, name))
        else:
            waiting_time = env.now - arrive
            waitingTimes.append(waiting_time)
            print('%6.3f : Waiting time then left of %s' % (waiting_time, name))

def notBookingQueue(env, name):
    # customer arrives to the system, waits and leaves
    arrive = env.now
    service_time = random.expovariate(0.3)
    with server2.request() as req:        
        results = yield req | env.timeout(maxWaitingTimeOfCustomer)

        if req in results:
            print('%7.4f : Get in not booking queue Time of %s' % (env.now, name))
            servertime = service_time
            yield env.timeout(servertime)
            serviceTimes.append(servertime)
            print('%7.4f : Get out not booking queue Time of %s' % (env.now, name))
            # print('%7.4f Time Spent in the queue of %s' % (env.now - arrive, name))
        else:
            waiting_time = env.now - arrive
            waitingTimes.append(waiting_time)
            print('%6.3f : Waiting time then left of %s' % (waiting_time, name))
# def clinicalExamination():

random.seed(random_seed)
env1 = simpy.Environment()
server1 = simpy.Resource(env1, capacity=1)  # capacity changes the number of generators in the system.
server2 = simpy.Resource(env1, capacity=2)  # capacity changes the number of generators in the system.
env1.process(generator(env1, new_customers, interarrival))
env1.run()

# interarrivalTimes.append(interarrival)
# average_interarrival = statistics.mean(interarrivalTimes)
# average_serviceTime = statistics.mean(serviceTimes)
# print("Average Interarrival Time Is : %7.4f" % average_interarrival)
# print("Average Service Time Is : %7.4f" % average_serviceTime)

# if len(waitingTimes) > 0:
#     average_waitingTime = statistics.mean(waitingTimes)
#     print("Average Waiting Time Is : %7.4f" % average_waitingTime)

# for i in range (0, 10):
#     # n = np.random.poisson(6, size=None)
#     t = service_time=random.expovariate(0.2)
#     # print('n= ', n)
#     print('t= ', t)


