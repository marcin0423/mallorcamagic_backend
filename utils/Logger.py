import logging
import os
from django.conf import settings

# Logging level
__LOGGING_LEVEL = logging.DEBUG


# Logging utilities
REDIRECT_IO = True
log = logging.getLogger('__main__')
log.setLevel(__LOGGING_LEVEL)
h = logging.StreamHandler()
h.setFormatter(logging.Formatter('%(levelname)s: [%(asctime)s] %(filename)s:%(funcName)s(%(lineno)d): %(message)s',
                                 datefmt='%d-%b-%y %S:%M:%H'))
log.addHandler(h)

if REDIRECT_IO:
    try:
        fd = os.open(settings.BASE_DIR / "logs.txt", os.O_RDWR | os.O_APPEND)
        os.dup2(fd, 1)
        os.dup2(fd, 2)
        if fd > 2:
            os.close(fd)
        log.debug('IO redirection is success!!')
    except Exception as e:
        log.error('IO redirection is failed: ' + str(e))
