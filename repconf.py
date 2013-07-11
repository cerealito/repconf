#!/usr/bin/env python
'''
Created on Jul 9, 2013

@author: saflores
'''

if __name__ == '__main__':
    # explicitly append the ./src directory to the current path.
    # PyDev does this Implicitly but it is better to have it explicit
    # this makes the tool work the same in tests and in CLI
    import sys
    sys.path.append("./src")


from optparse import OptionParser
from os.path import basename

from replicator.EAReader import EAReader 
from replicator.ConfWriter import ConfWriter


def main():
    
    usage = "usage: repconf [options] etat_appli root_dir"
    myParser = OptionParser(usage)
    
    myParser.add_option("-o",
                        "--output",
                        dest="output",
                        help="write output to FILE")
    
    opts, args = myParser.parse_args()

    if len(args) == 2:
        # inputs and output
        etat_appli_f = args[0]
        root_dir     = args[1]
        output_f     = "conf_" + basename(etat_appli_f)
               
        # rename output if needed
        if opts.output:
            output_f = opts.output
        
        #give user some output
        print 'etat appli : ' + etat_appli_f
        print 'remote root: ' + root_dir
        
        
        #TODO: check for errors
        try:
            myReader  = EAReader(etat_appli_f)
            mySources = myReader.getFiles(root_dir)
            myWriter  = ConfWriter()
            myWriter.addEntityName(basename(etat_appli_f))

        except IOError, ioe:
            # most probably etat_appli_f can not be read
            sys.exit(str(ioe))
        except AttributeError, ae:
            #most probably the template is not as the code expects
            sys.stderr.write(str(ae) + '\n')
            sys.exit('There is most likley an error with the Template file. Check it')
        
        print "appending " + str(len(mySources)) + " repSrc elements"
        
        myWriter.addSources(mySources)
        myWriter.writeTo(output_f)
        
        print "output file: " + output_f
        print "bye"
        
    else:
        myParser.error("incorrect number of arguments. Try -h for help")


if __name__ == '__main__':
    main()