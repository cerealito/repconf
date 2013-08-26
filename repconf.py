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
    import inspect
    from os.path import dirname, abspath, join
    #when in CLI use inspect to locate the source directory
    src_dir = join(dirname(abspath(inspect.getfile(inspect.currentframe()))),'src')
    sys.path.append(src_dir)


from optparse import OptionParser

from os.path import dirname, basename, splitext, join, exists

from replicator.EAReader import EAReader 
from replicator.RemoteLister import RemoteLister
from replicator.PlainWriter import PlainWriter
from replicator.RSyncWrapper import RSyncWrapper
from replicator.logger import configureErrors, configureOutput

import replicator.constants as constants

import os
import logging
import ConfigParser

def main():
    
    usage = "usage: repconf [options] program file.appli"
    myParser = OptionParser(usage)
    
    myParser.add_option("-l",
                        "--local",
                        action="store_true",
                        dest="local",
                        help="use a local file as input instead of downloading from remote filer")
    
    myParser.add_option("-?",
                        "--what",
                        action="store_true",
                        dest="show_available",
                        help="shows available programs")
    
    opts, args = myParser.parse_args()

    

    ##################################################################
    # create tmp dir and default settings for first time use
    initialize()


    ##################################################################
    # init loggers
    errLogger = logging.getLogger('err')
    outLogger = logging.getLogger('out')
    
    configureErrors(errLogger, join(constants.tmp_d, 'errors.log') )
    configureOutput(outLogger, join(constants.tmp_d, 'output.log') )
   
    ##################################################################
    # If in local mode, just one arg is needed ignore any other args
    if opts.local:
        etat_appli_f_name = args[0]
        local(etat_appli_f_name)
        # TODO: exit status should reflect the success or failure of the command 
        sys.exit(0)
    
    ##################################################################
    # show available .appli files in remote file system,
    #then exits, regardless of any other options
    if opts.show_available:
        
        if len(args) == 0:
            print 'listing known programs'
            
            for k,v in constants.programs.items():
                print k + ' : ' + v
             
            print 'try \'./repconf.py <program> -?\' for available .appli files in each program'
            
        if len(args) > 0:
            p     = args[0]
            p_dir = constants.programs.get(p)
            
            if p_dir == None:
                print "Do not know about program " + p
                print "Try -? for available programs"
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
            print "Try -? for available programs"
            sys.exit(-1)
        
        outLogger.info('getting remote file ' + etat_appli_f_name)
        rsync = RSyncWrapper()
    
        f_r_src = join(p_dir, etat_appli_f_name);
        f_l_dst = constants.local_root + '/' + join(p_dir, basename(etat_appli_f_name))
    
        outLogger.debug('full remote source is    :' + f_r_src)
        outLogger.debug('full local destination is:' + f_l_dst)
        
        etat_appli_TMP = rsync.SyncSingleFile(f_r_src, f_l_dst)
        
        if exists(etat_appli_TMP):
            local(etat_appli_TMP, p_dir)
        else:
            self.errLogger.error("Input appli file could not be obtained from remote filesystem. Check your permissions\n")
            sys.exit(-1)
    else:
        myParser.error("incorrect number of arguments. Try -h for help")
        # will exit on error.        
       
        
######################################################################
def local(etat_appli_f, remote_root=None):
    
    errLogger = logging.getLogger('err')
    outLogger = logging.getLogger('out')
    
    if remote_root:
        # apply dirname twice because we want the parent of the parent
        root_dir = dirname(dirname(remote_root))
    else:
        # apply dirname twice because we want the parent of the parent
        root_dir     =  dirname(dirname(etat_appli_f))

    f, ext = splitext(basename(etat_appli_f))      
    
    #give user some output
    outLogger.info('etat appli : ' + etat_appli_f)
    outLogger.info('remote root: ' + root_dir)
    
    
    #TODO: check for errors
    try:
        myReader  = EAReader(etat_appli_f)
        mySources = myReader.getFiles(root_dir)
        
        anotherWriter = PlainWriter()
        anotherWriter.addSources(mySources)
        
    except IOError, ioe:
        # most probably etat_appli_f can not be read
        sys.exit(str(ioe))
    except AttributeError, ae:
        #most probably the passed file is not an etat appli
        sys.exit("The input file is not an appropriate etat.appli ")
    
    outLogger.info("appending " + str(len(mySources)) + " repSrc elements")
    
    anotherWriter.writeTo(constants.rsync_tmp)
    
    
    rsync = RSyncWrapper()
    
    rsync.SyncFilesFrom(constants.rsync_tmp, constants.remote_root, constants.local_root)

    
######################################################################
def initialize():
    if not exists(constants.settings_f):
        
        if not exists(constants.tmp_d):
            os.makedirs(constants.tmp_d, 0775)
                
        print 'Initializing with default settings ' + constants.settings_f
    
        settings_f = open(constants.settings_f, 'w')
        
        contents = [
             '# Default settings file for repconf',
             '# Fill with the proper values      ',
             '                                   ',
             '[DEFAULT]',
             '# the login name to use in the remote location',
             'username: toto',
             '# the ip or hostname of the remote rsync server',
             'server  : 195.220.10.144',
             '\n'
             ]
        
        for line in contents:
            settings_f.write(line)
            settings_f.write('\n')
            
        settings_f.close()

######################################################################    
if __name__ == '__main__':
    main()