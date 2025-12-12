import logging
import os
import base64
import json
import shutil
import uuid
from pathlib import Path
import tempfile

from urllib.parse import urlparse, urlunparse
from typing import Optional, Tuple


logger = logging.getLogger("k3ssleipnir_deploy")


def validate_directory_for_file_exists(file: str) -> bool:
    directory = os.path.dirname(file)
    if os.path.exists(directory):
        return True
    return False


def _clear_previous_log_handlers():
    logger.handlers.clear()


def configure_logging(log_file: str, debug: bool = False):
    null_device = os.devnull
    final_log_file = null_device
    if validate_directory_for_file_exists(file=log_file) is True:
        final_log_file = log_file
    _clear_previous_log_handlers()
    logger.setLevel(logging.INFO)
    if debug is True:
        logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(filename=final_log_file)
    ch.setLevel(logging.INFO)
    if debug is True:
        ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s %(message)s"
    )
    if debug is True:
        formatter = logging.Formatter(
            "%(asctime)s %(pathname)s:%(funcName)s:%(lineno)d %(levelname)s %(message)s"
        )

    ch.setFormatter(formatter)
    logger.addHandler(ch)


def normal_base_64_encode(value) -> str:
    if isinstance(value, bytes) is False and isinstance(value, str) is True:
        value = value.encode("utf-8")
    return base64.b64encode(value).decode("utf-8")


###############################################################################
###                                                                         ###
###   CONVERSION FUNCTIONS                                                  ###
###                                                                         ###
###############################################################################


def conversion_json_to_dict(input_value):
    return json.loads(input_value)


CONVERSION_FUNCTIONS = {"json_to_dict": conversion_json_to_dict}


###############################################################################
###                                                                         ###
###   HELPER FUNCTIONS                                                      ###
###                                                                         ###
###############################################################################


def strip_url_creds(
    url_string: str,
) -> Tuple[Optional[str], Optional[str], str]:
    parsed_url = urlparse(url_string)
    username = parsed_url.username
    password = parsed_url.password
    if username is not None or password is not None:
        clean_netloc = parsed_url.hostname
        if parsed_url.port is not None:
            clean_netloc = "{}:{}".format(clean_netloc, parsed_url.port)
        cleaned_url_parts = parsed_url._replace(netloc=clean_netloc)
        cleaned_url = urlunparse(cleaned_url_parts)
    else:
        cleaned_url = url_string
    return (username, password, cleaned_url)


def delete_directory(dir: str) -> bool:
    try:
        os.remove(dir)
    except:
        try:
            shutil.rmtree(dir)
        except:  # pragma: no cover
            return False
    return True


def create_temp_directory() -> str:
    tmp_dir = "{}{}{}".format(tempfile.gettempdir(), os.sep, str(uuid.uuid4()))
    delete_directory(tmp_dir)  # Ensure it does not exist
    os.mkdir(tmp_dir)
    logger.info('Created directory "{}"'.format(tmp_dir))
    return tmp_dir


def create_dir(dir: str, with_parents: bool = True):
    path = Path(dir)
    path.mkdir(parents=with_parents, exist_ok=False)
    logger.info('Created directory "{}"'.format(dir))
