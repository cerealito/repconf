'''
Created on Aug 2, 2013

@author: saflores
'''
import subprocess, sys, os, logging
import constants
from os.path import basename, isfile, join, exists
from Queue import Queue, Empty
from threading import Thread


class RSyncWrapper(object):
    '''
    wraps Rsync like a burrito
    '''


    def __init__(self, login=constants.default_login, host=constants.default_host):
        '''
        Constructor
        '''
        self.login = login
        self.host  = host
        self.io_q = Queue()
        
        self.stderrLog = logging.getLogger('err')
        self.stdoutLog = logging.getLogger('out')

    def SyncSingleFile(self, remote_f_name, tgt_local_name=None):
        
        #print "attempting to rsync from " + self.host
        
        if tgt_local_name is None:
            tgt_local_name = remote_f_name
      
        full_remote_f_name = remote_f_name
        full_tgt_f_name    = tgt_local_name
        
        cmd_lst = ['rsync', '-cv',
                    self.login + '@' + self.host + ':' + full_remote_f_name,
                    full_tgt_f_name]
        
        proc =  subprocess.Popen(cmd_lst,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE
                                )
         
        stdout_watch   = Thread(target=stream_watcher, name='rsync stream watcher', args=('rsync', proc.stdout, self.io_q))
        stdout_printer = Thread(target=printer, name="printer", args=(proc,self.io_q))
         
        stdout_watch.start()
        stdout_printer.start()
         
        # wait for our auxiliary threads to die before anouncing the end
        while True:
            if stdout_printer.isAlive() or stdout_watch.isAlive():
                pass
            else:
                break
             
        print "--"
         
        if proc.stderr:
            self.stderrLog.error(proc.stderr)

        # if sucessful,l_name exists
        if exists(full_tgt_f_name):
            os.chmod(full_tgt_f_name, 0777)
            return full_tgt_f_name
        else:
            return None
        
    def SyncFilesFrom(self, input_f_name, r_root=constants.remote_root, l_root=constants.local_root):
        print "attempting to rsync from " + self.host
      
                
        cmd_lst = ['rsync',
                   '-cvptgoL', # checksum, verbose, permissions, times, group, owner, DEREFERENCE LINKS
                   '--files-from=' + constants.rsync_tmp,
                    self.login + '@' + self.host + ':' + constants.remote_root,
                    constants.local_root]
          
         
        proc =  subprocess.Popen(cmd_lst,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE
                                )
        
        stdout_watch   = Thread(target=stream_watcher, name='rsync stream watcher', args=('rsync', proc.stdout, self.io_q))
        stdout_printer = Thread(target=printer, name="printer", args=(proc,self.io_q))
        
        stdout_watch.start()
        stdout_printer.start()
        
        # wait for our auxiliary threads to die before anouncing the end
        while True:
            if stdout_printer.isAlive() or stdout_watch.isAlive():
                pass
            else:
                break
            
        print "done"
        
        if proc.stderr:
            self.stderrLog.error(proc.stderr)

########################################
def stream_watcher(stream_name, stream, queue):
        for line in stream:
            queue.put( (stream_name, line) )
        if not stream.closed:
            stream.close()

########################################
def printer(process, queue):
        while True:
            try:
                item = queue.get(True, 1)
            except Empty:
                if process.poll() is not None:
                    break
            else:
                stream_name, line = item
                sys.stdout.write( stream_name + ': ' + line )

