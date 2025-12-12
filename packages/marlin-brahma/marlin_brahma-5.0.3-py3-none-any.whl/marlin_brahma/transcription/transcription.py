"""Transcription genetic material/process is responsible for building the protein.
Here we model the action of decision making as the bot able to transcrible protein.
All the dna material in the bot is the genetic material required to regulate and transcribe
three different protein types:
1. An enzyme whose presence prescribes a 'ACTIVE' state
2. An enzyme whose presence prescribes a 'WAIT' state

This class/module is also considered 'genetic material', but it; sole responsibilty is to transcribe the already
exisiting genetic material. The genetic state of the gene(s) modelled here is/are always on (1/True).

gene state->genome->chromosome->expression vector-> [environmental regulation] -> transcription

[environmental regulation] will simply promote/suppress the expression vector rather than work on the transcrition
state

"""
import random, logging

logger = logging.getLogger("__main__")


#local import
import os, sys


# sys.path.append('../')
# from configCore import *



class DefaultTranscription(object):
    """This class models the genetic material required to transcribe the 'bot's' genetic material.
    It reads in chromosomal expression levels and decides whether

    Arguments:
        object {[type]} -- [description]


    """

    def __init__(self):

        self.transcription_state = None
        self.transcription_state_recorder = {}
        #self.transcription_threshold = random.random()
        #self.transcription_threshold = 0.002
        self.transcription_threshold = random.random()
        #v2. update - Apr 16
        #--update -> remove Nov 2020
        #self.transcription_threshold_exit = random.random()

    def __str__(self):
        return ("Activation Level: {0}".format(self.transcription_threshold))

    def get_structure(self):
        transcription_str = {}
        transcription_str['state'] = self.transcription_state
        #transcription_str['threshold'] = self.transcription_threshold_exit


    def transcribe(self, expression_data, activation_level = 0.7):
        """Transcribe DNA into protein

        Arguments:
            expression_data {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        # print (self.transcription_threshold)
        expression_str = expression_data['expression_data']
        #nt ("*********")
        
        expression_vec = []

        for chromTag, expression in expression_str.items():
            #print (expression)
            expression_vec.append(expression)


        protein_transcribe = self.map_expression_vector(expression_vec, t_level=activation_level)
        
       
        if protein_transcribe == True:
            
            self.transcription_state = True
            return protein_transcribe

        else:
            return False

        

    def map_expression_vector(self, e_data=None, t_level = 0.7):
        t_level = float(t_level)
        """Map expression vector. State function on expression vector to determine
        transcription state.

        Keyword Arguments:
            e_vector {[type]} -- [description] (default: {None})
        """
       
        
        express_sum = 0
        number_express = len(e_data)

        for expression in e_data:
            express_sum = express_sum + expression

        if number_express == 0:
            print (f'Error divide by zero. Transcription.')
            # exit()
        transcription_activity = express_sum/number_express
        #see if trade triggered
        
        #---debug
        #print (transcription_activity)
        # if transcription_activity > self.transcription_threshold:
        
        if transcription_activity > t_level:
            
            return True

        else:
            return False
    



    def mutate(self):
        self.transcription_threshold = random.random()
        #self.transcription_threshold_exit = random.random()


if __name__=="__main__":
    trans = Transcription()
    data = { 'expression_data':[0.3,0,0.65,0] }
    trans.transcribe(data)
