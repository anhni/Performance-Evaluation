import random
import numpy as np
import simpy
import statistics
from Class.patient import *
from Class.server import *

class System():
    def __init__(self, env, bookingqueue, notbookingqueue, clinicalServer, pharmacyServer, testingServer, sugeryServer) -> None:
        self.env = env

        # Server
        self.bookingqueue = Server("Booking Server", bookingqueue, self, 6, True, False)
        self.notbookingqueue = Server("Not Booking Server", notbookingqueue, self, 5, True, False)
        self.clinicalServer = Server("clinical Server", clinicalServer, self, 2, False, True)
        self.pharmacyServer = Server("pharmacy Server", pharmacyServer, self, 3, False, False)
        self.testingServer = Server("testing Server", testingServer, self, 4, False, False)
        self.sugeryServer = Server("sugery Server", sugeryServer, self, 2, False, False)

        self.server = []
        self.server.append(self.bookingqueue)
        self.server.append(self.notbookingqueue)
        self.server.append(self.clinicalServer)
        self.server.append(self.pharmacyServer)
        self.server.append(self.testingServer)
        self.server.append(self.sugeryServer)

        self.ticketNumber = 0

    def run(self, patient):
        if random.random() > 0.3:    
            yield self.env.process(self.notbookingqueue.joinServer(patient))
        else:  
            yield self.env.process(self.bookingqueue.joinServer(patient)) 
        patient.joinClinical = True


        while(not patient.leaveSystem):
            if(patient.joinClinical):
                yield self.env.process(self.clinicalServer.joinServer(patient))
                patient.joinClinical = False 

                ratio = random.random()
                if ratio < 0.4:    
                    patient.joinPharmacy = True
                elif ratio > 0.6: 
                    patient.joinSurgery = True
                else:
                    patient.joinTesting = True

            
            if(patient.joinPharmacy):
                yield self.env.process(self.pharmacyServer.joinServer(patient))
                patient.joinPharmacy = False

                patient.leaveSystem = True

            if(patient.joinTesting):
                yield self.env.process(self.testingServer.joinServer(patient))
                patient.joinTesting = False

                ratio = random.random()
                if ratio < 0.6:    
                    patient.joinPharmacy = True
                else:
                    patient.leaveSystem = True

            if(patient.joinSurgery):
                yield self.env.process(self.sugeryServer.joinServer(patient)) 
                patient.joinSurgery = False

                if ratio < 0.8:    
                    patient.joinPharmacy = True
                else:
                    patient.leaveSystem = True
             
    def getTicket(self, patient):
        patient.ticketNumber = self.ticketNumber
        self.ticketNumber += 1 

    def calculator(self):
        for server in self.server :
            print("-----%s-----" % (server.serverName))
            if len(server.workingTime) > 0:
                average_serviceTime = statistics.mean(server.workingTime)
                # print("Average Interarrival Time Is : %7.4f" % average_interarrival)
                print("Average Service Time Is : %7.4f" % average_serviceTime)

            if len(server.waitingTime) > 0:
                average_waitingTime = statistics.mean(server.waitingTime)
                print("Average Waiting Time Is : %7.4f" % average_waitingTime)

            if len(server.joinTime) > 0:
                average_joinTime = statistics.mean(server.joinTime)
                print("Average Time between 2 joins Is : %7.4f" % average_joinTime)
            
            print("Number of customer joins server Is : %7.4f" % server.patientNumber)
