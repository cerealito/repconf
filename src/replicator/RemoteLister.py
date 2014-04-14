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

        
    def ls(self, f, passFilter, opts=[], limit=0):
        '''
            f is a file or directory to be passed as an argument to ls
            passFilter is a string to be passed to grep after ls
            opts is a list of strings to be passed to ls as options
            limit is a number to pass to tail
        '''

        cmd_lst  = ['ssh', self.login + '@' + self.host, 'ls', '-1']
        cmd_lst += opts
        cmd_lst += [f, '|', 'grep', passFilter]

        if limit != 0:
            cmd_lst += ['|', 'tail', '-'+str(limit) ]

        proc =  subprocess.Popen(cmd_lst,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        
        stdout, stderr = proc.communicate()
        
        if stdout:
            print stdout
        if proc.returncode != 0:
            if stderr:
                print stderr

                