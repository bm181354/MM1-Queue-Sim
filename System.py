from SimPy.Simulation import *
import random as r
from numpy.random import seed, uniform,exponential
import argparse


# First Name: Biken 
# Last Name: Maharjan
# BU ID: #ID Removed for Security reason

#You can add any extra helper methods to these classes as you see fit#.


#You must modify this class#
class Parameters:
    '''In this class, you must just define the following variables of your distribution:
    These variables will be hardcoded with values. Please refer to the assignment handout what
    these values must be. You can use the values appropiately in your code by calling Parameters.NAME_OF_VARIABLE
    --For Poisson Arrivals and Exponential Service Time
      1) lambda for poisson arrivals
      2) Ts for service time

    --For Uniform Arrivals and Uniform Service Time
       3) interarrivalTimeMin and interarrivalTimeMax for Uniform distribution.
       4) serviceTimeMin and serviceTimeMax for Uniform distribution.
    5. numberOfServers in your computing system
    6. simulationTime in hrs. '''
    TOTAL_SIMULATION = 10000 #
    
    arrivals_poisson = 10.0
    service_time = 8.0 # 
    #-----[Uniform]--
    interarrivalTimeMin = 1.5
    interarrivalTimeMax = 3.5
    serviceTimeMin = 2.5
    serviceTimeMax = 6.5
    #----------------
    numberOfServers = 1  # 
    seed = 123

    
    

##### Processes #####
# Customer
class Packet(Process):
    def behavior_of_single_packet(self,cs):
        '''You must implement this method. This method is the behavior of a single packet
        when it interacts with the queue of your computing system. These are some questions you will want to think about
        1. What happens when the packet arrives? Does it get serviced immediately or gets put in the queue?
        2. If it does get serviced, how long will it be serviced for? Or does it get put in the queue?
        3. When does it depart?

        The cs in the method is an instance of the Computing System class'''
        if args.generateRawResults == False:
            ########
            print("Time: {}: {} is arriving in the System".format(now(),self.name))
            packet_arrives = now()
            if now() > 120:
                length_of_system = len(cs.activeQ)
                length_of_queue =  len(cs.waitQ)
                #print(length_of_queue)
                mn.observe(length_of_queue) # (x,_)
                p.observe(length_of_system + length_of_queue)               
            # Customer arrives, joins queue
            yield request,self,cs
            waiting_time = now() - packet_arrives

            
            #active_time = cs.actMon.mean()
            #total_time = active_time + waiting_time
            ####
            if now() > 120:
                #print("----------")
                #print("Waiting time:")
                m.observe(waiting_time)
            print("Time : {}: {} is about to be service".format(now(),self.name))
            #print("This is %f , %f " %(now(),self.name) )
            #print(args.type)
            ##
            if args.type == 'MM1' or args.type == 'MM2':
                yield hold, self,exponential(Parameters.service_time)
            else:
                yield hold, self,uniform(Parameters.serviceTimeMin,Parameters.serviceTimeMax)
            ##
            yield release,self,cs
            print("Time: {}: {} is done with the service ".format(now(),self.name))
            # for total time taken calculation
            packet_out = now()
            total_time = (packet_out - packet_arrives)
            t.observe(total_time)      
                  
            ########
            
        elif args.generateRawResults == True:
            packet_arrives = now()
            if now() > 120:
                
                length_of_queue =  len(cs.waitQ)
                mn.observe(length_of_queue) # (x,_)
            
            yield request,self,cs
            waiting_time = now() - packet_arrives
            ####
            if now() > 120:
                m.observe(waiting_time)
            if args.type == 'MM1' or args.type == 'MM2':
                yield hold, self,exponential(ts) # change i (_,y)
            else:
                yield hold, self,uniform(ts)
            yield release,self,cs
            ########
            

# Packet Generator class.
class PacketGenerator(Process):
        def createPackets(self,cs):
            '''You must complete this method. This method generates and creates packets as per the
            arrival rate distribution defined'''
            i = 0
            while True:
                
                ##
                if args.type == 'MM1' or args.type == 'MM2':
                    yield hold, self,exponential(Parameters.arrivals_poisson)
                ##
                else:
                    yield hold, self,uniform(Parameters.interarrivalTimeMin,Parameters.interarrivalTimeMax)
                packet_name = "Packet " + str(i)
                p = Packet(name = packet_name)
                activate(p,p.behavior_of_single_packet(cs))
                i= i + 1
                
#You do not need to modify this class.
class ComputingSystem(Resource):
    pass
#You can modify this model method#.
## Model ---------------------------------------
#[GOOD]
def model():
    # Seed the generator using seed value of 123.
    seed(Parameters.seed) 
    initialize()
    p = PacketGenerator() 
    cs = ComputingSystem(capacity= Parameters.numberOfServers, monitored = True, monitorType = Monitor)
    activate(p,p.createPackets(cs))
    simulate(until = Parameters.TOTAL_SIMULATION)
    value = cs.waitMon.mean() #
    ####
    #print(value)
    
    
#Change the below, as per the requirements of the assignment.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-generateRawResults','-generateRawResults', action ='store_true')
    parser.add_argument('--type', help = ' Type model',type = str)
    #parser.add_argument('--type',required =True, help = ' Type model',metavar ='MM1')
    #parser.add_argument('--type',required =True, help = ' Type model',metavar ='MM2')
    args = parser.parse_args()
    m = Monitor()
    
    active_time = 0.0
    total_time = 0.0
    waiting_time = 0
    
    mn = Monitor()
    ts = 0.5
    p = Monitor()
    t = Monitor()              
    if args.generateRawResults == False:
    ############
        print(args.type)
        if args.type == "MM1":
            Parameters.numberOfServers = 1
            model()
        elif args.type == "MM2":
            Parameters.numberOfServers = 2
            model()
        elif args.type == "UU1":
            Parameters.numberOfServers = 1
            model()
        #--[MEAN]-------
        print("________%s_______"%(args.type))
        
        print("-------Waiting_time-------")       
        print("Average Waiting time in Queue (Tw): ")                       
        print(m.mean()) # mean of waiting time
        
        print("-------QUEUE_LENGTH-------")
        print("Average of queue length (w):")                       
        print(mn.mean()) # mean of queue_length
        
        print("Average of System length (q):")
        print(p.mean())
        
        print("Total time taken in the system(tq):")
        print(t.mean())
        ##############
    else:
        while ts < 11.5:
            for i in range(0,10):
                Parameters.seed = i
                if args.type == "MM1":
                    Parameters.numberOfServers = 1
                    model()
                elif args.type == "MM2":
                    Parameters.numberOfServers = 2
                    model()
                elif args.type == "UU1":
                    Parameters.numberOfServers = 1
                    model()
                #print("ts: %f, Average Queue Length %f  " %(ts,mn.mean()))
                #print(ts)
                #print("---------------")
                print(mn.mean())
                mn.reset()
                m.reset()
            print(" ")    
            ts = ts + 0.5    
        ##############      
       

    
    
    
    
