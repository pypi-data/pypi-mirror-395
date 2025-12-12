import logging
import os
import sys

DEFAULT_LOGFILE = "/var/log/vmanage-agent.log"


def setup_logger(
    log_name: str = "vmanage-agent",
    log_file: str = DEFAULT_LOGFILE,
    log_level: int = logging.DEBUG,
):
    try:
        os.system("sudo touch " + log_file)
        os.system("sudo chmod 666 " + log_file)
    except Exception as e:  # noqa
        print(
            "Error creating log file. You probably don't have permission to write to /var/log. Please run with sudo."
        )
        sys.exit(-1)
    # create logger
    logger = logging.getLogger(name=log_name)
    logger.setLevel(log_level)

    # create a stream handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create a file handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)

    # create a logging format
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


log = setup_logger("vmanage-agent", "/var/log/vmanage-agent.log", logging.DEBUG)
