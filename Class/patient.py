import random
import numpy as np
import simpy

class Patient ():
    
    def __init__(self, env, name) -> None:
        self.env = env
        self.name = name
        self.ticketNumber = 0
        self.joinclinical = False

        self.leaveSystem = False

    def joinSystem(self, env, system):
        arrive = env.now
        # print('%7.4f : Arrival time of %s' % (arrive, self.name))
        yield env.process(system.run(self))
        
class System():
    def __init__(self, env, bookingqueue, notbookingqueue, clinicalServer) -> None:
        self.env = env
        self.bookingqueue = bookingqueue
        self.notbookingqueue = notbookingqueue
        self.clinicalServer = clinicalServer
        self.ticketNumber = 0
    

    def run(self, patient):
        if random.random() > 0.3:    
            yield self.env.process(self.notBookingQueue(self.env, patient))
        else: 
            yield self.env.process(self.bookingQueue(self.env, patient)) 

        while(not patient.leaveSystem):
            yield self.env.process(self.clinicalExamination(self.env, patient)) 
        

        

    
    def getTicket(self, patient):
        patient.ticketNumber = self.ticketNumber
        self.ticketNumber += 1 
        
    def bookingQueue(self, env, patient):
        # customer arrives to the system, waits and leaves
        arrive = env.now
        service_time = random.expovariate(0.5)
        maxWaitingTimeOfCustomer = np.random.poisson(3, size=None)

        with self.bookingqueue.request() as req:      
            results = yield req | env.timeout(maxWaitingTimeOfCustomer)

            if req in results:
                self.getTicket(patient)
                print('%7.4f : %s join booking server[%i/%i] after wait %7.4f' % (env.now, patient.name, self.bookingqueue.count, self.bookingqueue.capacity, env.now-arrive))
                servertime = service_time
                yield env.timeout(servertime)
                # serviceTimes.append(servertime)
                print('%7.4f : %s leave booking server after %7.4f with number ticket %i' % (env.now, patient.name, servertime, patient.ticketNumber))
                patient.joinClinical = True
            else:
                waiting_time = env.now - arrive
                # waitingTimes.append(waiting_time)
                print('%s Waiting %6.3f at booking queue then left' % (patient.name, waiting_time))
                patient.leaveSystem = True
    
    def notBookingQueue(self, env, patient):
        # customer arrives to the system, waits and leaves
        arrive = env.now
        service_time = random.expovariate(0.3)
        maxWaitingTimeOfCustomer = np.random.poisson(3, size=None)

        with self.notbookingqueue.request() as req:        
            results = yield req | env.timeout(maxWaitingTimeOfCustomer)

            if req in results:
                print('%7.4f : %s join not booking server[%i/%i] after wait %7.4f' % (env.now, patient.name, self.notbookingqueue.count, self.notbookingqueue.capacity, env.now-arrive))
                servertime = service_time
                yield env.timeout(servertime)
                # serviceTimes.append(servertime)
                self.getTicket(patient)
                print('%7.4f : %s leave not booking server after %7.4f with number ticket %i' % (env.now, patient.name, servertime, patient.ticketNumber))
                patient.joinClinical = True
            else:
                waiting_time = env.now - arrive
                # waitingTimes.append(waiting_time)
                print('%s Waiting %6.3f at not booking queue then left' % (patient.name, waiting_time))
                patient.leaveSystem = True

    
    # def clinicalExamination(self, env, patient):
    #     arrive = env.now
    #     service_time = random.expovariate(0.3)
    #     maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)

    #     with self.notbookingqueue.request(priority = patient.ticketNumber) as req:        
    #         results = yield req | env.timeout(maxWaitingTimeOfCustomer)

    #         if req in results:
    #             print('%7.4f : Get in clinical examination Time of %s' % (env.now, patient.name))
    #             servertime = service_time
    #             yield env.timeout(servertime)
    #             # serviceTimes.append(servertime)
    #             self.getTicket(patient)
    #             print('%7.4f : Get out clinical examination Time of %s with number ticket %i' % (env.now, patient.name, patient.ticketNumber))
    #             # print('%7.4f Time Spent in the queue of %s' % (env.now - arrive, patient.name))
    #         else:
    #             waiting_time = env.now - arrive
    #             # waitingTimes.append(waiting_time)
    #             print('%6.3f : Waiting time at clinical examination then left of %s' % (waiting_time, patient.name))
    
    def clinicalExamination(self, env, patient):
        arrive = env.now
        service_time = random.expovariate(1.0 / (np.random.poisson(10, size=None) + 0.01))
        # maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)

        with self.clinicalServer.request(patient.ticketNumber, False) as req:        
            print('%7.4f : %s join clinical server[%i/%i] after wait %7.4f with number ticket %i' % (env.now, patient.name, self.clinicalServer.count, self.clinicalServer.capacity, env.now-arrive, patient.ticketNumber))
            servertime = service_time
            yield env.timeout(servertime)
            # serviceTimes.append(servertime)
            print('%7.4f : %s leave clinical server after %7.4f' % (env.now, patient.name, servertime))
            # print('%7.4f Time Spent in the queue of %s' % (env.now - arrive, patient.name))
            patient.leaveSystem = True
                