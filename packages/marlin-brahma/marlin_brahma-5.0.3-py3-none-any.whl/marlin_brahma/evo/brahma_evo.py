"""

BrahmA Evolution Module
=======================================
written by Rahul Tandon c/o Vixen Intelligence

"""

import os, sys, time, random, copy


#--config core import--
# sys.path.append('../')
# from configCore import *

#import root bot
from marlin_brahma.bots.bot_root import *

# import bots
from custom_bots import *

# logging
from loguru import logger as logger_


import itertools
#-----------------------------MATE-----------------------------------------------


class Mate(object):
  '''
  Class to mate individuals. Static and class routines provided to mate bots. This is 
  the default version.

  Procedure:
  1. Create a child bot
  2. Combine parent DNA
  3. Add randomly chosen tradnscription DNA from parents.
  3. Return child

  '''

  def __init__(self):
    pass

  @staticmethod
  def DMDB_Mate(maleBot, femaleBot):

    
    logger_.trace(maleBot)
    logger_.trace(femaleBot)
    
    
 
    
    active_species = maleBot.species
    active_env = femaleBot.env
    direction = femaleBot.direction
    child_args = {'direction' : direction, 'parent' : femaleBot.name, 'training_set_description': femaleBot.training_data_desc, 'study_focus' : femaleBot.study_focus}
    
    botStr = eval(active_species)
    childBot = botStr(active_env, myspecies = active_species, myargs = child_args)
    
    mom_tmp = copy.deepcopy(femaleBot)
    dad_tmp = copy.deepcopy(maleBot)

    #determine number of dna strands
    import math
    numberMaleDNA = math.floor(maleBot.numberDNA)
    numberMaleDNA = max(1, numberMaleDNA)
    numberFemaleDNA = math.floor(femaleBot.numberDNA)
    numberFemaleDNA = max(1, numberFemaleDNA)

    #determine which DNA strands

    #forward or reverse

    #addDNAStrand(self, dna):
    for i in range(numberMaleDNA):
        # print (f'number genes: {len(dad_tmp.dNA)}')
        # Dad contribution
        if len(dad_tmp.dNA) < 1:
          continue
        dnaTag = random.choice(list(dad_tmp.dNA.keys()))
        number_dna = len(list(dad_tmp.dNA.keys()))
        logger_.trace(f'DNA Size [1] is [ {number_dna} ]')
        Mate.DMDB_addDNAStrand(dad_tmp.dNA[dnaTag], childBot)
        
        del dad_tmp.dNA[dnaTag]


    for i in range(numberFemaleDNA):
        # print (f'number genes: {len(dad_tmp.dNA)}')
        # Dad contribution
        number_dna = len(list(mom_tmp.dNA.keys()))
        logger_.trace(f'DNA Size [1] is [ {number_dna} ]')
        if len(mom_tmp.dNA) < 1:
          continue
        dnaTag = random.choice(list(mom_tmp.dNA.keys()))
        Mate.DMDB_addDNAStrand(mom_tmp.dNA[dnaTag], childBot)
        
        del mom_tmp.dNA[dnaTag]


    #forward or reverse
    
    # for i in range(numberFemaleDNA):
    #     print (f'number genes: {len(mom_tmp.dNA)}')
    #     if len(mom_tmp.dNA) < 1:
    #       continue
    #     dnaTag = random.choice(list(mom_tmp.dNA.keys()))
    #     Mate.addDNAStrand(mom_tmp.dNA[dnaTag], childBot)
    #     del mom_tmp.dNA[dnaTag]

    #transcription DNA
    Mate.addTranscription(random.choice([femaleBot.transcriptionDNA,maleBot.transcriptionDNA]),  childBot)

    
   
    
    del mom_tmp
    del dad_tmp

    
    logger_.trace(childBot)
    
    
    #return child
    return childBot


  @staticmethod
  def Mate(maleBot, femaleBot):

    
    active_species = maleBot.species
    active_env = femaleBot.env
    direction = femaleBot.direction
    child_args = {'direction' : direction, 'parent' : femaleBot.name, 'training_set_description': femaleBot.training_data_desc, 'study_focus' : femaleBot.study_focus}
    
    botStr = eval(active_species)
    childBot = botStr(active_env, myspecies = active_species, myargs = child_args)
    
    mom_tmp = copy.deepcopy(femaleBot)
    dad_tmp = copy.deepcopy(maleBot)

    #determine number of dna strands
    import math
    numberMaleDNA = math.floor(maleBot.numberDNA)
    numberMaleDNA = max(1, numberMaleDNA)
    numberFemaleDNA = math.floor(femaleBot.numberDNA)
    numberFemaleDNA = max(1, numberFemaleDNA)

    #determine which DNA strands

    #forward or reverse

    #addDNAStrand(self, dna):
    for i in range(numberMaleDNA):
        # print (f'number genes: {len(dad_tmp.dNA)}')
        if len(dad_tmp.dNA) < 1:
          continue
        dnaTag = random.choice(list(dad_tmp.dNA.keys()))
        Mate.addDNAStrand(dad_tmp.dNA[dnaTag], childBot)
        del dad_tmp.dNA[dnaTag]

    #forward or reverse
    
    # for i in range(numberFemaleDNA):
    #     print (f'number genes: {len(mom_tmp.dNA)}')
    #     if len(mom_tmp.dNA) < 1:
    #       continue
    #     dnaTag = random.choice(list(mom_tmp.dNA.keys()))
    #     Mate.addDNAStrand(mom_tmp.dNA[dnaTag], childBot)
    #     del mom_tmp.dNA[dnaTag]

    #transcription DNA
    Mate.addTranscription(random.choice([femaleBot.transcriptionDNA,maleBot.transcriptionDNA]),  childBot)

    
   
    
    del mom_tmp
    del dad_tmp

    #return child
    return childBot

  """
  Evolutionary procedures. These can be overritten, but these are provided 
  by BrahmA in the root bot class.
  """

  @staticmethod
  def addTranscription(transcription, patient):
    '''
    Add a transcription to a child bot  (or possibkly adult)

    Arguments:
        transcription {Transcription} -- Protein transcription algorithm.

    '''
    newTanscription = copy.deepcopy(transcription)
    patient.transcriptionDNA = newTanscription
    
    return patient

  @staticmethod
  def addDNAStrand(dna, patient):
    '''Copy DNAStrand to bot

    Arguments:
        dna {[VixenDNA]} -- DNAStrand
    '''

    patient.numberDNA+=1
    newDNA = copy.deepcopy(dna)
    newDNATag = random.randint(100,100000)
    newDNA.Name = newDNATag



    patient.dNA[newDNATag] = newDNA
    patient.dNAExpression[newDNATag] = 0.0
    

    return patient


  @staticmethod
  def DMDB_addDNAStrand(dna, patient):
    '''Copy DNAStrand to bot

    Arguments:
        dna {[VixenDNA]} -- DNAStrand
    '''

    patient.numberDNA+=1
    newDNA = copy.deepcopy(dna)
    newDNATag = random.randint(1,99999999)
    newDNA.Name = newDNATag

    # genome = newDNA.genome.genome
    active_genome_tag = list(newDNA.genome.keys())[0]
    number_genes = len(list(newDNA.genome[active_genome_tag].genome.keys()))
    logger_.trace(f"BEFORE splicing genome in DNA Slice: Gene number: [ {number_genes} ]")
    if number_genes > 1:
      number_splice = max(1,math.floor(number_genes/2))
      logger_.trace(f'Splice number : {number_splice}')
      _genome = dict(itertools.islice(newDNA.genome[active_genome_tag].genome.items(),number_splice))
      newDNA.genome[active_genome_tag].genome = _genome
      number_genes = len(list(newDNA.genome[active_genome_tag].genome.keys()))
      logger_.trace(f"AFTER splicing genome in DNA Slice: Gene number: [ {number_genes} ]")


    if len(list(patient.dNA.keys())) == 0:
      
      patient.dNA[newDNATag] = newDNA
      patient.dNAExpression[newDNATag] = 0.0
    
    else:
     
      active_dna_id = list(patient.dNA.keys())[0]
     
      running_genome_id = list(patient.dNA[active_dna_id].genome.keys())[0]
      patient.dNA[active_dna_id].genome[running_genome_id].genome = patient.dNA[active_dna_id].genome[running_genome_id].genome | newDNA.genome[active_genome_tag].genome
      
      
    
    

    return patient

  @staticmethod
  def removeDNAStrand(patient):

    if len(patient.dNA > 1):
          #get key from dnaStrands and del from bot
        randomKey = random.choice(list(patient.dNA.keys()))
        del patient.dNA[randomKey]
        del patient.dNAExpression[randomKey]
    
    return patient
    


#--------------------------TOURNAMENT--------------------------------------------


class RootTournament(object):
  def __init__(self, generationEval = None, population = None, dataManager = None):
    self.population = population
    #ranking by name
    self.rankings = []
    #evaluations
    self.evaluations = generationEval
    #optimisation data manager
    self.winners = []
    self.results = {}

    if (len(self.population.bots) < 4):
      print ("Critical Error! Need more bots. Exiting.")
      exit()

  def Rank(self):
    pass

  def Regenerate(self):
    pass
  
  def printRankings(self):
    for bid in self.rankings:
      fitnessValue = self.evaluations[bid].fitnessValue
      num_correct = self.evaluations[bid].number_correct
      number_incorrect = self.evaluations[bid].number_incorrect
      print (f'{bid} {fitnessValue} | [ {num_correct} ] / [ {number_incorrect} ] ')
      
    

class SimpleTournamentRegenerate(RootTournament):
  """
  A simple tournament (ranking algorithm) shipped with BrahmA for rapid develpment.s
  This class 

  :param RootTournament: [description]
  :type RootTournament: [type]
  """

  def __init__(self, generationEval = None, population = None, dataManager = None):
    super().__init__(generationEval = generationEval, population = population, dataManager = dataManager)
    if generationEval != None:
        #evaluations (EvaluateDecisions) by bot Tag
        #self.evaluations = generationEval
        #need the population data as this class will kill and create new population members
        #edited Nov 2020. Taken care in root
        #self.population = population
        #ranking by name
        #self.rankings = []
        pass

    else:
        print ("critical error initialising tournament.")
        exit()


  def Zeros(self):
    zeros = []

    for k, v in self.evaluations.items():
      if v.fitnessValue == 0.0 or v.fitnessValue == -1000:
        #we have no decisions, return
        zeros.append(k)

    number_zeros = len(zeros)
    # print (f'Number of dead wood: {number_zeros}')
    return zeros


  def RankPopulation(self, output = 0 ):

    import operator
    # print ("evaluations")
    # print (self.evaluations)
   
    rankedEvals = sorted(self.evaluations.items(), key=lambda x: x[1].fitnessValue, reverse=True)
    # print ("Ranked")
    #print (rankedEvals)
    #reset rankings
    
    self.rankings = []
    winners = []
    for key, value in rankedEvals:
        
        # print (f'val: {value.fitnessValue}')
        if value.fitnessValue != 0.0 or value.fitnessValue != 0:
          self.rankings.append(key)
          if (float(value.fitnessValue) > 0.0):
            self.winners.append(key)
            self.results[key] = float(value.fitnessValue)
          # print (f'{key} : {value.fitnessValue}')
          # print (f'added: {value.fitnessValue} ')
        #print (botID)
    # print (self.rankings)
    if len(self.rankings) < 5:
      self.rankings = []
      #n = len(self.rankings)
      for key, value in rankedEvals:
        #print (f'val: {value.fitnessValue}')
        self.rankings.append(key)
        #print (f'added: {value.fitnessValue} ')

    # print (self.rankings)
    number_participants = len(self.rankings)
    logger_.info(f'[ {number_participants} ] participants.')

    if output == -1:
      
      for botID, value in self.evaluations.items():
        winners.append(botID)
      
      return winners


    if output == 1:
        import random

        winners = []
        unique_names = []
        for botID, value in self.evaluations.items():
            if value.fitnessValue > 0:

                uniqueName = botID + "_" + str(random.randint(10,1000000))
                unique_names.append(uniqueName)
                winners.append(botID)

            #logger.info('Optimisation: %d', generation)

        return winners
        
  def RegeneratePopulation(self, dmdb_flag = False):

    #select 2 parents...

    #best bot structure 1
    maleParent = self.population.species[self.rankings[0]]
    # print (f'parent : {maleParent.name}')
    #best bot structure 2
    femaleParent = self.population.species[self.rankings[1]]
    # print (f'parent : {femaleParent.name}')



    #mom_tmp = copy.deepcopy(femaleParent)
    #dad_tmp = copy.deepcopy(maleParent)
    
    if dmdb_flag:
      childOne = Mate.DMDB_Mate(maleParent, femaleParent)
    else:
      childOne = Mate.Mate(maleParent, femaleParent)

    #best bot structure 3
    maleParent = self.population.species[self.rankings[2]]
    # print (f'parent : {maleParent.name}')
    
    #best bot structure 4
    femaleParent = self.population.species[self.rankings[3]]
    # print (f'parent : {femaleParent.name}')

    if dmdb_flag:
      childTwo = Mate.DMDB_Mate(maleParent, femaleParent)
    else: 
      childTwo = Mate.Mate(maleParent, femaleParent)




    #kill bottom 2
    populationSize = len(self.population.species)
    #edit rankings as ranking vevtor now not as long as population  as zero decision makers removed
    deathTagOne = self.rankings[len(self.rankings)-1]
    deathTagTwo = self.rankings[len(self.rankings)-2]

    del (self.population.species[deathTagOne])
    
    self.population.bots.remove(deathTagOne)
    del (self.population.species[deathTagTwo])
    
    self.population.bots.remove(deathTagTwo)

    #add children
    self.population.species[childOne.name] = childOne
    self.population.bots.append(childOne.name)
    self.population.species[childTwo.name] = childTwo
    self.population.bots.append(childTwo.name)


    mom_tmp = None
    dad_tmp = None

#-------------------------- GENETIC SHUFFLE -------------------------------

class RootMutate(object):
    

  """
  Root Mutate Class
  =============================
  Individual (gene) mutation is taken care of the root bot class. The mutation routine
  can of course be overridden. 
  """



  def __init__(self,  population = None, config = None):
    self.population = population
    #edit nov 2020 - read directly from optimisation parameters
    self.config = config


  def mutate(self, args = {}, dmdb_flag = False):
    '''
    Mutate according to mutation rate.
    '''
    
    for indTag, ind in self.population.species.items():
        chance = random.random()
        if chance < self.config['mutation_rate']:
            #print (f'Mutating...[{indTag}]')
            ind.transcriptionDNA.Mutate()


    
  
    for indTag, ind in self.population.species.items():
        chance = random.random()
        if chance < self.config['mutation_rate']:
            #print (f'Mutating...[{indTag}]')
            ind.Mutate(args=args, dmdb_flag=dmdb_flag, dmdb = self.population.dmdb)



#========================================================================
#                 Evolve                                                =
#========================================================================
class Evolve(object):
  """
  Main callable evolve class for BrahmA
  """
  def __init__(self):
    pass

#=======================================================================


#========================================================================
#                 Evolve Data                                               =
#========================================================================
class EvolveData(object):
  """
  Main callable evolve class for BrahmA
  """
  def __init__(self):
    pass

#=======================================================================