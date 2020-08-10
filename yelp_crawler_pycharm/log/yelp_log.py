import logging
import datetime

Path = 'log/log{0}.log'
Format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Create a custom logger
logger = logging.getLogger(__name__)
dtime = datetime.datetime.now().strftime('%Y%m%d')
path = Path.replace('{0}',dtime)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(path)
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)