#!
"""
This is for error and log-file handling
Need to import os for filename (location of handling)

----------------------------------------------------------------------------------

DEBUG get no file log:

    my3xceptions.logger.debug('   - [%s/msg()] -- This is a DEBUG --' % (os.path.basename(__file__)))

----------------------------------------------------------------------------------

INFO, WARNING, ERROR, CRITICAL get a file log:

    my3xceptions.logger.info('    - [%s/msg()] -- This is a INFO --' % (os.path.basename(__file__)))

    my3xceptions.logger.warning(' - [%s/msg()] -- This is a WARNING --' % (os.path.basename(__file__)))

    my3xceptions.logger.error('   - [%s/msg()] -- This is a ERROR --' % (os.path.basename(__file__)))

    my3xceptions.logger.critical('- [%s/msg()] -- This is CRITICAL --' % (os.path.basename(__file__)))

----------------------------------------------------------------------------------
10 - DEBUG -- information important for troubleshooting, and usually suppressed in normal day-to-day operation
20 - INFO -- day-to-day operation as "proof" that program is performing its function as designed
30 - WARN -- out-of-nominal but recoverable situation, *or* coming upon something that may result in future problems
40 - ERROR -- something happened that necessitates the program to do recovery, but recovery is successful. Program is likely not in the originally expected state, though, so user of the program will need to adapt
50 - CRITICAL -- something happened that cannot be recovered from, and program likely need to terminate lest everyone will be living in a state of sin
----------------------------------------------------------------------------------
"""

# lib import
import logging
import os

# script import
# import
# import
# import

# # setting the logger
# logging.basicConfig(format='%(asctime)s.%(msecs)02d - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()  # https://realpython.com/python-logging/
f_handler = logging.FileHandler('file.log')

# Activate INFO and DEBUG
logger.setLevel(logging.INFO)  # important: https://stackoverflow.com/questions/21105753/python-logger-not-working
logger.setLevel(logging.DEBUG)

# write to file: INFO, WARNING, ERROR, CRITICAL
f_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.INFO)
# f_handler.setLevel(logging.DEBUG)


# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s.%(msecs)03d - [%(name)s] - %(levelname)s  %(message)s', datefmt='%d-%b-%y %H:%M:%S')
f_format = logging.Formatter('%(asctime)s.%(msecs)03d - [%(name)s] - %(levelname)s  %(message)s', datefmt='%d-%b-%y %H:%M:%S')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


def msg():
    logger.debug('   - [%s/msg()] -- This is a DEBUG --' % (os.path.basename(__file__)))
    logger.info('    - [%s/msg()] -- This is a INFO --' % (os.path.basename(__file__)))
    logger.warning(' - [%s/msg()] -- This is a WARNING --' % (os.path.basename(__file__)))
    logger.error('   - [%s/msg()] -- This is a ERROR --' % (os.path.basename(__file__)))
    logger.critical('- [%s/msg()] -- This is CRITICAL --' % (os.path.basename(__file__)))


if __name__ == '__main__':
    msg()
