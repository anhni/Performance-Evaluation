import numpy as np
import matplotlib.pyplot as plt

# Generate 1000 samples from an exponential distribution with lambda = 1
samples_expo = np.random.exponential(1.0 / (np.random.poisson(10, size=None) + 0.01), 1000)

# Generate 1000 samples from a Poisson distribution with lambda = 1
samples_poisson = np.random.poisson(10, 1000)

# Plot the histograms of the samples
plt.hist(samples_expo, label="Exponential Distribution")
plt.hist(samples_poisson, label="Poisson Distribution")
plt.xlabel("Sample Value")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# import random
# import simpy
# import numpy as np
# from random import seed
# from Class.patient import *

# seed(29381)  # for seed of randint function
# random_seed = 41  # for seed of other random generators
# new_customers = 20  # Total number of customers in the system
# interarrival = np.random.poisson(3, size=None)  # Generate new customers roughly every x seconds
# maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)
# patientNumber = 0
# waitingTimes = []
# serviceTimes = []
# interarrivalTimes = []

# interval = np.random.poisson(10, size=None) 

# for i in range(0,10):
#     # print(np.random.poisson(4, size=None))
#     # print(random.expovariate(1.0 / (interval + 0.01)))
#     # print(random.expovariate(0.1))
#     print(random.expovariate(1.0 / (np.random.poisson(10, size=None) + 0.01)))

