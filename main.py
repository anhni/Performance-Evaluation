import random
import simpy
import numpy as np
from random import seed
from Class.system import *


# seed(2983)  # for seed of randint function
# random_seed = 31  # for seed of other random generatorss
new_customers = 20  # Total number of customers in the system
interarrival = np.random.poisson(0.1, size=None)  # Generate new customers roughly every x seconds
maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)


def generator(env, number, interval):  # customer generator with interarrival times.
    """generator generates customers randomly"""
    for i in range(number):
        newPatient = Patient(env1, 'Customer %02d' % i)
        env.process(newPatient.joinSystem(env1, newSystem))
        t = random.expovariate(1.0 / (interval + 0.01))
        yield env.timeout(t)  # adds time to the counter, does not delete from the memory
    

# random.seed(random_seed)
env1 = simpy.Environment()
bookingServer = simpy.Resource(env1, capacity = 1)  # capacity changes the number of generators in the system.
notBookingServer = simpy.Resource(env1, capacity = 2)
clinicalServer = simpy.PriorityResource(env1, capacity = 6)
pharmacyServer = simpy.Resource(env1, capacity = 3)
specializedServer = simpy.Resource(env1, capacity = 4)
testingServer = simpy.Resource(env1, capacity = 2)

newSystem = System(env1, bookingServer, notBookingServer, clinicalServer, pharmacyServer, specializedServer, testingServer)

env1.process(generator(env1, new_customers, interarrival))
env1.run()

newSystem.calculator()


