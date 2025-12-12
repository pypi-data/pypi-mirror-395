from dotmap import DotMap
import yaml
import logging

from . import exceptions

log = logging.getLogger('root')


def load_YAML(file_object):
    """
    Load a YAML configuration file into a DotMap.
    """
    try:
        config = yaml.safe_load(file_object)
    except yaml.composer.ComposerError as e:
        log.error(f"YAML composer error {e}")
        raise exceptions.ConfigurationError(e) from e
    except yaml.scanner.ScannerError as e:
        log.error(f"YAML scanner error {e}")
        raise exceptions.ConfigurationError(e) from e

    return DotMap(config, _dynamic=True)


def make_static(dm: DotMap):
    """
    Recursively remove _dynamic from a DotMap.
    """
    if isinstance(dm, DotMap):
        for k in dm._map:
            if isinstance(dm[k], DotMap):
                make_static(dm[k])
            if isinstance(dm[k], list):
                for item in dm[k]:
                    make_static(item)
            dm._dynamic = False
