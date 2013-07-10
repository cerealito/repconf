'''
Created on Apr 22, 2013

@author: saflores
'''

import unittest
import os

from replicator.EAReader import EAReader 
from replicator.ConfWriter import ConfWriter


class Test(unittest.TestCase):


    

    
    def setUp(self):
        print 'working on \n' + os.getcwd() + '\n'

    def tearDown(self):
        pass

           
    def testWrite(self):
        etat_appli_f = './etat_STD5_officiel.appli'
        root_dir     = '/home/SIMU_DEVELOPPEMENT/APPLICATIONS/Linux_2.4.7/A350/A350H'
        
        output_f     = '002_xml_output.xml'
        
        myReader   = EAReader(etat_appli_f)
        repSources = myReader.getFiles(root_dir)
        
        myWriter = ConfWriter()
        
        print "appending " + str(len(repSources)) + " repSrc elements"
        myWriter.addSources(repSources)
        
        myWriter.writeTo(output_f)
        


        self.assertTrue(os.path.exists(output_f), 'something went wrong while writing')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWrite']
    unittest.main()