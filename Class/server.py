import random
import numpy as np
import simpy
import statistics
from Class.patient import *

class Server():
    def __init__(self, serverName, resource, system, serviceTime, getTicket) -> None:
        self.serverName = serverName
        self.resource = resource
        self.system = system
        self.env = system.env
        self.serviceTime = serviceTime
        self.getTicket = getTicket

        self.waitingTime = [] # waiting time 
        self.workingTime = [] # service time in reality
        self.patientNumber = 0 # Number customer join server
        self.joinTime = [] # Time patient join server
        self.lastTimeinServer = 0 # time that last time patient in server
        self.join = False

    def joinServer(self):
        arrive = self.env.now
        service_time = random.expovariate(self.serviceTime)

        with self.resource.request() as req:      
            yield req

            self.patientNumber += 1 

            # Calculate join time, time between 2 joins
            if self.patientNumber > 1 :
                self.joinTime.append(self.env.now - self.lastTimeinServer)
                # print("between time: %7.4f" % (env.now - self.lastTimeinServer))
            self.lastTimeinServer = self.env.now

            # Patient get number ticket
            if(self.getTicket):
                self.system.getTicket(self.system.patient)

            print('%7.4f : %s join %s[%i/%i] after wait %7.4f' % (self.env.now, self.system.patient.name, self.serverName, self.resource.count, self.resource.capacity, self.env.now-arrive))
            
            self.waitingTime.append(self.env.now - arrive)

            yield self.env.timeout(service_time)
            
            self.workingTime.append(service_time)
            print('%7.4f : %s leave %s after %7.4f with number ticket %i' % (self.env.now, self.system.patient.name, self.serverName, service_time, self.system.patient.ticketNumber))
            
            

