'''
Created on Apr 22, 2013

@author: saflores
'''

import unittest
import os

from replicator.EAReader import EAReader 
from replicator.ConfWriter import ConfWriter


class Test(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(Test, self).__init__(methodName)
        print "constructor"
        self.repSources = []
        

    def setUp(self):
        print 'working on \n' + os.getcwd() + '\n'
        

    def tearDown(self):
        pass


    def testRead(self):
        etat_appli_f = './etat_STD5_officiel.appli'
        root_dir     = '/home/SIMU_DEVELOPPEMENT/APPLICATIONS/Linux_2.4.7/A350/A350H'
        
        myReader   = EAReader(etat_appli_f)
        self.repSources = myReader.getFiles(root_dir)
        
        for src in self.repSources:
            print src
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRead']
    unittest.main()