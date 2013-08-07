"""
#-------------------- Header/Title block ---------------------------
# This is module configures the logging facilities
#--------------------------------------------------------------------
# . Configuration and modification management
#--------------------------------------------------------------------
__version__ = "1.0"
__date__ = "20/07/2011"
__author__ = "Sogeti High Tech "
# History 
# + 20/07/2011 : Creation of the file
#-------------------- Instruction 'IMPORT' --------------------------
# Declaration of imported modules
#----
"""
import logging

def configure(logger_p, path='./Log.txt'):
    """
    change config here
    """
    # if no handlers have been configured...
    if 0 == len(logger_p.handlers): 
        logger_p.setLevel(logging.DEBUG)
        
        
        # this will make the project logger write all messages in a file
        file_handler = logging.FileHandler(path, mode = 'w')
        line_format  = "%(levelname)s" + ": %(message)s "
    
        f_formatter  = logging.Formatter(line_format)
        file_handler.setFormatter(f_formatter)
        
        logger_p.addHandler(file_handler)
        
                            
        # this will make the project logger write INFO messages to the console 
        console_handler = logging.StreamHandler()
        c_formatter     = logging.Formatter(line_format)
        console_handler.setFormatter(c_formatter)
        
        console_handler.setLevel(logging.CRITICAL)
    
        logger_p.addHandler(console_handler)
    else:
        pass

