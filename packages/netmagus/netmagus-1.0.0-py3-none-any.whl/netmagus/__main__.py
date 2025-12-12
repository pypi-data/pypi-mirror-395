import argparse
import codecs
import logging
import logging.config
import sys

import netmagus.session

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(process)d %(module)s %(levelname)s %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
}

if __name__ == "__main__":
    if sys.stdout.encoding != "UTF-8":
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout, "strict")
    # handle command line arguments
    parser = argparse.ArgumentParser(description="NetMagus NetworkOperation Script")
    parser.add_argument(
        "--script", help="name of the user Python file to execute", required=True
    )
    parser.add_argument(
        "--input-file",
        help="full path to a valid NetMagus NetworkOperation form JSON output file",
        required=True,
    )
    parser.add_argument(
        "--token",
        help="hash key sent by NetMagus to indicate the "
        "instance of this formula "
        "execution.  Used by formula to generate RPC "
        "targets and/or file names for "
        "responses",
        required=True,
    )
    parser.add_argument(
        "--loglevel", help="integer 0-5 indicating desired logging level", required=True
    )
    cli_args = parser.parse_args()

    _log_level_index = {
        0: 0,
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARN,
        4: logging.ERROR,
        5: logging.CRITICAL,
    }
    logging.config.dictConfig(LOGGING_CONFIG)
    log_level = _log_level_index[int(cli_args.loglevel)]
    log_suppress_level = _log_level_index[int(cli_args.loglevel) - 1]
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    if not log_level:
        logging.disable(logging.CRITICAL)
    else:
        logging.disable(log_suppress_level)
    logger.debug(f"CLI args received from NM backend: {cli_args}")
    netmagus.session.NetMagusSession(
        token=cli_args.token,
        input_file=cli_args.input_file,
        loglevel=log_level,
        script=cli_args.script,
    )._start()
