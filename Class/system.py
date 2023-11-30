import random
import numpy as np
import simpy
import statistics
from Class.patient import *
from Class.server import *
import math
import matplotlib.pyplot as plt
from tabulate import tabulate


class System():
    def __init__(self, env, bookingqueue, notbookingqueue, clinicalServer, pharmacyServer, testingServer, sugeryServer) -> None:
        self.env = env

        # Server
        self.bookingqueue = Server("Booking Server", bookingqueue, self, serviceTime=6, getTicket=True, priority=False)
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

        self.timeInSystem = []

        self.averageTime = []

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
                self.TimeInSystem(patient)
                patient.leaveSystem = True

            if(patient.joinTesting):
                yield self.env.process(self.testingServer.joinServer(patient))
                patient.joinTesting = False

                ratio = random.random()
                if ratio < 0.6:    
                    patient.joinPharmacy = True
                else:
                    self.TimeInSystem(patient)
                    patient.leaveSystem = True

            if(patient.joinSurgery):
                yield self.env.process(self.sugeryServer.joinServer(patient)) 
                patient.joinSurgery = False

                if ratio < 0.8:    
                    patient.joinPharmacy = True
                else:
                    
                    self.TimeInSystem(patient)
                    patient.leaveSystem = True
             
    def getTicket(self, patient):
        patient.ticketNumber = self.ticketNumber
        self.ticketNumber += 1 
    
    def TimeInSystem(self, patient):
        patient.leaveSystemTime = self.env.now
        self.timeInSystem.append(patient.leaveSystemTime - patient.joinSystemTime)

    def calculator(self):
        for server in self.server :
            # print("-----%s-----" % (server.serverName))
            if len(server.workingTime) > 0:
                average_serviceTime = statistics.mean(server.workingTime)
                # print("Average Service Time Is : %7.4f h" % average_serviceTime)
            else: average_serviceTime = 0

            if len(server.waitingTime) > 0:
                average_waitingTime = statistics.mean(server.waitingTime)
                # print("Average Waiting Time Is : %7.4f h" % average_waitingTime)
            else: average_waitingTime = 0

            if len(server.joinTime) > 0:
                average_joinTime = statistics.mean(server.joinTime)
                # print("Average Time between 2 joins Is : %7.4f h" % average_joinTime)
            else: average_joinTime = 0
            
            # print("Number of patients join server Is : %7.4f h" % server.patientNumber)

            self.averageTime.append([server.serverName, average_serviceTime, average_waitingTime, average_joinTime, server.patientNumber])
        
        head = ["Server Name", "Average Service Time", "Average Waiting Time", "Average Time between 2 joins", "Number of patients"]
 
        # display table
        print(tabulate(self.averageTime, headers=head, tablefmt="grid"))

        print("---------------")
        if len(self.timeInSystem) > 0:
                average_timeInSystem = statistics.mean(self.timeInSystem)
                print("Average Time in System Is : %7.4f h" % average_timeInSystem)
        print("---------------")
        
        
    def calculate_batch_means(self, batch_size):
        batch_variances = []       
        batch_means_server = []
        for num_batch in range(2, batch_size + 2):
            # print("num batch %i: "% num_batch)
            
            batch_means = []
            for server in self.server :
                # print("Sever working time %i :"%len(server.workingTime))
                num_batches = math.floor(len(server.workingTime)/num_batch)
                # print(num_batches)
                for num in range(num_batch):

                    batch_mean_list = []
                    for i in range(num_batches):
                        if len(server.workingTime) > (i + num*10) :
                            batch_mean_list.append(server.workingTime[i + num*10])
                    
                    
                    if(len(batch_mean_list) > 1):
                        batch_mean = statistics.mean(batch_mean_list) 
                        batch_means.append(batch_mean)                 
                        
                # print("len batch %i"%len(batch_means))
                    # overall_mean = statistics.mean(batch_means)
            if(len(batch_means) > 1):
                # print(len(batch_means))
                batch_means_server.append(statistics.mean(batch_means))
                # print("len batch all server %i : %7.4f"%(len(batch_means_server), batch_means_server[-1]))

            if(len(batch_means_server) > 1):
                batch_variance = statistics.variance(batch_means_server)
                batch_variances.append(batch_variance)

        # print("Size of batch_variances:", len(batch_variances)) 
        
        return batch_variances
    
    def histogram_batch_means(self, batch_size):
        # Calculate batch means and plot the variances over batches
        batch_variances = self.calculate_batch_means(batch_size)
        # num_batches = math.floor(len(self.server[1].workingTime)/num_batches)
        
        # if len(batch_variances) < num_batches:
        #     print("Warning: Not enough data for all batches.")
        #     num_batches = len(batch_variances)

        plt.plot(range(2, len(batch_variances) + 2), batch_variances, marker='.')
        plt.xlabel('Batch Number')
        plt.ylabel('Variance of Batch Means')
        plt.title('Batch Means Method - Working Time')
        plt.show()

    def QueueInServer(self):
        time_all = []
        numberQueue_all = []
        for server in self.server:
            time = []
            numerQueue = []
            # print(self.server[1].waitingQueue)
            for i in range(len(server.waitingQueue)):
                time.append(server.waitingQueue[i][1])
                numerQueue.append(server.waitingQueue[i][0])
            time_all.append(time)
            numberQueue_all.append(numerQueue)

        fig, ax = plt.subplots(3, 2, figsize=(8, 12))


        # Plot the first chart
        ax[0, 0].plot(time_all[0], numberQueue_all[0], 'r-', label='Booking Server')
        ax[0, 0].set_xlabel('Time')
        ax[0, 0].set_ylabel('Number patient wait in queue')
        ax[0, 0].legend()

        # Plot the second chart
        ax[0, 1].plot(time_all[1], numberQueue_all[1], 'g-', label='Not Booking Server')
        ax[0, 1].set_xlabel('Time')
        ax[0, 1].set_ylabel('Number patient wait in queue')
        ax[0, 1].legend()

        # Plot the third chart
        ax[1, 0].plot(time_all[2], numberQueue_all[2], 'b-', label='Clinical Server')
        ax[1, 0].set_xlabel('Time')
        ax[1, 0].set_ylabel('Number patient wait in queue')
        ax[1, 0].legend()

                # Plot the first chart
        ax[1, 1].plot(time_all[3], numberQueue_all[3], 'p-', label='Pharmarcy Server')
        ax[1, 1].set_xlabel('Time')
        ax[1, 1].set_ylabel('Number patient wait in queue')
        ax[1, 1].legend()

        # Plot the second chart
        ax[2, 0].plot(time_all[4], numberQueue_all[4], 'y-', label='Testing server')
        ax[2, 0].set_xlabel('Time')
        ax[2, 0].set_ylabel('Number patient wait in queue')
        ax[2, 0].legend()

        # Plot the third chart
        ax[2, 1].plot(time_all[5], numberQueue_all[5], 'm-', label='Surgery Server')
        ax[2, 1].set_xlabel('Time')
        ax[2, 1].set_ylabel('Number patient wait in queue')
        ax[2, 1].legend()

        # Adjust the spacing between subplots
        plt.tight_layout()

        # Show the plot
        plt.show()
