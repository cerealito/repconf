'''
Created on Jul 31, 2013

@author: saflores
'''

import subprocess

class RemoteLister(object):
    '''
    A class that will wrap rsync or other mechanisms to interrogate
    a remote file system for files
    '''

    def __init__(self, login, host):
        '''
        Constructor
        '''
        self.login = login
        self.host  = host

        
    def ls(self, f, passFilter):
        '''
            pass filter will be passed to GREP
        '''
        
        cmd_lst = ['ssh', self.login + '@' + self.host, 'ls', '-1', f, '|', 'grep', passFilter]
        
        proc =  subprocess.Popen(cmd_lst,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        
        stdout, stderr = proc.communicate()
        
        if stdout:
            print stdout
        if proc.returncode != 0:
            if stderr:
                print stderr

                