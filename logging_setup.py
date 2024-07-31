import logging

def Logging_Init():
    logger = logging.getLogger('my_logger')  # Use a specific logger name

    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(levelname)s : %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

# Initialize the logger once
logger = Logging_Init()
