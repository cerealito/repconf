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
from os.path import dirname, basename, splitext, join, exists

from replicator.EAReader import EAReader 
from replicator.ConfWriter import ConfWriter
from replicator.RemoteLister import RemoteLister
from replicator.SCopier import SCopier
from replicator.PlainWriter import PlainWriter

import replicator.constants as constants

import os


def main():
    
    usage = "usage: repconf [options] program file.appli"
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
                        help="shows available programs")
    
    opts, args = myParser.parse_args()
        
    ##################################################################
    # If in local mode, just one arg is needed ignore any other args
    if opts.local:
        etat_appli_f_name = args[0]
        ret = local(etat_appli_f_name, opts.output)
        sys.exit( ret )
    
    ##################################################################
    # show available .appli files in remote file system,
    #then exits, regardless of any other options
    if opts.show_available:
        
        if len(args) == 0:
            print 'listing known programs'
            
            for k,v in constants.programs.items():
                print k + ' : ' + v
             
            print 'try -w <program> for available .appli files in each program'
            
        if len(args) > 0:
            p     = args[0]
            p_dir = constants.programs.get(p)
            
            if p_dir == None:
                print "Do not know about program " + p
                print "Try -w for available programs"
                sys.exit(-1)
            
            print 'listing available appli files in ' + p
            print
            RemoteLister.ls(p_dir, "appli$")
        
        sys.exit(0)
    
    ##################################################################
    # If in remote mode
    if len(args) == 2:
        p     = args[0]
        etat_appli_f_name = args[1]
        
        p_dir = constants.programs.get(p)
        
        if p_dir == None:
            print "Do not know about program " + p
            print "Try -w for available programs"
            sys.exit(-1)
        
        print 'getting remote file ' + etat_appli_f_name
    
        myScp = SCopier()
        etat_appli_TMP = myScp.get(join(p_dir, etat_appli_f_name))
        local(etat_appli_TMP, opts.output, constants.default_dir)
    else:
        myParser.error("incorrect number of arguments. Try -h for help")
        # will exit on error.        
       
        
    ##################################################################
    # If no error, start doing the stuff

        
        
        

def local(etat_appli_f, output=None, remote_root=None):
    
    if remote_root:
        # apply dirname twice because we want the parent of the parent
        root_dir = dirname(dirname(remote_root))
    else:
        # apply dirname twice because we want the parent of the parent
        root_dir     =  dirname(dirname(etat_appli_f))

    f, ext = splitext(basename(etat_appli_f))      
    output_f     = "conf_" + f + ".xml"
    
    # rename output if needed
    if output:
        output_f = output
    
    #give user some output
    print
    print 'etat appli : ' + etat_appli_f
    print 'remote root: ' + root_dir
    
    
    #TODO: check for errors
    try:
        myReader  = EAReader(etat_appli_f)
        mySources = myReader.getFiles(root_dir)
        myWriter  = ConfWriter()
        myWriter.addEntityName(basename(etat_appli_f))
        
        anotherWriter = PlainWriter()
        anotherWriter.addSources(mySources)
        
    except IOError, ioe:
        # most probably etat_appli_f can not be read
        sys.exit(str(ioe))
    except AttributeError, ae:
        #most probably the passed file is not an etat appli
        sys.exit("The input file is not an appropriate etat.appli ")
    
    print "appending " + str(len(mySources)) + " repSrc elements"
    
    myWriter.addSources(mySources)
    myWriter.writeTo(output_f)
    anotherWriter.writeTo('rsync.txt')
    
    print "output file: " + output_f
    
    if exists(output_f):
        return 0 # shell convention for success
    else:
        return -1 # shell convention for failure


if __name__ == '__main__':
    main()