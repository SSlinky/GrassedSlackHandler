import json
import logging
import logging.config

with open('config.json', 'r') as f:
    logger_config = json.load(f)
logging.config.dictConfig(logger_config)
log = logging.getLogger(__name__)


log.debug("debug message body")
log.warning("warning message body")
