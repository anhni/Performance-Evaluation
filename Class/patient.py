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

        self.joinSystemTime = 0
        self.leaveSystemTime = 0

    def joinSystem(self, env, system):
        self.joinSystemTime = env.now
        yield env.process(system.run(self))





    
        


    

                