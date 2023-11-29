import random
import simpy
import numpy as np
from random import seed
from Class.patient import *
from Class.system import *
from Class.server import *
import statistics


seed(2983)  # for seed of randint function
random_seed = 32  # for seed of other random generators
new_customers = 20  # Total number of customers in the system
interarrival = np.random.poisson(0.1, size=None)  # Generate new customers roughly every x seconds
maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)
patientNumber = 0
waitingTimes = []
serviceTimes = []
interarrivalTimes = []

def generator(env, number, interval):  # customer generator with interarrival times.
    """generator generates customers randomly"""
    for i in range(number):
        newPatient = Patient(env1, 'Customer %02d' % i)
        env.process(newPatient.joinSystem(env1, newSystem))
        t = random.expovariate(1.0 / (interval + 0.01))
        yield env.timeout(t)  # adds time to the counter, does not delete from the memory
    

random.seed(random_seed)
env1 = simpy.Environment()
bookingServer = simpy.Resource(env1, capacity=1)  # capacity changes the number of generators in the system.
notBookingServer = simpy.Resource(env1, capacity=2)
clinicalServer = simpy.PriorityResource(env1, capacity=6)
pharmacyServer = simpy.Resource(env1, capacity=3)
specializedServer = simpy.Resource(env1, capacity=4)
testingServer = simpy.Resource(env1, capacity=2)

newSystem = System(env1, bookingServer, notBookingServer, clinicalServer, pharmacyServer, specializedServer, testingServer)

hahaServer = Server("haha", simpy.Resource(env1, capacity=2), newSystem, 3, True)

env1.process(generator(env1, new_customers, interarrival))
env1.run()

print("----booking server----")
newSystem.calculatorTime(newSystem.WT_bookingqueue, newSystem.ST_bookingqueue, newSystem.JT_bookingqueue, newSystem.NC_bookingqueue)

print("----not booking server----")
newSystem.calculatorTime(newSystem.WT_notbookingqueue, newSystem.ST_notbookingqueue, newSystem.JT_notbookingqueue, newSystem.NC_notbookingqueue)

print("----clinical server----")
newSystem.calculatorTime(newSystem.WT_clinicalServer, newSystem.ST_clinicalServer, newSystem.JT_clinicalServer, newSystem.NC_clinicalServer)

print("----pharmacy area server----")
newSystem.calculatorTime(newSystem.WT_pharmacyServer, newSystem.ST_pharmacyServer, newSystem.JT_pharmacyServer, newSystem.NC_pharmacyServer)

print("----minor surgery server----")
newSystem.calculatorTime(newSystem.WT_sugeryServer, newSystem.ST_sugeryServer, newSystem.JT_sugeryServer, newSystem.NC_sugeryServer)

print("----testing room server----")
newSystem.calculatorTime(newSystem.WT_testingServer, newSystem.ST_testingServer, newSystem.JT_testingServer, newSystem.NC_testingServer)

