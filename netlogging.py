import json
import logging
import logging.config

with open('config.json', 'r') as f:
    logger_config = json.load(f)
logging.config.dictConfig(logger_config)
log = logging.getLogger(__name__)


# Standard logging test messages
log.debug('This is a debugging message.')
log.info('This is an information message.')
log.warning('This is a warning message.')
log.error('This is an error message.')
log.critical('You had better go and get mum!')


# Asynchronous 'burst' testing
for i in range(2):
    log.critical(f'Test message no flag: {i}')

print('PROGRAM EXECUTION CONTINUING')

for i in range(2, 4):
    log.critical(f'Test message no flag: {i}')


# Log an exception
try:
    x = 1 / 0
except ZeroDivisionError:
    log.exception("Turns out you can't divide by zero!")
