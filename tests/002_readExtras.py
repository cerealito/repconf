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


from replicator.ExtraFileReader import ExtraFileReader


class Test(unittest.TestCase):     

    def setUp(self):
        print '=================================='
        print 'working on \n' + os.getcwd() + '\n'
        

    def tearDown(self):
        pass


    def testReadV2(self):
        f = './DALI_V2.xml'
        print f
        myReader   = ExtraFileReader(f)
        
        self.repSources = myReader.getFiles()
        
        for src in self.repSources:
            print src
            
    def testReadV1(self):
        f = './DALI_V1.xml'
        print f
        
        myReader   = ExtraFileReader(f)
        
        self.repSources = myReader.getFiles()
        
        for src in self.repSources:
            print src
            

            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRead']
    unittest.main()