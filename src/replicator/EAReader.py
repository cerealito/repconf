'''
Created on 4 juil. 2013

@author: saflores

'''

from xml.dom import minidom
from xml.parsers.expat import ExpatError
from os.path import join

import sys, logging

class EAReader(object):
    '''
    This reads the etat_XXX_appli xml file
    '''

    def __init__(self, ea_file):
        '''
        Constructor
        '''
        self.errLogger = logging.getLogger('err')
        self.outLogger = logging.getLogger('out')
        
        try:        
            self.ea_xmldoc = minidom.parse(ea_file)
        except ExpatError, e:
            self.errLogger.critical(str(e) + '\n')
            self.errLogger.critical('Input file '+ ea_file + ' is not a well formed xml file')
            sys.exit(-1)
        self.interesting_tags = ["Taches",
                       "Sequencement",
                       "Exceptions",
                       "InitFlot",
                       "XPMI",
                       "Chargement",
                       "Liboperateur",
                       "GenericServices",
                       "GdC",
                       "Modele"
                       ]
        
        
    def getFiles(self, root_dir):
        '''
        gets all the interesting files and puts them on a list of RepSrc
        '''
        
        # this gets the first XML node called "Elements"
        elementTag = self.ea_xmldoc.getElementsByTagName("Elements").item(0)
        
        lst_repsrc = []

        #################################
        for tag in self.interesting_tags:                       
            tag_lst = elementTag.getElementsByTagName(tag)
            
            self.outLogger.debug(">>> " + tag + ":")
            #################################
            for i in range( tag_lst.length) :
                
                # each file is represented by a RepSrc object
                f = RepSrc()
                
                f.dirname = root_dir    
                
                # files are always in Rep_Livraison, even if Rep_Livrasion is empty
                f.appendToDirname(tag_lst.item(i).getAttribute("Rep_Livraison"))
                
                # models are ALWAYS in sous-modeles directory
                # and the basename is in the Librarie attribute
                if (tag == 'Modele'):
                    f.appendToDirname("sous_modeles")
                    f.basename = tag_lst.item(i).getAttribute("Librairie")
                # for every other tag look for attribute Nom
                else:
                    f.basename = tag_lst.item(i).getAttribute("Nom")
                
                lst_repsrc.append(f)
  
            #################################          
        #################################
        
        return lst_repsrc

class RepSrc(object):
    def __init__(self):
        self.basename = ''
        self.dirname  = ''
    
    def fullPath(self):
        return join(self.dirname, self.basename)
    
    def appendToDirname(self, extra_dir):
        self.dirname = join(self.dirname, extra_dir)
    
    def __str__(self, *args, **kwargs):
        return self.fullPath()
    
