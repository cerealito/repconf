import logging
from logging import FileHandler, StreamHandler, Formatter

def configureOutput(logger_p, path='./Log.txt'):
    """
    configures the logging
    """
    # if no handlers have been configured...
    if 0 == len(logger_p.handlers): 
        
        # let everything pass by default
        logger_p.setLevel(logging.DEBUG)

        # this will make the project logger write all messages in a file
        file_handler = FileHandler(path, mode = 'w')
        file_handler.setFormatter(Formatter('%(levelname)-8s : %(message)s'))
        
        # accept even the most trivial shit
        file_handler.setLevel(logging.DEBUG)
        logger_p.addHandler(file_handler)
        
        # this will make the logger write INFO messages to the console 
        console_handler = StreamHandler()
        console_handler.setFormatter(Formatter('%(message)s'))
        
        #ignore debug messages, only Info, warnings, errors and criticals
        console_handler.setLevel(logging.INFO)
    
        logger_p.addHandler(console_handler)
    else:
        pass

