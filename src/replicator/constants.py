'''
Created on Jul 31, 2013

@author: saflores
'''

from os.path import join, dirname, abspath
from os import environ
import inspect

# directory of THIS file at runtime:
runtime_d = dirname(abspath(inspect.getfile(inspect.currentframe())))

# origin-directories
programs = {
            'A350C' : '/home/SIMU_DEVELOPPEMENT/APPLICATIONS/Linux_2.4.7/A350/A350C/application/',
            'A350H' : '/home/SIMU_DEVELOPPEMENT/APPLICATIONS/Linux_2.4.7/A350/A350H/application/',
            'S400D' : '/home/SIMU_DEVELOPPEMENT/APPLICATIONS/LINUX/A400M/S400D/application/',
			'MOSART_A380_PLFREF'  : '/home/SIMU_MOSART/APPLICATIONS/LINUX/A380M/PLFREF/application/',
            'MOSART_DT_PLFREF'    : '/home/SIMU_MOSART/APPLICATIONS/LINUX/DT/PLFREF/application/'
           }

local_root  = '/'
remote_root = '/'

# temp dir is hidden in the user's home
tmp_d    = join(environ.get('HOME'), '.repconf_d/')

settings_f = join(tmp_d, 'settings.txt') 
rsync_tmp  = join(tmp_d, 'file_list.txt')

    
