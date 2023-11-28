import random
import numpy as np
import simpy
import statistics

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
        arrive = env.now
        # print('%7.4f : Arrival time of %s' % (arrive, self.name))
        yield env.process(system.run(self))
        
class System():
    def __init__(self, env, bookingqueue, notbookingqueue, clinicalServer, pharmacyServer, testingServer, sugeryServer) -> None:
        self.env = env

        # Server
        self.bookingqueue = bookingqueue
        self.notbookingqueue = notbookingqueue
        self.clinicalServer = clinicalServer
        self.pharmacyServer = pharmacyServer
        self.testingServer = testingServer
        self.sugeryServer = sugeryServer

        # Waiting time
        self.WT_bookingqueue =[] 
        self.WT_notbookingqueue =[]
        self.WT_clinicalServer =[]
        self.WT_pharmacyServer =[]
        self.WT_sugeryServer =[]
        self.WT_testingServer =[]

        # Service time
        self.ST_bookingqueue =[] 
        self.ST_notbookingqueue =[]
        self.ST_clinicalServer =[]
        self.ST_pharmacyServer =[]
        self.ST_sugeryServer =[]
        self.ST_testingServer =[]

        # Number customer join server
        self.NC_bookingqueue = 0
        self.NC_notbookingqueue = 0
        self.NC_clinicalServer = 0
        self.NC_pharmacyServer = 0
        self.NC_sugeryServer = 0
        self.NC_testingServer = 0
        
        # Ticket number
        self.ticketNumber = 0  

    def run(self, patient):
        if random.random() > 0.3:    
            yield self.env.process(self.notBookingQueue(self.env, patient, 5))
        else: 
            yield self.env.process(self.bookingQueue(self.env, patient, 4)) 

        while(not patient.leaveSystem):
            if(patient.joinClinical):
                yield self.env.process(self.clinicalExamination(self.env, patient, 2)) 
            if(patient.joinPharmacy):
                yield self.env.process(self.pharmacyArea(self.env, patient, 3)) 
            if(patient.joinTesting):
                yield self.env.process(self.TestingRoom(self.env, patient, 4))
            if(patient.joinSurgery):
                yield self.env.process(self.SurgeryRoom(self.env, patient, 2)) 
             
    def getTicket(self, patient):
        patient.ticketNumber = self.ticketNumber
        self.ticketNumber += 1 
        
    def bookingQueue(self, env, patient, timeService):
        # customer arrives to the system, waits and leaves
        arrive = env.now
        service_time = random.expovariate(timeService)
        # maxWaitingTimeOfCustomer = np.random.poisson(3, size=None)

        with self.bookingqueue.request() as req:      
            # results = yield req | env.timeout(maxWaitingTimeOfCustomer)
                yield req
                self.NC_bookingqueue += 1 

            # if req in results:
                self.getTicket(patient)
                print('%7.4f : %s join booking server[%i/%i] after wait %7.4f' % (env.now, patient.name, self.bookingqueue.count, self.bookingqueue.capacity, env.now-arrive))
                self.WT_bookingqueue.append(env.now-arrive)
                servertime = service_time
                yield env.timeout(servertime)
                self.ST_bookingqueue.append(servertime)
                print('%7.4f : %s leave booking server after %7.4f with number ticket %i' % (env.now, patient.name, servertime, patient.ticketNumber))
                patient.joinClinical = True
            # else:
            #     waiting_time = env.now - arrive
            #     # waitingTimes.append(waiting_time)
            #     print('%s Waiting %6.3f at booking queue then left' % (patient.name, waiting_time))
            #     patient.leaveSystem = True
    
    def notBookingQueue(self, env, patient, timeService):
        # customer arrives to the system, waits and leaves
        arrive = env.now
        service_time = random.expovariate(timeService)
        # maxWaitingTimeOfCustomer = np.random.poisson(3, size=None)

        with self.notbookingqueue.request() as req:        
            # results = yield req | env.timeout(maxWaitingTimeOfCustomer)
                yield req
                self.NC_notbookingqueue += 1
            # if req in results:
                print('%7.4f : %s join not booking server[%i/%i] after wait %7.4f' % (env.now, patient.name, self.notbookingqueue.count, self.notbookingqueue.capacity, env.now-arrive))
                self.WT_notbookingqueue.append(env.now-arrive)
                servertime = service_time
                yield env.timeout(servertime)
                self.ST_notbookingqueue.append(servertime)
                self.getTicket(patient)
                print('%7.4f : %s leave not booking server after %7.4f with number ticket %i' % (env.now, patient.name, servertime, patient.ticketNumber))
                patient.joinClinical = True
            # else:
            #     waiting_time = env.now - arrive
            #     # waitingTimes.append(waiting_time)
            #     print('%s Waiting %6.3f at not booking queue then left' % (patient.name, waiting_time))
            #     patient.leaveSystem = True
   
    def clinicalExamination(self, env, patient, timeService):
        arrive = env.now
        service_time = random.expovariate(timeService)
        # maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)

        with self.clinicalServer.request(patient.ticketNumber, False) as req:       
            yield req 
            self.NC_clinicalServer += 1
            print('%7.4f : %s join clinical server[%i/%i] after wait %7.4f with number ticket %i' % (env.now, patient.name, self.clinicalServer.count, self.clinicalServer.capacity, env.now-arrive, patient.ticketNumber))
            self.WT_clinicalServer.append(env.now-arrive)
            servertime = service_time
            yield env.timeout(servertime)
            self.ST_clinicalServer.append(servertime)
            print('%7.4f : %s leave clinical server after %7.4f' % (env.now, patient.name, servertime))
            # print('%7.4f Time Spent in the queue of %s' % (env.now - arrive, patient.name))
            
            ratio = random.random()
            if ratio < 0.4:    
                patient.joinPharmacy = True
            elif ratio > 0.6: 
                patient.joinSurgery = True
            else:
                patient.joinTesting = True
                          
    def pharmacyArea(self, env, patient, timeService):
        arrive = env.now
        service_time = random.expovariate(timeService)
        # maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)

        with self.pharmacyServer.request() as req:     
            yield req 
            self.NC_pharmacyServer += 1  
            print('%7.4f : %s join pharmacy server[%i/%i] after wait %7.4f with number ticket %i' % (env.now, patient.name, self.pharmacyServer.count, self.pharmacyServer.capacity, env.now-arrive, patient.ticketNumber))
            self.WT_pharmacyServer.append(env.now-arrive)
            servertime = service_time
            yield env.timeout(servertime)
            self.ST_pharmacyServer.append(servertime)
            print('%7.4f : %s leave pharmacy server after %7.4f' % (env.now, patient.name, servertime))
            # print('%7.4f Time Spent in the queue of %s' % (env.now - arrive, patient.name))
            patient.leaveSystem = True
    
    def SurgeryRoom(self, env, patient, timeService):
        arrive = env.now
        service_time = random.expovariate(timeService)
        # maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)

        with self.sugeryServer.request() as req: 
            yield req     
            self.NC_sugeryServer += 1  
            print('%7.4f : %s join surgery room server[%i/%i] after wait %7.4f with number ticket %i' % (env.now, patient.name, self.sugeryServer.count, self.sugeryServer.capacity, env.now-arrive, patient.ticketNumber))
            self.WT_sugeryServer.append(env.now-arrive)
            servertime = service_time
            yield env.timeout(servertime)
            self.ST_sugeryServer.append(servertime)
            print('%7.4f : %s leave surgery room after %7.4f' % (env.now, patient.name, servertime))
            # print('%7.4f Time Spent in the queue of %s' % (env.now - arrive, patient.name))
            
            ratio = random.random()
            if ratio < 0.8:    
                patient.joinPharmacy = True
            else:
                patient.leaveSystem = True

    def TestingRoom(self, env, patient, timeService):
        arrive = env.now
        service_time = random.expovariate(timeService)
        # maxWaitingTimeOfCustomer = np.random.poisson(4, size=None)

        with self.testingServer.request() as req:  
            yield req    
            self.NC_testingServer += 1   
            print('%7.4f : %s join testing room server[%i/%i] after wait %7.4f with number ticket %i' % (env.now, patient.name, self.testingServer.count, self.testingServer.capacity, env.now-arrive, patient.ticketNumber))
            self.WT_pharmacyServer.append(env.now-arrive)
            servertime = service_time
            yield env.timeout(servertime)
            self.ST_testingServer.append(servertime)
            print('%7.4f : %s leave testing room after %7.4f' % (env.now, patient.name, servertime))
            # print('%7.4f Time Spent in the queue of %s' % (env.now - arrive, patient.name))
            
            ratio = random.random()
            if ratio < 0.6:    
                patient.joinPharmacy = True
            else:
                patient.leaveSystem = True

    def calculatorTime(self, waitingTimes, serviceTimes , numberCustomers):
        # interarrivalTimes.append(interarrival)
        # average_interarrival = statistics.mean(interarrivalTimes)
        if len(serviceTimes) > 0:
            average_serviceTime = statistics.mean(serviceTimes)
            # print("Average Interarrival Time Is : %7.4f" % average_interarrival)
            print("Average Service Time Is : %7.4f" % average_serviceTime)

        if len(waitingTimes) > 0:
            average_waitingTime = statistics.mean(waitingTimes)
            print("Average Waiting Time Is : %7.4f" % average_waitingTime)
        
        print("Number of customer joins server Is : %7.4f" % numberCustomers)

    
        


    

                