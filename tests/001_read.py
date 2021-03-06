'''
Created on Apr 22, 2013

@author: saflores
'''
# explicitly append the ./src directory to the current path.
# PyDev does this implicitly but it is better to have it explicit
# this makes the tool work the same in tests and in CLI
import sys
import inspect
from os.path import dirname, abspath, join
#when in CLI use inspect to locate the source directory
src_dir = join(dirname(dirname(abspath(inspect.getfile(inspect.currentframe())))),'src')
sys.path.append(src_dir)

import unittest
import os


from replicator.EAReader import EAReader 


class Test(unittest.TestCase):     

    def setUp(self):
        print '=================================='
        print 'working on \n' + os.getcwd() + '\n'
        

    def tearDown(self):
        pass


    def testReadOK(self):
        etat_appli_f = './etat_STD5_officiel.appli'
        root_dir     = '/home/SIMU_DEVELOPPEMENT/APPLICATIONS/Linux_2.4.7/A350/A350H'
        
        myReader   = EAReader(etat_appli_f)
        self.repSources = myReader.getFiles(root_dir)
        
        for src in self.repSources:
            print src
            
    def testReadKO(self):
        etat_appli_f = '../ref/conf_A350AC-1.xml'
        root_dir     = '/home/SIMU_DEVELOPPEMENT/APPLICATIONS/Linux_2.4.7/A350/A350H'
        
        try:
            myReader   = EAReader(etat_appli_f)
            self.repSources = myReader.getFiles(root_dir)
        except AttributeError, ae:
            print "input file for EAReader not in appropriate format"
        

            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRead']
    unittest.main()