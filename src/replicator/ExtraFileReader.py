'''
Created on 4 juil. 2013

@author: saflores

'''

from xml.dom import minidom
from xml.parsers.expat import ExpatError
from os.path import join, dirname, basename

import logging

class ExtraFileReader(object):
    '''
    This reads the extra file Appli XXX xml file
    '''

    def __init__(self, ea_file):
        '''
        Constructor
        '''
        self.outLogger = logging.getLogger('out')
        
        try:        
            self.ea_xmldoc = minidom.parse(ea_file)
        except ExpatError, e:
            self.outLogger.critical(str(e) + '\n')
            self.outLogger.critical('Input file '+ ea_file + ' is not a well formed xml file')
            raise ExpatError('Not a proper application file: ' + ea_file )
        except IOError, e:
            raise e
            
        self.interesting_tags = [ 'Batch', 'Shell' ]
    
    def getFiles(self):
        if self.getVersion() == 1:
            return self.__getFilesV1()
        else:
            return self.__getFilesV2()
    
    def getVersion(self):
        # dali V2 extras have "Scripts" tag
        ScriptsTag = self.ea_xmldoc.getElementsByTagName("Scripts").item(0)
        
        if ScriptsTag:
            return 2
        else:
            return 1
    
    def __getFilesV1(self):
        '''
            blahhh
        '''
        # this gets the first XML node called "Elements"
        
        ShellsTag = self.ea_xmldoc.getElementsByTagName("Shells").item(0)
        
        kshScriptsDir = ShellsTag.getAttribute("path") 
        batScriptsDir = join(dirname(kshScriptsDir), "BATCH")        
                
        lst_repsrc = []
        #################################
        for tag in self.interesting_tags:                       
            tag_lst = self.ea_xmldoc.getElementsByTagName(tag)
            
            #self.outLogger.debug(">>> " + tag + ":")
            #################################
            for i in range( tag_lst.length) :
                
                # each file is represented by a RepSrc object
                f = RepSrc()
                                
               
                if (tag == 'Batch'):
                    f.appendToDirname(batScriptsDir)
                    if tag_lst.item(i).getAttribute("fileName"):
                        f.basename = tag_lst.item(i).getAttribute("fileName") +'_'+ tag_lst.item(i).getAttribute("version") + ".bat"
                    else:
                        f.basename = tag_lst.item(i).getAttribute("name") +'_'+ tag_lst.item(i).getAttribute("version") + ".bat"
                    
                     
                # for every other tag look for attribute Nom
                elif (tag == 'Shell'):
                    f.appendToDirname(kshScriptsDir)
                    
                    if tag_lst.item(i).getAttribute("fileName"):
                        f.basename = tag_lst.item(i).getAttribute("fileName") +'_'+ tag_lst.item(i).getAttribute("version") + ".ksh"
                    else:
                        f.basename = tag_lst.item(i).getAttribute("name") +'_'+ tag_lst.item(i).getAttribute("version") + ".ksh"
                
                lst_repsrc.append(f)
  
            #################################          
        #################################        
        return lst_repsrc

    def __getFilesV2(self):
        '''
        gets all the interesting files and puts them on a list of RepSrc
        '''
        
        # this gets the first XML node called "Scripts"
        ProjectTag = self.ea_xmldoc.getElementsByTagName("Project").item(0)
        ScriptsTag = self.ea_xmldoc.getElementsByTagName("Scripts").item(0)
        
        allScriptsRoot = ProjectTag.getAttribute("ux_root")
        batScriptsDir  = join( ScriptsTag.getAttribute("scripts_path"), 'BATCH') 
        kshScriptsDir  = join( ScriptsTag.getAttribute("scripts_path"), 'SH'   )
    
        lst_repsrc = []        
        #################################
        for tag in self.interesting_tags:                       
            tag_lst = ScriptsTag.getElementsByTagName(tag)
            
            #self.outLogger.debug(">>> " + tag + ":")
            #################################
            for i in range( tag_lst.length) :
                
                # each file is represented by a RepSrc object
                f = RepSrc()
                
                f.dirname = allScriptsRoot
                
                # models are ALWAYS in sous-modeles directory
                # and the basename is in the Librarie attribute
                if (tag == 'Batch'):
                    f.appendToDirname(batScriptsDir)
                    f.basename = tag_lst.item(i).getAttribute("name") +'_'+ tag_lst.item(i).getAttribute("version") + ".bat" 
                # for every other tag look for attribute Nom
                elif (tag == 'Shell'):
                    f.appendToDirname(kshScriptsDir)
                    f.basename = tag_lst.item(i).getAttribute("name") +'_'+ tag_lst.item(i).getAttribute("version") + ".ksh"
                
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
    
