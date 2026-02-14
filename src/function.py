import logging
from main import add

logger = logging.getLoggger("myapp")
result = add(1, 2)

logger.info(f"The result was {result}")

try:
    1 / 0
except ZeroDivisionError:
    logger.exceptio("A bad thing happened")