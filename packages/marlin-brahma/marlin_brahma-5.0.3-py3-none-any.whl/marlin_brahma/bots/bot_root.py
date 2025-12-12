"""This is v1.0 of the trader template. Procedures for birth, death evolution must be contained here.
This is a template for a general intraday futures/fx trader.
"""

#v2.0 
import os, sys, time, copy, datetime, random

#config core
# sys.path.append('../')
# from configCore import *

# sys.path.append('../dna')
# current
import logging
# importing
from marlin_brahma.dna.vixen_dna import *
from marlin_brahma.transcription.transcription import * 
from custom_transcription import *
class BotRoot(object):
    
    """BotRoot is the root class of all indis/bots in the brahma world.
    Genetic material is deterined by lcl folder for material and derived bots  can add
    functionality. e.g.  trader  - direction of bot.

    todo: visualise bot genetic strucure

    :param object: [description]
    :type object: [type]
    :param object: [description]
    :type object: [type]
    :param object: [description]
    :type object: [type]

    """
    
    def __init__(self, myenv="", myspecies = "BotRoot", myargs=None, version="1_0_0"):
        self.direction = 0
        self.env = myenv
        self.dob = datetime.datetime.now()
        self.species = myspecies
        self.custom = False #introduced for custom traders built elsewhere
        self.name = "vixen_bot" + str(random.randint(0,1000000))  + str(random.randint(0,1000000)) 
        self.version = version
        self.regulatory_network = None
        self.args = myargs
        
        # descriptions 
        training_data_desc = "none provided"
        study_focus = "none provided"
        
        if myargs != None:
            training_data_desc = myargs['training_set_description']
            study_focus = myargs['study_focus']
             
        self.training_data_desc = training_data_desc
        self.study_focus = study_focus
        
        
        # print (self.training_data_desc)
        # print ( self.study_focus)
        #genetic material
        if myargs == None:
            
            self.parent = "Eve"
        else:
            if 'parent' in myargs:
                self.parent = myargs['parent']
            if 'custom' in myargs:
                self.custom = myargs['custom']
            if 'name' in myargs:
                self.name = myargs['name']
        
        self.dNA = {}                   #contains strands of DNA
        #self.riskDNA = {}
        self.numberDNA = 0
        self.dNAExpression = {}         #expression value of each DNA strand 
                                        #this is required for transcription

        #self.dNARiskExpression = {}    #expression value of each risk DNA strand 
                                        #this is required for transcription

        #protein transcription
        self.transcriptionDNA = None    #this is what is used for transcription
                                        #DNA expression levels is required

        #initialised
        self.initialised = False

        #logger
        #self.logger = GetBrahmaLogger("Bot Creation")
        

    def __str__(self):
        """
        Overide of print method.Export high level description of bot. 

        :return: High  level description of bot.
        :rtype: String
        """
        risk_tag = "No Risk DNA"
        num_risk = 0
        for tag, dna in self.dNA.items(): 
            if dna.dnaType == "risk":
                risk_tag = dna.name
                num_risk += 1
                
        
        if not hasattr(self, 'version'):
            self.version = "1_0_0"
        
        return ("Name: [{0}] Version [{7}] Custom: [{6}] Number DNA: [{1}] Env: [{2}] Species: [{3}] Risk Tag: [{4}] Risk DNA[{5}]".format(self.name, self.numberDNA, self.env, self.species, risk_tag, num_risk, self.custom, self.version))

    def BuildBot(self, parms = None, gene_args = None, dmdb_flag = False, dmdb_ids = []):
        """
        Build the bot and all its genetic material. This is the root class 
        so all root genetic material is built. 

        :param parms: [description], defaults to None
        :type parms: [type], optional
        """
        
        #determine numer of dna strands
        if parms != None:
            self.numberDNA = random.randint(parms['min_number_dna'], parms['max_number_dna'])
            logging.debug(f'built dna number')
        else:
            #Build generic bot.
            exit(0)

        
        # -- we are using a dmdb approach
        if dmdb_flag:
            logger_.trace("Building DBDB Bot")
            
            for i in range(0,self.numberDNA):
                dna_length = random.randint(parms['min_number_genes'], parms['max_number_genes'])
                #get delay
                dna_delay = random.randint(0, parms['max_dna_data_delay'])
                botDNA = VixenDNA(dataLength=dna_length, envName=self.env, dataDelay=dna_delay, gene_args = gene_args)
                botDNA_tag = botDNA.name
                botDNA.AddGenome(parms=parms,dmdb_flag = dmdb_flag, dmdb_ids=dmdb_ids)
                self.dNA[botDNA_tag] = botDNA
                botDNA = None
                self.dNAExpression[botDNA_tag] = 0.0
                
            #build transcription DNA
            self.transcriptionDNA = Transcription()
            
            
            return 1
       
        
        
        #--------------------------- Initial MyTradeBot
        
        #number of marketDNA
        for i in range(0,self.numberDNA):
           #print (self.numberDNA)
            
            #build market dna

            #get deltaT
            #dna_deltaT = random.randint(1, parms['maxDeltaT'])
            #dna_deltaT = random.choice(EpochBuckets)
            
            #get length
            dna_length = random.randint(parms['min_number_genes'], parms['max_number_genes'])
            #get delay
            dna_delay = random.randint(0, parms['max_dna_data_delay'])
            
            # brahma note: group data on fly
            logging.debug(f'dna adding dna structure')
            botDNA = VixenDNA(dataLength=dna_length, envName=self.env, dataDelay=dna_delay, gene_args = gene_args)
            botDNA_tag = botDNA.name
           
            #add genome... only one per DNA strand - yes for now
            logging.debug(f'dna adding genome')
            botDNA.AddGenome(parms=parms)
            
            
            
            self.dNA[botDNA_tag] = botDNA
            
            # del(marketDNA)
            botDNA = None
            self.dNAExpression[botDNA_tag] = 0.0
            #print (self.MarketDNA[marketDNA_tag].ExpressionTable)
            # exit()

            logging.debug(f'built genome')
        
        

        #build transcription DNA
        self.transcriptionDNA = Transcription()
        return 1
         
    def BuildChild(self, parent = None):
        species = parent.species

    def Reset(self):
        for dnaTag, dna in self.dNA.items():
            dna.Reset()
            
    def GetMemory(self):
        max_memory = -1
        for dnaTag, dna in self.dNA.items():
            max_memory = max(max_memory, dna.GetMemory())
            # print (f'b {max_memory}')
            
        # print (f'bot {max_memory} ')    
        return max_memory

    def StartUp(self):
        """
        All expression levels must be set to zero before starting a new run.
        """

        for dnaTag, e in self.dNAExpression.items():
            self.dNAExpression[dnaTag] = 0.0

        #for dnaTag, e in self.dNARiskExpression.items():
        #    self.dNARiskExpression[dnaTag] = 0.0
    
    def ForceTranscribe(self):
        for dnaTag, expression in self.dNAExpression.items():
            self.dNAExpression[dnaTag] = 1
    
   

    def ExpressDNA(self, data={}, dmdb_flag = False):
        """
        ---Populate dNAExpression---
        Express each strand of DNA in the bot and build the DNA epression table for
        the bot. Return values are 1 for bot is now initialised and 0 for not initialised.

        :param data: Pressure data, defaults to {} for root as no data required 
                    for test data. User defined for derived bot data requirements
        :type data: dict, optional
        :return: Initialised state of bot. True: is initialised False: not initialised 
        :rtype: Bool
        """

        #run risk first - obsolete
        '''
        for dnaTag, dna in self.riskDNA.items():
            expression_value = dna.ExpressDNA(data=data)
            #check to see if all the genetic material has been initialised
            #a value of False means that one of the genomes has not been initialised
            #so ExpressDNA also returns false after settng the initialised value to  False
            if expression_value == False:
                self.initialised = False
                return  False
            self.dNARiskExpression[dnaTag] = expression_value
        '''
        
        #added feb 21. Reset expression between iterations
        #self.dNAExpression  = {}
        #--use StartUp instead

        #print (self.initialised)
        #print (self.dNA)
        #print (self.dNAExpression)
        
        
        for dnaTag, dna in self.dNA.items():
            # print (f'dna: {dnaTag}')
           
            
            pressure_data = data
            
            expression_value = dna.ExpressDNA(data=pressure_data, dmdb_flag=dmdb_flag)
            
            if dna.dnaType == "risk":
                if expression_value == 1:
                    #transcribe protein
                    self.ForceTranscribe()
                    return True
            
            
            #print  (f'******* {expression_value}')

            #debug ---> gene flip analysis
            #print  (expression_value)
            #check to see if all the genetic material has been initialised
            #a value of False means that one of the genomes has not been initialised
            #so ExpressDNA also returns false after settng the initialised value to  False


            #update nov 2020 :  returning boolean and floating point
            if expression_value == -10:
                self.initialised = False
                if dnaTag in self.dNAExpression:
                    self.dNAExpression[dnaTag] = 0.0
                else:
                    self.dNAExpression[dnaTag] = 0.0
                    print (self.dNAExpression)
                    print (dnaTag)
                    print ("Key error location 2. bot_root")
                    
                #feb 2021 
                return  False

            #each DNA strand in bot now has valie
            self.dNAExpression[dnaTag] = expression_value


        #we have expressed all DNA strands which means all genomes inside have been run
        #which means that the individual is now intialised.
        self.initialised = True

        #---debug output
        #tickExpress = []
        #for key, val in self.dNAExpression.items():
        #    #print (val)
        #    fp = open ("express.txt", "a")
        #    fp.write("{0}\n".format(val))
        #    fp.close()
        #    tickExpress.append(val)
        #print (self.initialised)
        #print (*tickExpress)
        
        #print ("***")
        #---

        return True

    def GetExpressionData(self, type=""):
        return self.dNAExpression
       
    def GetAvgExpressionValue(self):
        total_expression = 0.0
        num_dna = 0
        avg_expression = 0.0
        for k,v in self.dNAExpression.items():
            total_expression = total_expression + v
            num_dna+=1
            
        if num_dna > 0:
            avg_expression = total_expression/num_dna
        return avg_expression
            
    
    #get expression data for each chromosome / DNA for transcription -> one value per (MARKET)DNA STRAND
    def get_chromosome_expression_structure(self):
        data = {}

        for tagID, dna in self.dNA.items():

            if EXPRESS_DEBUG:
                dna.print_expression_table()

            sum_express = 0
            num_genome = 0
            num_genome = len(dna.genome)
            #print ("num gen ", num_genome)
            #print (marketDNA.ExpressionTable)
            for genomeID, genome in dna.genome.items():


                if genomeID in dna.expressionTable:
                    sum_express = sum_express + dna.expressionTable[genomeID]
                    if GENOME_DEBUG == True:
                        print ("Genome Expression Vector")
                        print (dna.expressionTable[genomeID])

                else:
                    if TRANSCRIPTION_DEBUG:
                        print ("Can't find genome expression for transcription data! Expression Tabe for chromosome: \n")
                        print (dna.expressionTable)

            chromo_express = sum_express/num_genome
            data[tagID]=chromo_express

            if TRANSCRIPTION_DEBUG:
                print ("Num Genome in Chromosome: " + str(num_genome))
                print ("Sum Express for DNA: {0}".format(sum_express))
                print ("Actual Express for DNA: {0}".format( chromo_express))





        return data

    def printMood(self):
        pass

    def printStr(self):
        import json
        """Expression and decision making output. Not just expression levels. Trader level debug.
        Get a feel for the mood.
        """
        #print ("root bot print STr")
        #build the bot structure:
        bot_structure = {}
        bot_structure['name'] = self.name
        bot_structure['chromosomeNumber'] = self.numberDNA
        #bot_structure['direction'] = self.direction
        bot_structure['env'] = self.env
        bot_structure['parnet'] = self.parent
        bot_structure['creation_args'] = self.args
        bot_structure['study_focus'] = self.study_focus
        bot_structure['training_data'] = self.training_data_desc
        if hasattr(self, 'version'):
            bot_structure['version'] = self.version
        else:
            bot_structure['version'] = '1_0_0'
            
        chromosomes = {}
        for dnaTag, chromosome in self.dNA.items():
            chromosomes[dnaTag] = chromosome.GetStructureData()

       
        bot_structure['genetics'] = chromosomes

        

        #export
        '''
        file_str = open(BOT_DATA_FOLDER + self.name + ".json", "w")
        json.dump(bot_structure, file_str)
        file_str.close()

        if CHILD_DEBUG:
            print (bot_structure)

        if STRUCTURE_OUTPUT == True:
            
            for dnaTag, chromosome in self.dNA.items():
                print (chromosome)
                for genomeID, genome in chromosome.genome.items():
                    print (genome)

       


        if MOOD_OUTPUT == True:

            for dnaTag, chromosome in self.dNA.items():
                print (chromosome)
                """
                if hasattr(self, 'MarketDNAExpression'):
                    print ("Excitement: {0}".format(self.MarketDNAExpression[dnaTag]))
                else:
                    chromosome.print_expression_table()"""
        '''
        return (bot_structure)

    def printAll(self):
        """
        Print all ind genetic data
        """
        
        for key, dna_strand in self.dNA.items():
            print (dna_strand.__str__())
            for key, gene in dna_strand.genome.items():
                print (gene)
            
    
    
        
    
    """
    Evolutionary procedures. These can be overritten, but these are provided 
    by BrahmA in the root bot class.
    """
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

        patient.NumberMarketDNA+=1
        newDNA = copy.deepcopy(dna)
        newDNATag = random.randint(100,100000)
        newDNA.Name = newDNATag

        patient.marketDNA[newDNATag] = newDNA
        if DEBUG:
            print (patient.marketDNA[newDNATag])


        return patient

    @staticmethod
    def removeDNAStrand(patient):

        if len(patient.marketDNA > 1):
             #get key from dnaStrands and del from bot
            randomKey = random.choice(list(patient.marketDNA.keys()))
            del patient.marketDNA[randomKey]
        
        return patient
        
    """
    """
    Mutate individual
    """
    def Save(self, save_folder = ""):
        import pickle
        fileName = ""
        fileName_str = ""
        if save_folder == "":
            fileName = 'bots/' + self.name + '.vixen'
            fileName_str = 'bot_str/' + self.name + '.json'
            
        else:
            fileName = f'{save_folder}/{self.name}.vixen'
            fileName_str = f'{save_folder}/bot_str/{self.name}_str.json'
        # if folder == "":
        #     fileName = BOT_SAVE_FOLDER + self.name + '.bot'
        print (f'Saving .... {fileName} Next Gen.')
        saveFile = open(fileName, 'wb')
        pickle.dump(self, saveFile)
        saveFile.close()

        bot_str = self.printStr()
        
        with open(fileName_str, 'w') as fp:
            json.dump(bot_str, fp)

        return (1)

    def Mutate(self, args = {}, dmdb_flag = False, dmdb = {}):
        
        
        if dmdb_flag:
            for dnaTag, dna in self.dNA.items():
                for genomeID, genome in dna.genome.items():
                    genome.DMDB_Mutate(dmdb, args)
            
            
            
            return 1
        
        # iterate over dna and mutate 
        for dnaTag, dna in self.dNA.items():
            for genomeID, genome in dna.genome.items():
                for geneTag, gene in genome.genome.items():
                    gene.mutate(args)

    
"""

class myTradeBot(BotRoot):
    def __init__(self, myenv="", myspecies = "myTradeBot", myargs=None):
        super().__init__(myenv=myenv, myspecies = myspecies, myargs=myargs)

        #looking for a buyer here
        self.direction = 1

        def Mutate(self):
            print ("Mutate bot...")


"""
