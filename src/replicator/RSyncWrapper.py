'''
Created on Aug 2, 2013

@author: saflores
'''
import subprocess, sys, os, logging
import constants
from os.path import exists, dirname
from Queue import Queue, Empty
from threading import Thread


class RSyncWrapper(object):
    '''
    wraps Rsync like a burrito
    '''


    def __init__(self, login, host):
        '''
        Constructor
        '''
        self.login = login
        self.host  = host
        self.io_q  = None
        
        self.outLogger = logging.getLogger('out')

    def SyncSingleFile(self, remote_f_name, tgt_local_name):
        self.io_q  = Queue()
        
        self.outLogger.debug('attempting to rsync from ' + self.host)
      
        if remote_f_name is None or tgt_local_name is None:
            raise ValueError
      
        # rsync will not create directories in this mode
        if not exists(dirname(tgt_local_name)):
            try:
                os.makedirs(dirname(tgt_local_name), 0777)
            except OSError, e:
                self.outLogger.critical('Error creating target directories. Can not continue')
                self.outLogger.critical(e)
                sys.exit(-1)
        
        tgt_local_name    = tgt_local_name
        
        cmd_lst = ['rsync', '-cv',
                    self.login + '@' + self.host + ':' + remote_f_name,
                    tgt_local_name]
        
        self.outLogger.debug(cmd_lst)
        proc =  subprocess.Popen(cmd_lst,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE
                                )
         
        stdout_watcher   = Thread(target=s_watcher, name='rsync stdout watcher', args=('rsync', proc.stdout, self.io_q))
        stderr_watcher   = Thread(target=s_watcher, name='rsync stderr watcher', args=('rsync_warning', proc.stderr, self.io_q))
        stdout_printer = Thread(target=printer, name="printer", args=(proc,self.io_q))
         
        stdout_watcher.start()
        stderr_watcher.start()
        stdout_printer.start()
         
        # wait for our auxiliary threads to die before anouncing the end
        while True:
            if stdout_printer.isAlive() or stdout_watcher.isAlive():
                pass
            else:
                break
         
        self.outLogger.info("--")
        
        if proc.poll() == 0:
            #success, return something 
            # if sucessful,l_name exists
            if exists(tgt_local_name):
            
                try:
                    os.chmod(tgt_local_name, 0777)    
                except OSError, e:
                    self.outLogger.warning(tgt_local_name + ' belongs to someone else!')
                
                return tgt_local_name
            
            else:
                return None
        else:

            if proc.poll() == 23:
                # remote file does not exist
                self.outLogger.critical('Could not read remote file:')
                self.outLogger.critical(' ' + remote_f_name)
                self.outLogger.critical('use repconf.py -w <program> for available .appli files in each program')
                sys.exit(-1)
                
            if proc.poll() == 255:
                # weird error on rsync, bail out
                self.outLogger.critical('rsync timed out')
                self.outLogger.critical('Are you sure you passed the Firewall?')
                sys.exit(-1)
            else:
                self.outLogger.critical('unknown error with rsync')
                self.outLogger.critical('check your permissions')
                sys.exit(-1)
                
        
    def SyncFilesFrom(self, input_f_name, r_root=constants.remote_root, l_root=constants.local_root):
        self.outLogger.debug('attempting to rsync from ' + self.host)
        self.io_q  = Queue()
                
        cmd_lst = ['rsync',
                   '-cvl', # checksum, verbose, copy likns as links
                   '--files-from=' + input_f_name,
                    self.login + '@' + self.host + ':' + constants.remote_root,
                    constants.local_root]
          
        self.outLogger.debug(cmd_lst)
        proc =  subprocess.Popen(cmd_lst,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE
                                )
        
        
        stdout_watcher = Thread(target=s_watcher, name='s_watcher', args=('rsync', proc.stdout, self.io_q))
        stderr_watcher = Thread(target=s_watcher, name='e_watcher', args=('rsync_warning', proc.stderr, self.io_q))
        stdout_printer = Thread(target=printer,   name='s_printer', args=(proc, self.io_q))
        
        stdout_watcher.start()
        stderr_watcher.start()
        stdout_printer.start()
        
        # wait for our auxiliary threads to die before anouncing the end
        while True:
            if stdout_printer.isAlive() or stdout_watcher.isAlive():
                pass
            else:
                break
        
        self.outLogger.info('rsync done (' + str(proc.poll()) + ')' )
        

########################################
def s_watcher(stream_name, stream, queue):
    for line in stream:
        queue.put( (stream_name, line) )
    if not stream.closed:
        stream.close()

########################################
def printer(process, queue):
    outLogger = logging.getLogger('out')
    while True:
        try:
            item = queue.get(True, 1)
            stream_name, line = item
            if line.endswith('\n'):
                line = line[:-1]

            if stream_name != 'rsync':
                outLogger.warning(line)
            else:
                outLogger.info(line)
        except Empty:
            if process.poll() is not None:
                break


