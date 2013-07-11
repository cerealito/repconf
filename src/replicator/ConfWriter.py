'''
Created on Jul 5, 2013

@author: saflores
'''
from xml.dom import minidom

from os.path import exists

class ConfWriter(object):
    '''
    This class will generate the output xml file known as conf_XXXX.xml based on a template
    '''
            

    def __init__(self, template=None):
        '''
        Constructor
        '''
        
        # i dunno how we will ship this
        if template != None:
            self.template = template
        else: 
            self.template = '/home/saflores/workspace/repconf/src/templates/00_basic.xml'
        
        #check
        if not exists(self.template):
            raise IOError
        
        #start form the template
        self.conf_xmldoc = minidom.parse(self.template)
        
    def addEntityName(self, name):
        '''
        adds a 'nom' attribute to the 'entite' tag in the template, and assigns it the value
        of the passed name string
        
        '''
        #identify the node: it is the first 'entite' tag.
        # TODO: what if the template does not have the searched node?
        entityTag = self.conf_xmldoc.getElementsByTagName('entite').item(0)
        entityTag.setAttribute('nom', name)
     
    def addSources(self, repSources):
        '''
        writes the output files based on a template and the given list of repository sources
        '''
        #identify the node where we will put the repSources
        # TODO: what if the template does not have a data node?
        dataTag = self.conf_xmldoc.getElementsByTagName('data').item(0)
        
        #create an xml node for every element of the repSources:
        for src in repSources:
            tag = self.conf_xmldoc.createElement('srcRep')
            txt = self.conf_xmldoc.createTextNode(src.fullPath())
            
            tag.appendChild(txt)
            
            dataTag.appendChild(tag)
    
    def writeTo(self, output_f):
        self.conf_xmldoc.writexml( open(output_f,'w') ,
                                   indent    = '    ',
                                   addindent = '    ',
                                   newl      = '\n'   )    
        
    