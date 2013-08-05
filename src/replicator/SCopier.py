'''
Created on Jul 31, 2013

@author: saflores
'''

import subprocess
import constants
import os, stat
from os.path import basename, exists, dirname


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
#         print "copying remote file: "
#         print "  " + r_file
#         print "as: "
#         print "  " + l_name
#         print "Existing files will be overwritten"

        if not exists(dirname(l_name)):
            os.makedirs(dirname(l_name))
                
        cmd_lst = ['scp', self.login + '@' + self.host + ':' + r_file]
        
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
                
        # if sucessful,l_name exists
        if exists(l_name):
            os.chmod(l_name, 0777)
            return l_name
         
