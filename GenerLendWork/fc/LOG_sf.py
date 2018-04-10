# -*- coding: utf-8 -*-

import logging
from logging import getLogger
from logging import FileHandler 
from logging import StreamHandler 
from logging import Formatter 

#code for log
#Using:     logger.info( 'Some information' ) to replace print( 'Some information' )
logger = getLogger( 'SF:' )
logger.setLevel( logging.DEBUG)
#logging.basicConfig( level = logging.INFO )

#LOG_FILE = 'Log_test.log'

fh = FileHandler( 'Log-test.log' )
fh.setLevel( logging.INFO )

ch = StreamHandler()
#ch.setLevel( logging.WARN)
ch.setLevel( logging.DEBUG)

formatter = Formatter( '%(asctime)s - %(name)s - %(levelname)s:\n%(message)s\n' )
formatter_ch = Formatter( '%(name)s:     %(message)s' )
fh.setFormatter( formatter )
ch.setFormatter( formatter_ch )

logger.addHandler(fh)
logger.addHandler(ch)

"""
The code below is a test for module logging.
"""
tts = '0'
ttn = int(tts) 
logger.info( 'ttn = %d ' % ttn )
logger.debug( 'Debug:ttn = %d ' % ttn )
ldebug = logger.debug
linfo = logger.info
ldebug( 'LDB\n\n rename loggger.debug to ldebug!!' )
try:
    print( 10 / ttn )
except Exception as e:
    ldebug( e )
