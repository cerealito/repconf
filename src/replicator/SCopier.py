'''
Created on Jul 31, 2013

@author: saflores
'''

import subprocess
import constants
from os.path import basename, isfile


class SCopier(object):
    '''
    wraps scp
    '''


    def __init__(self, login=constants.default_login, host=constants.default_host):
        '''
        Constructor
        '''
        self.login = login
        self.host  = host

    
    def get(self, r_file, l_name=None):
        print "copying remote file: "
        print "  " + r_file
        print "to current directory. Existing files will be overwritten"
                
        cmd_lst = ['scp', '-p', self.login + '@' + self.host + ':' + r_file]
        
        if not l_name:
            l_name = basename(r_file)
        
        cmd_lst.append(l_name)
        
        proc =  subprocess.Popen(cmd_lst,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        
        stdout, stderr = proc.communicate()
        
        if stdout:
            print stdout
        if proc.returncode != 0:
            if stderr:
                print stderr
                
        # if sucessful,l_name is a file
        if isfile(l_name):
            return l_name
         
