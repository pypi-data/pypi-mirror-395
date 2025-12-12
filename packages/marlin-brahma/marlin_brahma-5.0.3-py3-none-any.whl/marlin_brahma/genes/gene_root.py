import random


class ConditionalRoot(object):
    """This is the root class for all conditional objects. FS_DNA objects all take input, process them and fire back either 0 or 1.
    Inputs can be any numberical or defined vector. These are the building blocks of the decision making FSM.


    Arguments:
        object {[type]} -- [object]
    """

    def __init__(self, condition=None, env=None):
        
        # conditional name
        self.condition = condition
        # id of condition
        self.i_D = self.define_tag()
        # market condition is attached to
        self.env = env
        # date codition created for trader
        self.DOB = self.define_dob()
        #debug
        self.safeRun = False
        # name
        self.name = f'{self.i_D}_{condition}'

    def Safe(self):
        self.safeRun = True

    def Start(self):
        """
        '''Routine to check that the gene ran with data. This is required for all genes and can be used for debugging
        """
        self.safeRun = False

    def __str__(self):
        return (" Condition: {0} , Env: {1} , DOB: {2}".format(self.condition, self.env, self.DOB))



    def run(self, input = [], active_price=0):

        """Root call to main function 'run'. It calls a default input of a vector and sets the state to 0.
        This function must be overridden in derived classes.
        Keyword Arguments:
            input {list} -- [input list] (default: {[]})
        """
        state_lcl = 0

        self.state = state_lcl
        return self.state



    def define_tag(self):
        return "geneTag" + str(random.randint(10,100000))

    def define_dob(self):
        from datetime import date
        curr_date = str(date.today())
        return curr_date

    #evo code
    def mutate(self):
        print ("Root mutate. Must override.")
