import os

from yaml import load, dump
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


from k3ssleipnir import logger


def load_yaml_manifest(manifest_file: str) -> tuple:
    file_content = ""
    with open(manifest_file, "r") as f:
        file_content = f.read()
    logger.info(f"Read {len(file_content)} bytes")

    config_sections = list()
    for data in yaml.load_all(file_content, Loader=Loader):
        config_sections.append(data)
    logger.info(f"Manifest contains {len(config_sections)} sections")

    return tuple(config_sections)


def dump_dict_to_yaml_file(data: dict, target_file: str):
    output = dump(data, Dumper=Dumper)
    logger.debug("YAML Data:\n----------\n{}\n----------".format(output))
    if os.path.exists(target_file) is True:
        os.unlink(target_file)
    logger.debug('Removed target file "{}"'.format(target_file))
    with open(target_file, "w") as f:
        f.write(output)
    logger.info("Written {} bytes to {}".format(len(output), target_file))
