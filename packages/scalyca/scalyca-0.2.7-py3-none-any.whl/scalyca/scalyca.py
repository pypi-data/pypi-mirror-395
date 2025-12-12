import abc
import argparse
import dotmap
import logging
import sys

import schema

from . import scala
from . import exceptions
from . import configuration
from . import colour as c


log = logging.getLogger('root')


class Scalyca(scala.Scala, metaclass=abc.ABCMeta):
    """
    Simple Console Application with Logging, Yaml Configuration and Argparse

    Scalyca extends Scala with support for persistent configuration that is read from a YAML file.
    An extra mandatory argument `config` is added and the file is parsed automatically.
    Its contents are stored in a DotMap, so that they can be accessed more conveniently.

    In `override_configuration` it is possible to override values from the configuration file
    with command line arguments.
    """
    _app_name = 'Scalyca'
    _description = "Simple Configurable Application with Logging, Yaml file Configuration and Argparse"
    # Config validation schema, or None to skip validation
    _prog = "Scalyca"
    _schema: schema.Schema | None = None

    def _add_default_arguments(self):
        """
        Scalyca adds one mandatory argument to Scala's defaults: the path to the YAML config file.
        """
        super()._add_default_arguments()
        self.add_argument('config', type=argparse.FileType('r'), help="main configuration file")

    def _configure(self):
        try:
            self._load_configuration()
            self.override_configuration()
            self._lock_configuration()
            self._debug_configuration()
            self._validate_configuration()

        except exceptions.FatalError:
            log.critical(f"{c.script(self._app_name)} aborting during configuration")
            sys.exit(-1)

    def _load_configuration(self):
        """ Load the configuration from the specified file and convert it to a dynamic dotmap """
        raw = configuration.load_YAML(self.args.config)
        self.config = dotmap.DotMap(raw, _dynamic=True)
        log.debug(f"Configuration read from {c.path(self.args.config.name)}")

    def _lock_configuration(self):
        """
        Lock the configuration (set the DotMap's ``_dynamic`` to false recursively).
        """
        log.debug(f"Locking the configuration")
        configuration.make_static(self.config)

    def _debug_configuration(self):
        if self.args.debug:
            log.debug("Full config is")
            self.config.pprint()

    def _validate_configuration(self):
        if self._schema is None:
            log.debug("No config validation schema provided, skipping validation")
        else:
            log.debug("Validating the configuration")
            try:
                self._schema.validate(self.config)
            except schema.SchemaError as e:
                raise exceptions.ConfigurationError(e) from e
