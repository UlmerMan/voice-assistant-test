import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'phon.log',
    mode = 'a',
    maxBytes= 2000000,
    backupCount= 1,
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%d-%b-%y %H:%M:%S")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

while(True):
    logger.debug('test')