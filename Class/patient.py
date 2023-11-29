import random
import numpy as np
import simpy
import statistics
from Class.system import *

class Patient ():
    
    def __init__(self, env, name) -> None:
        self.env = env
        self.name = name
        self.ticketNumber = 0

        self.joinClinical = False

        self.joinPharmacy = False
        self.joinTesting = False
        self.joinSurgery = False

        self.leaveSystem = False

    def joinSystem(self, env, system):
        # arrive = env.now
        # print('%7.4f : Arrival time of %s' % (arrive, self.name))
        yield env.process(system.run(self))





    
        


    

                