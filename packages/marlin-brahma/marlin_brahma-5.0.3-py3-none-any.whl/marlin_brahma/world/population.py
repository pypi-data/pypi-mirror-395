"""Population class for evolutionary algorithms
"""
import json, requests
import logging
from tqdm import tqdm as tq
import os, sys, random, pkgutil, math
logging.basicConfig(level=logging.CRITICAL)
#insert root dir into system path for python
#config core
# sys.path.append('../')
# from configCore import *

#import root bot
from marlin_brahma.bots.bot_root import *

# import bots
from custom_bots import *
# from custom_genes import *

import os
from loguru import logger as logger_
# logger_.add('ident_learn.log', format="{level} : {time} : {message}: {process}", level="TRACE")
# # logger_.remove(0)
# logger_.add(sys.stdout, level="INFO")  
import pickle




class Population(object):
    """
    Population is the container object for all bots/indis in the game/optimisation run.
    
    Arguments:
        object {root object} -- object class
    """

    def __init__(self, parms=None, name="vx_dm", gene_args = None, version="1_0_0", dmdb_load = False):
       
        logger_.info("Initialising Population.")
        """
        Create the Population class. This class holds all bots in the game.

        :param parms: optimisation parameters - from config file but passed through for now, defaults to None
        :type parms: key/value pairs, optional
        :param name: name root, defaults to "vx_dm"
        :type name: str, optional
        """

        self.name = name + str(random.randint(10,10000))
        self.parms = parms
        self.feature_version = version
        #bot names in list
        self.bots = []
        #species structure tagged by name
        self.species = {}
        #logger

        #self.logger = GetBrahmaLogger("Population")
        self.gene_args = gene_args
        
        #DM database
        #11-25
        self.dmdb = {}
        self.geneticSelectionDict = {}
        self.dmdb_flag = False
        self.dmdb_load = dmdb_load
        
        
        self.species_name = "undef"
        
    def __exit__(self):
        del self.logger

    #edit march
    #kill bots not making decisions -> 0 fitness
    
    def KillDeadWood(self, tags = []):
        pop_size = len(self.bots)
        dead_size = len(tags)
        logger_.info(f'[ {pop_size} ] bots after generation run. [ {dead_size} ] about to be killed off.')
        
        number = len(tags)
        splice_number = math.floor(number/2)
        # for tag in tags[0:splice_number]:
        for tag in tags:
            if tag in self.species:
                del (self.species[tag])
                self.bots.remove(tag)
        
        pop_size = len(self.bots)
        logger_.info(f'[ {pop_size} ] bots left.')
    #edit march
    def Repopulate(self, species = "BotRoot", args = None):
        population_size = len(self.species)
        delta = self.parms['population_size'] - population_size
        
        args = {
                            'training_set_description' : self.parms['training_set_description'], 
                            'study_focus' : self.parms['study_focus'], 
                            'parent' : "Eve"
                            }
        
        
        for i in range(delta):
            self.CreateBot(species = species, args = args) 
            
        for i in range(2):
            self.CreateBot(species = species, args = args) 
           
        # if dmdb_load == False:
        #     self.save_dmdb()
    

    
    def Populate(self, species = "BotRoot", args = None, dmdb = False):
        
        self.species_name = species
        if dmdb:
            self.dmdb_flag = True
            self.BuildDMDB()
        # logging.debug('Building inside brahma pop ')
        if globals().get("AcousticBot") is not None:
            logger_.info("We have bot creation dust! ")
            
        
        if args == None:
            try:
                args = {
                            'training_set_description' : self.parms['training_set_description'], 
                            'study_focus' : self.parms['study_focus'], 
                            'parent' : "Eve"
                            }
            except:
                logger_.error("Error setting bot args in populution build.")
       
        import pickle
        import os
        
        # if args == None:
        # print ("new bots")
        if species != "tribal":
            # if DEBUG:
            #     print ("Size: " + str(self.parms['population_size']))
            # print ("Size: " + str(self.parms['population_size']))
            population_size = self.parms['population_size']
            # print (self.gene_args)
            logger_.info("Building population.")
            for i in tq(range(0, int(self.parms['population_size']))):
                
                # logger_.info(f'building {i} of {population_size}')
                self.CreateBot(species = species, args = args)   
                # logger.debug(f'built {i} of {population_size}')
                
                #dmdb approach -> randomly select x number from dmdb
            
            logger_.info("Population built.")
            
        else:

            self.CreateBot(species = species, args = args)

        
            
        if args=="Living":
            
            BOT_SAVE_FOLDER = os.path.join(os.path.expanduser('~'), 'dev', 'app', 'tutorial-make-decisions', 'saved', '')
            # load all traders in bin folder
            listOfFiles = os.listdir(BOT_SAVE_FOLDER)
            
            for i in range(0, int(self.parms['population_size'])):
                
                #load saved bots
                filename = random.choice(listOfFiles)
                
                #pop from list
                indx = listOfFiles.index(filename)
                listOfFiles.pop(indx)
                
                try:
                    print (BOT_SAVE_FOLDER + filename)
                    pkl_binary = open(BOT_SAVE_FOLDER + filename , 'rb')
                   
                except:
                    print ("warning, bot not found")
                    exit()
                    continue
            
                try:
                    _bot = pickle.load(pkl_binary)
                    self.ResetTrader(_bot)
                    self.bots.append(_bot.name)
                    self.species[_bot.name] = _bot
                except Exception as e:
                    print (e)
                    
                
                # print (_bot.name)
                # print (_bot)
                
        
       
                    
    def ResetTrader(self,  trader):
        for dnaTag, dna in trader.dNA.items():
            dna.expressionTable = {}
            

    def test(self):
        pass

    
    # ----- NEW FRAMEWORK FOR OPTIMISATION ------
    def save_dmdb(self):
        with open('dm/saved_dmdb.dm', 'wb') as fp:
            pickle.dump(self.dmdb,fp)

    def BuildDMDB(self, args=None):
        
        if self.dmdb_load:
            with open('dm/saved_dmdb.dm', 'rb') as fp:
                self.dmdb = pickle.load(fp)
                
                
            
            return (1)
        
        population_size = self.parms['dmdb_size']
        logger_.info("Building [DMDB].")
        for i in tq(range(0, int(self.parms['dmdb_size']))):
                
            # logger_.debug(f'building {i} of {population_size}')
            self.CreateDMDBInd(args = args)   
            logger_.debug(f'built {i} of {population_size}')
    
        return (1)
    
    def CreateDMDBInd(self, args=None):
        
        #self.logger.info("Building Normal Genome - Gene count: {0}".format(self.genomeSize))
        self.BuildGeneSelectionDict()
        logger_.debug(self.BuildGeneSelectionDict)
        counter = {}
        #select
        valid_gene = False
        while not valid_gene:
            geneType = self.SelectGeneFromSelectionDict()
            logger_.debug(geneType)
            # print (self.gene_args)
            # print (geneType)
            if geneType in counter:
                if counter[geneType] < self.gene_args[geneType]:
                    valid_gene = True
                    counter[geneType] += 1
            else:
                if self.gene_args[geneType] != 0:
                    counter[geneType] = 1
                    valid_gene = True
                
            
            
            logger_.debug("Normal gene selected: {0}".format(geneType))

            
            geneStructureTmp = self.BuildGeneStructure(geneType,  self.geneticSelectionDict, gene_args=self.gene_args)
            geneStructureTmp.i_D = f'{geneStructureTmp.i_D}_dmdb'
            self.dmdb[geneStructureTmp.i_D] = geneStructureTmp
            #kill tmp structure
            geneStructureTmp = None
            

        return
 
    def BuildGeneSelectionDict(self):
        """Build gene type selection lists
        """


        import os
        #local genes loaded {todo: custom genes}
        #geneFileList = os.listdir(BRAHMA_GENETIC_DATA_FOLDER_LCL)
        #edit
        
        genetic_material_folder  = os.getenv('GENETIC_DATA_FOLDER_USR')
        logger_.debug(f'{genetic_material_folder}')
        geneFileList = os.listdir(genetic_material_folder)
        logger_.debug(f'{geneFileList}')
        for fileName in geneFileList:
            
            if fileName.endswith('.py'):
                
                fnArray = fileName.split('.')
                geneType = fnArray[0]
                if geneType != "dnaroot":
                    
                    prefix = geneType.split('_')
                    prefixStr = prefix[0]
                    
                    if prefixStr == "g":
                        geneName = prefix[1]
                        
                        logger_.debug("Adding Gene to Selection: {0}".format(geneName))
                        self.geneticSelectionDict[geneName] = eval(f'{geneName}')
            
    def SelectGeneFromSelectionDict(self):
        """Select a genetype from the list
        and return to caller
        """
        import random
        try:
            #self.logger.debug("Trying to grab a random gene tag.")
            
            randomGeneTag = random.choice(list(self.geneticSelectionDict))
            #self.logger.debug("Random gene tag: {0}".format(randomGeneTag))
            
            return randomGeneTag

        except Exception as e:
            
            #self.logger.critical("Error selecting gene")
            exit(-1)
        return -1
 
    def BuildGeneStructure(self, gene_type = "", classCollection=None, gene_args = {}):
        if gene_type != "":
            pass
        else:
            #self.logger.critical("No genetic material found for gene_type: {0}".format(gene_type))
            exit("No genetic material")

        logger_.debug(f"Building gene : {gene_type}")
        
        logger_.debug(f"Building gene : {classCollection}")
        
        tmpGene = None
        #self.logger.debug("attempting to create gene from new selection approach: {0}".format(gene_type))
        try:
            #print (gene_type)
            #print (self.geneticSelectionDict)
            #tmpGene = self.geneticSelectionDict[gene_type]("test")
            #'test' being passed as env changed  feb '21
            # print ("***")
            # print (classCollection)
            
            tmpGene = classCollection[gene_type](self.parms['env'], gene_args=gene_args)
            # print ("---")
            # print (f'temp : {tmpGene}')
        except Exception as e:
            #self.logger.critical("Attempting to create gene from new selection approach: FAIL")
            logger_.error(e)
            exit(0)

        return tmpGene

    def ShowDMDB(self):
        print (self.dmdb)
        for dm_id, dm in self.dmdb.items():
            desc = dm.__str__() 
            logger_.info(f'{dm_id} : {desc}')
    

    # ----- NEW FRAMEWORK FOR OPTIMISATION ------

    def CreateBot(self, species = None, args = None):
        
        self.botStr = {}
        self.botStr[species] = eval(species)
        
        logger_.trace(f'creating bot')
        #build the bot here - general
        
        bot_tmp = self.botStr[species](self.parms["env"], myspecies = species, myargs = args, version=self.feature_version)
        
        bot_tmp.BuildBot(parms=self.parms, gene_args = self.gene_args, dmdb_flag = self.dmdb_flag, dmdb_ids = list(self.dmdb.keys()))
        
        # bot_tmp.printAll()
        self.bots.append(bot_tmp.name)
        self.species[bot_tmp.name] = bot_tmp
        
       

    def Show(self):
        
        for key, value in self.species.items():
            # print (value)
            value.printAll()

            
    def save_bots(self):
        for bot_id, bot in self.species.items():
            
            #serialise bot to local file.
            print (f'saving ... {bot_id}')
            bot.save()
            # self.recordWinningBot(bot)
            
    
    def DMDB_saveBots(self,bot_list = [], data={}):
        """DMDB_saveBots    Save list of bots. We need to build a structure which can be used live. We need to swap the string ID of a gene (DM)
        for a real gene structure that can be used live. This is done by iterating over the genome in a DNA strand and swapping a DM ID with a DM strucure.
        The structure is taken from the DMDB structure.

        :param bot_list: _description_, defaults to []
        :type bot_list: list, optional
        """
        
        new_names = []
        
        suffix = ""
        if 'generation' in data:
            suffix = data['generation']
            
        
        # iterate over bot ids
        for bot_id in bot_list:
            # create a deep copy of the active bot
            logger_.info(f'Saving {bot_id}')
            bot_tmp = copy.deepcopy(self.species[bot_id])
            bot_tmp.name = self.species[bot_id].name + "_" + str(suffix)
            # get active DNA & genome id tag
            dNA_tag = list(bot_tmp.dNA.keys())[0]
            genome_tag = list(bot_tmp.dNA[dNA_tag].genome.keys())[0]
            
            # get list of genes in genome
            _genome_ = bot_tmp.dNA[dNA_tag].genome[genome_tag].genome
            
            # iterate over genome and swap gene id for structure
            _new_genome = {}
            for g_tag, dm_id in _genome_.items():
                dm_str = self.dmdb[dm_id]
                _new_genome[g_tag] = dm_str
            
            bot_tmp.dNA[dNA_tag].genome[genome_tag].genome = _new_genome
            # bot_tmp.printAll()
            bot_tmp.Save(save_folder = data['bot_path'])
            new_names.append(bot_tmp.name)
            
            
        return new_names
    

    
    def recordWinningBot(self, bot):
        """Record optimisation winners to db

        Arguments:
            botlist {[type]} -- [description]
        """
        #logger.info('Winning bots recorded')
        botStr = bot
        botID = bot.name
        #--build data for posting
        dataSend = {}
        dataSend["action"] = "record_bot"
        dataSend["user"] = self.parms['uid']
        dataSend["botID"] = botID
        dataSend["botStructure"] = botStr.printStr()
        dataSend["market"] = self.parms['env']
        dataSend["direction"] = ""
        dataSend["optimisationID"] = ""
        dataSend["parent"] = "Eve"
        dataSend["scope"] = "global"
       
        
        dataSendJSON = json.dumps(dataSend)
      
        #--post data
        try:
            API_ENDPOINT = "https://www.vixencapital.com/api/optimisation/"
            try:
                r = requests.post(url = API_ENDPOINT, data = dataSendJSON)
                response = r.text
            except:
                print("request error")

        except:
            #logger.critical('Error recording winning bot')
            pass


        #print (response)
    


if __name__ == "__main__":
    pass
    '''
    pop = Population(parms={'PopulationSize' : '100'}, name = "demo")
    pop.populate('trader')
    '''

