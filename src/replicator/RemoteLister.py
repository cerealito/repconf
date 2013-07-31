'''
Created on Jul 31, 2013

@author: saflores
'''

import subprocess
import constants


class RemoteLister(object):
    '''
    A class that will wrap rsync or other mechanisms to interrogate
    a remote file system for files
    '''

    def __init__(self,params):
        '''
        Constructor
        '''

    @staticmethod        
    def ls(f, passFilter):
        '''
            pass filter will be passed to GREP
        '''
        
        cmd_lst = ['ssh', constants.default_login + '@' + constants.default_host, 'ls', '-1', f, '|', 'grep', passFilter]
        
        proc =  subprocess.Popen(cmd_lst,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        
        stdout, stderr = proc.communicate()
        
        if stdout:
            print stdout
        if proc.returncode != 0:
            if stderr:
                print stderr
                