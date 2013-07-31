#!/usr/bin/env python
'''
Created on Jul 9, 2013

@author: saflores
'''

if __name__ == '__main__':
    # explicitly append the ./src directory to the current path.
    # PyDev does this Implicitly but it is better to have it explicit
    # this makes the tool work the same in tests and in CLI
    import sys
    sys.path.append("./src")


from optparse import OptionParser
from os.path import dirname, basename, splitext

from replicator.EAReader import EAReader 
from replicator.ConfWriter import ConfWriter
from replicator.RemoteLister import RemoteLister
import replicator.constants as constants

import os


def main():
    
    usage = "usage: repconf [options] /path/to/file.appli"
    myParser = OptionParser(usage)
    
    myParser.add_option("-o",
                        "--output",
                        dest="output",
                        help="write output to FILE")
    
    myParser.add_option("-l",
                        "--local",
                        action="store_true",
                        dest="local",
                        help="use a local file as input instead of downloading from remote filer")
    
    myParser.add_option("-w",
                        "--what",
                        action="store_true",
                        dest="show_available",
                        help="shows available .appli files in airbus ")
    
    opts, args = myParser.parse_args()
    
    ##################################################################
    # show available .appli files in remote file system,
    #then exits, regardless of any other options
    if opts.show_available:
        print 'listing available .appli files in '
        print constants.default_host + ':' + constants.default_dir
        print
        RemoteLister.ls(constants.default_dir, "appli$")
        
        sys.exit(0)
    
    ##################################################################
    # Real replication needs at least one argument:    
    if len(args) == 1:
        # inputs and output
        etat_appli_f = args[0]
    else:
        myParser.error("incorrect number of arguments. Try -h for help")
        # will exit on error.        
       
        
    ##################################################################
    # If no error, start doing the stuff
    if opts.local:
        local(etat_appli_f, opts.output)
    else:
        print 'getting remote file'
        
        

def local(etat_appli_f, output=None):
    # apply dirname twice because we want the parent of the parent
    root_dir     =  dirname(dirname(etat_appli_f))

    f, ext = splitext(basename(etat_appli_f))      
    output_f     = "conf_" + f + ".xml"
    
    # rename output if needed
    if output:
        output_f = output
    
    #give user some output
    print 'etat appli : ' + etat_appli_f
    print 'remote root: ' + root_dir
    
    
    #TODO: check for errors
    try:
        myReader  = EAReader(etat_appli_f)
        mySources = myReader.getFiles(root_dir)
        myWriter  = ConfWriter()
        myWriter.addEntityName(basename(etat_appli_f))

    except IOError, ioe:
        # most probably etat_appli_f can not be read
        sys.exit(str(ioe))
    except AttributeError, ae:
        #most probably the passed file is not an etat appli
        sys.exit("The input file is not an appropriate etat.appli ")
    
    print "appending " + str(len(mySources)) + " repSrc elements"
    
    myWriter.addSources(mySources)
    myWriter.writeTo(output_f)
    
    print "output file: " + output_f
    print "bye"


if __name__ == '__main__':
    main()