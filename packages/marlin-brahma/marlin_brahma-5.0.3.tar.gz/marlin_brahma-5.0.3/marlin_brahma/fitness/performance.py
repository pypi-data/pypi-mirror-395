

import os, sys, time, random, logging
import inspect

# import custom decisions

# from decisions import *
# from custom_decisions.decisions import *
# modulename = 'custom_decisions'
#     #print (sys.path)
# if modulename not in sys.modules:
#     print('You have not imported the {} module'.format(modulename))
    

# if not 'IdentEvaluation' in inspect.getmembers(modulename):
#     print('You have not imported the {} class'.format('IdentEvaluation'))
    
    


class RootDecision(object):
    """Decision involve an entry and exit. This is the decision entry. Stimuli initiate a decision. We then resolve that decision
    as part of a fitness function

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self, decision_type="", decision_status=None, type = "none"):
        if decision_status != "":
            self.DecisionType = decision_type
            self.DecisionStatus = decision_status
            self.Type = type
        else:
            print ("Critical Error in Decision Root")
            print (decision_status)
            print (decision_type)
            #exit()

    def __str__(self):
        return ("Root decision")

class DecisionProfile(object):
    """Decision Profile holder. This can be extended for more
    complex decision making algorithms. Trade decisions will simply
    have entry and exit. Decision profile closed by adding decision with
    status 0. returns decision with profile 2 ( a measured decision )


    Arguments:
        object {[type]} -- [description]

    """
    def __init__(self, decision = None, min_number_decisions = 2):
        self.Decision_id = "decision_profile" + str(random.randint(1,100000))
        self.DecisionList = []
        self.Type = decision.Type
        self.Status = "Open"
        #mnin nunber decisions required for evqaluation..
        self.minNumberRequired = min_number_decisions
        if decision != None:
            
            self.DecisionList.append(decision)


    def __str__(self):
        number_decisions = len(self.DecisionList)
        return (f'id: {self.Decision_id} number: {number_decisions} type: {self.Type}')

    def force_close_decision(self):
        """Shut down this decision profile
        """
        self.Status = 'Closed'


    def add_decision(self, decision):
        #print ("ADDING DECIIONS")
        #self.DecisionList.append(decision)
        d_result = None
        if decision.DecisionStatus == 0:
            #shutting down profile
            self.Status = 'Closed'
            self.DecisionList.append(decision)
            
            #d_result = self.evaluate_thinking()
            #self.DecisionList.append(d_result)

        if decision.DecisionStatus == 1:
            #add decision
            self.Status = 'Open'
            self.DecisionList.append(decision)
            
            #d_result = self.evaluate_thinking()
            #self.DecisionList.append(d_result)
            #check against constraints
            #if test fail, set closed and add result
            #decion to list

        return d_result


    #obsolete!!!
    def evaluate_thinking(self):
        """get the result data for this decision profile

        Returns:
            [type] -- [description]
        """
        decisionResult = None
        if self.Type == "trade":
            decisionResult = TradeDecisionResult()
            decisionResult.evaluate_result(decision_profile=self.DecisionList)
            return decisionResult

        else:
            return decisionResult

class RootResult(object):
    """Root Decision for performance storing. All decisions end with a result. This is the root class
    of the result

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self, decision_type = ""):
        self.DecisionType = decision_type
        self.Success = None
        self.Fitness = 0

    def __str__(self):
        return ""

class DailyPerformance(object):
    """Performance dataPerformance is discretised into daily buckets or epoch buckets.
    This is used by the evolution classes to rank and select and
    is therefore generic. Simply defines fitness values.
    Data more specific to the actual decision can be made
    using the decision profile data
    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self, date):
        """Initialise by passing date for which data is relevant

        Arguments:
            date {[type]} -- [description]
        """

        self.DecisionProfiles = []  #decision profiles
                                    #(includes specialised results for real deciison results)
        self.Decisions = []         #all decisions

    def add_decision(self, decision):
        """Add result to daily data.

        Keyword Arguments:
            date {str} -- [description] (default: {""})
            time_entry {str} -- [description] (default: {""})
            time_exit {str} -- [description] (default: {""})
            market {str} -- [description] (default: {""})
            pl {float} -- [description] (default: {0.0})
        """

        #append decisions - general list
        self.Decisions.append(decision)

        #add/create new decision profile
        numberProfiles = len(self.DecisionProfiles)
        if numberProfiles > 0:
            if self.DecisionProfiles[numberProfiles-1].Status == "Open":
                #add to existing profile
                self.DecisionProfiles[numberProfiles - 1].add_decision(decision)
                return

            #closed status after adding decision
            if self.DecisionProfiles[numberProfiles-1].Status == "Closed":
              
               #need new profile
               
               decisionProfile = DecisionProfile(decision)
               self.DecisionProfiles.append(decisionProfile)
               decisionProfile = None
               return

        else:
            decisionProfile = DecisionProfile(decision)
            self.DecisionProfiles.append(decisionProfile)
            decisionProfile = None



    def __str__(self):
        return ("Date: {0} ; Number Trades: {1} ; Number + {2} ; Number - {3} ; Total PL {4}".format(self.Date, self.NumberOfTrades, self.NumberPositive, self.NumberNegative, self.TotalPL))

class BotPerformance(object):
    """Individual bt performance recorder.

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self):

        self.PerformanceHolder = {}
        self.LastDecision = None



    def __str__(self):
        return_str = ""
        for date,value in self.PerformanceHolder.items():
            return_str += ((self.PerformanceHolder[date].__str__()))
            return_str += "\n"
        return return_str

    def getLastBotDecision(self):
        return self.LastDecision

    def add_decision(self, decision, epoch):
        """add individual decision result data. e.g. trade If the date doesn't already exist, add it

        Keyword Arguments:
            date {str} -- [description] (default: {""})
            time_entry {str} -- [description] (default: {""})
            time_exit {str} -- [description] (default: {""})
            market {str} -- [description] (default: {""})
            pl {float} -- [description] (default: {0.0})

        """
        self.LastDecision = decision
        if epoch in self.PerformanceHolder:
            self.PerformanceHolder[epoch].add_decision(decision)
        else:
            dailyPerformace = DailyPerformance(epoch)
            self.PerformanceHolder[epoch] = dailyPerformace
            self.PerformanceHolder[epoch].add_decision(decision)
    

    def GetLastDecision(self):
        return self.LastDecision

    def showDailyDecisions(self, bot_name, verbose=True):
        '''Output daily decision lists for trader.
        '''
        num_epochs = len(self.PerformanceHolder)
        
       
        text_out = ""
        for date, dp in self.PerformanceHolder.items():
            for decision in dp.Decisions:
                text_out += f'{decision.__str__()} \n'
                if verbose:
                    print (decision)
        return text_out

    def output_summary(self):
        return ("TotalPL: {0} # Trade: {1} # Up {2} # Down {3} \n".format(self.TotalPL, self.NumberTrades, self.NumberPositive, self.NumberNegative))

class EvaluateDecisions(object):
    '''Root class of evaluation. Fitness value only.

    Arguments:
        object {[type]} -- [description]


    '''
    def __init__(self, bot, botPerformance):
        self.fitnessValue = 0.0 
        self.decisionSummary = {}
        #agent in optimisation process and making decisions
        self.bot = bot
        #bot/agent performance which holds decision profiles made  -> discretised by day or anyother
        #discretising factor. Always need multiple dynamic process -> not required though. e.g. one day can work
        #but not good practice
        self.botPerformance = botPerformance
        #Fitness recorder of each Decision Profile


    def evaluateFitness(self):
        self.fitnessValue = 0.0


    def printDecisionSummary(self):
        print ("Must override in custom evaluation logic")

    def getTradeDecisionsForRecording(self):
        return None

class Performance(object):

    """
    Main Performance class. Record and store metrics for optimisation/simulation.

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self):
        """Initialise performance instance
        """
        
        import random
        self.performance_id = "performance" + str(random.randint(100,100000))
        from datetime import date
        curr_date = str(date.today())
        self.date_started = curr_date
        #this holds the botperformance->dailyperformance->decisionprofiles->decisions
        self.bots = {}
        #current state of bot
        self.decision_state = {}

        #evaluation of decisions...after all the decisions have been made, we must evaluate them
        #we must create the custom class for this run. e.g a trade evaluation class. All required metrics
        #are in root evaluation class.
        self.evaluation = {}
        
        self.number_winners = 0
        self.number_participants = 0
        


    def parallelJoinPerformances(self, performances = []):
        num_perf = 0
        for perf in performances:
            num_perf +=1
            print (f'bot num:{len(perf.bots)}')
            self.bots.update(perf.bots)

        print (f"Joined performances: {len(self.bots)} bots : {num_perf} performances")
        
    def getLastBotDecision(self,botID):
        return self.bots[botID].getLastBotDecision()

    def showBotDecisions(self, bot_name = None, verbose = True):
        if bot_name == None:
            for bot, botperformance in self.bots.items():
                botperformance.showDailyDecisions(bot)
        else:
            if bot_name in self.bots:
                performance = self.bots[bot_name]
                text = performance.showDailyDecisions(bot_name, verbose=verbose)
                return (text)
            return ""
        

    def add_trader(self, bot=None):
        """Add a trader to the performance tracker

        Keyword Arguments:
            bot {trader} -- New trader to add (default: {None})
        """
        if bot != None:
            botID = bot.Name
            botPerformance = BotPerformance()
            self.bots[botID] = botPerformance

    def UpdateDecisions(self):
        """Update against, for eg, decision contraints
        """

        pass

    def dna_transcribed(self, data):
        """
        DNA has been transcribed. This tells us whether the bot is 
        looking to open  or close a decision.

        Arguments:
            data {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        i_d = data['victim']
        if TRANSCRIPTION_DEBUG:
            print ("looking for decision status")
            print ("Victim ID: {0}".format(i_d))
        if i_d in self.decision_state:
            if TRANSCRIPTION_DEBUG:
                print ("looking for decision status")
                print ("Victim ID: {0} Found".format(i_d))
            decision_status = self.decision_state[i_d]
            if decision_status == 0:
                #currently idle
                return 0
            else:
                #in decision territory!
                return 1
        if TRANSCRIPTION_DEBUG:
            print ("Cant find ID in decision tracker. Must be a first decision.")
            print ("Victim ID: {0}".format(i_d))
        #no decisions made yet so return status 0 and make a new decision.
        return 0

    def update_decision_status(self, decision, bot_id):
        if bot_id in self.decision_state:
            self.decision_state[bot_id] = decision.DecisionStatus
        else:
            self.decision_state[bot_id] = decision.DecisionStatus

    def add_decision(self, decision=None, epoch="", botID=""):
        """Add decision. This can be any decision derived from root

        Keyword Arguments:
            decision {[type]} -- [description] (default: {None})
            date {str} -- [description] (default: {""})
            botID {str} -- [description] (default: {""})
        """

        self.update_decision_status(decision, botID)

        if decision != None:

            if botID in self.bots:
                self.bots[botID].add_decision(decision, epoch)

            else:
                botPerformance = BotPerformance()
                self.bots[botID] = botPerformance
                self.bots[botID].add_decision(decision, epoch)
                

        if decision == None:
            print ("Critical Error :: Adding Decision.")
            exit()

    def evaluateBots(self, agents, args = {}):

        '''Evaluate all bots in game.

        Arguments:
            agents {[type]} -- [description]
        '''

        self.number_winners = 0
        self.number_participants = 0
        for name, agent in agents.items():
            # print (name)
            # has the agent made any decisions and in bot vector ( only those who have made decisions )
            if name in self.bots:
                
                evalClassName = args['evaluation_class_name']
                evalClass = eval(evalClassName)
                self.evaluation[name] = evalClass(agent, self.bots[name])
                self.evaluation[name].evaluateFitness()
                self.number_participants+=1
                if self.evaluation[name].fitnessValue > 0:
                    self.number_winners+=1
                
            else:
                evalClassName = args['evaluation_class_name']
                evalClass = eval(evalClassName)
                self.evaluation[name] = evalClass(agent, None)
                self.evaluation[name].evaluateFitness()
                
    
    def output_fitness_vector(self):
        fitness_vector = []
        for bot_name, eval in self.evaluation.items():
            fitness_vector.append(eval.fitnessValue)

        return fitness_vector
    
    def outputDecisionPerformanceSummary(self):
        '''
        Output to screen decision Summary -> decision data and associated fitness
        '''
        print ("ND: {}".format(len(self.evaluation)))
        for botName, evalAlg in self.evaluation.items():
            evalAlg.printDecisionSummary()

    def outputStructure(self, dataManager = None, gen = 0):
        '''Output structures
        '''

    def text_output_fitness(self):
        best_fitness = -999999
        fitness_struc = {}
        f_values = []
        worst_fitness = 0.0
        bot_id = ""
        
        for botName, evalAlg in self.evaluation.items():
            #print (botName)
            
            #logger.info('%s being recorded', botName)
            fitness_struc[botName] = evalAlg.fitnessValue
            # print (f'Bot: {botName} | fitness: {evalAlg.fitnessValue}')
            if best_fitness == None:
                if evalAlg.fitnessValue != 0 or evalAlg.fitnessValue != 0.0:
                    best_fitness = evalAlg.fitnessValue
                    
                    # print (best_fitness)
                    bot_id = botName
                else:
                    continue
                
            if worst_fitness == None:
                if evalAlg.fitnessValue != 0 or evalAlg.fitnessValue != 0.0:
                    worst_fitness = evalAlg.fitnessValue
                    # worst_fitness = min(worst_fitness,  evalAlg.fitnessValue)
                else:
                    continue
            
            if evalAlg.fitnessValue != 0 or evalAlg.fitnessValue != 0.0:
                
                if  evalAlg.fitnessValue > best_fitness:
                    bot_id = botName
                    best_fitness = evalAlg.fitnessValue
                
                worst_fitness = min(worst_fitness,  evalAlg.fitnessValue)
                f_values.append(evalAlg.fitnessValue)
                
            # if evalAlg.fitnessValue > best_fitness:
                
            
            
            
        return best_fitness, worst_fitness, bot_id, fitness_struc

    def outputAndRecordEvalResults(self, dataManager = None, gen = 0, population = None):
        '''Output evaluation results.
        Save best trader and output data to track optimisation via the data manager
        Genration tag required
        '''
        fitness_struc = {}
        
        for botName, evalAlg in self.evaluation.items():
            
            #logger.info('%s being recorded', botName)
            fitness_struc[botName] = evalAlg.fitnessValue
            
            try:
                dataManager.recordBotDecisions(generation = gen, content = evalAlg.decisionSummary, botName = botName)
            except:
                print ("an error occured recording decision.")
                #logger.critical('An error occured recording decision.')


            

            #try:
            #    dataManager.saveBotDecisions(generation = gen, content = evalAlg.decisionSummary, botName = botName)
            #except:
            #    print ("an error occured saving decision.")

            #success = False
            #while (success == False):
            '''
            print ("fitness: sending structures")
            try:
                #print (population)
                structure = population[botName].printStr()
                #print (structure)
                #print ("---")
                dataManager.recordBotStructures(generation = gen, content = structure, botName = botName)
                print ("--- str sent")
                
            except:
                print ("an error occured recording structure.")
                #create structure image & save
            '''

            
            '''
            OP_OUTPUT_FOLDER = os.path.join(os.path.expanduser('~'), 'tradingalgorithm','code','lucen' , 'output')

            directoryPATH = os.path.join(OP_OUTPUT_FOLDER, str(dataManager.optimsationID))

            imgSavePath = os.path.join(directoryPATH, "tracker", "gen" , str(gen), "")
            '''

            '''
            imgBuilder = StructureImage(structure=structure, botName = botName, outpath = imgSavePath)
            #print (botName#)
            #print (imgSavePath)


            #build and save image
            imgBuilder.BuildImage()

            try:
                #upload image
                dataManager.recordBotImage(generation=gen, botName = botName)
            except:
                print ("An error occured recording .")
            '''



        import json

        fitness_json = json.dumps(fitness_struc)

        if dataManager != None:

            #success = False
            #while (success == False):
            # try:
            #     dataManager.saveFitnessValues(generation = gen, content = fitness_json)
            # except:
            #     print ("an error occured saving fitness values")
            try:
                dataManager.recordFitnessValues(generation = gen, content = fitness_json)
                #success = True
            except:
                print ("an error occured recording fitness values")
                #logger.critical('An error occured recording fitness values')

    def SummarizeBotPerformance(self):
        for ind, data in self.bots.items():
            data.summarize()

    def output_bot_summary(self):
        for ind, data in self.bots.items():
            print(data.output_summary())

    def output_all_data(self):
        print (f'Number of bots:  {len(self.bots)}')
        for ind, value in self.bots.items():
            print (ind)
            #print (self.bots[ind])


   
if __name__ == "__main__":
    demo = Performance()
    print (demo.performance_id + " ; " + demo.date_started)
    '''
    d_result = TradeDecisionResult()
    d_result.define_result(2.5,"09:04","10:06")
    d_result_t = TradeDecisionResult()
    d_result_t.define_result(5,"09:04","10:06")

    demo.add_decision(d_result, date="09-09-09", botID="demoBot")
    demo.add_decision(d_result_t, date="09-10-09", botID="demoBot")

    d_result = TradeDecisionResult()
    d_result.define_result(12.5,"09:04","10:06")
    d_result_t = TradeDecisionResult()
    d_result_t.define_result(-4,"09:04","10:06")

    demo.add_decision(d_result, date="09-09-09", botID="demoBot2")
    demo.add_decision(d_result_t, date="09-10-09", botID="demoBot2")
    '''


    demo.output_all_data()
    demo.SummarizeBotPerformance()
    demo.output_bot_summary()


# import custom decision
# ---

from custom_decisions import *