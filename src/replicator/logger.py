import logging

def configureErrors(logger_p, path='./Log.txt'):
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
        
        #ignore debug and info
        console_handler.setLevel(logging.ERROR)
    
        logger_p.addHandler(console_handler)
    else:
        pass

def configureOutput(logger_p, path='./Log.txt'):
    """
    change config here
    """
    # if no handlers have been configured...
    if 0 == len(logger_p.handlers): 
        
        logger_p.setLevel(logging.DEBUG)

        # this will make the project logger write all messages in a file
        file_handler = logging.FileHandler(path, mode = 'w')
        fh_formatter  = logging.Formatter('%(message)s')
        file_handler.setFormatter(fh_formatter)
        
        #ignore debug messages
        file_handler.setLevel(logging.DEBUG)
        
        logger_p.addHandler(file_handler)
        
                            
        # this will make the project logger write INFO messages to the console 
        
        console_handler = logging.StreamHandler()
        ch_formatter     = logging.Formatter('%(message)s')
        console_handler.setFormatter(ch_formatter)
        
        #ignore debug messages
        console_handler.setLevel(logging.INFO)
    
        logger_p.addHandler(console_handler)
    else:
        pass

