'''
Created on Aug 1, 2013

@author: saflores
'''

class PlainWriter(object):
    '''
    This class will generate a plain text file to be used by rsync
    '''
            

    def __init__(self):
        '''
        Constructor
        '''
        self.sources = None
     
    def addSources(self, repSources):
        '''
        writes the output files based on a template and the given list of repository sources
        '''
        self.sources = repSources
    
    def writeTo(self, output_f):
        f = open(output_f,'w')
        for s in self.sources:
            f.write(str(s) + '\n')
        f.close()