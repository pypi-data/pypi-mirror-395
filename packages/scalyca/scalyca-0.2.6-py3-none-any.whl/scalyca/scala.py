import abc
import argparse
import datetime
import logging

from . import colour as c
from . import exceptions
from . import logger

log = logger.setup_log('root', timefmt='%H:%M:%S')


class Scala(metaclass=abc.ABCMeta):
    """
    Scala: Simple Console Application with Logging and Argparse

    The main class of the framework that manages basic application metadata,
    setting up the logging module and parsing command-line arguments.
    It is intended for batch processing jobs and other non-interactive programs.

    Its primary purpose it to make parsing arguments straightforward and simple,
    and provide defaults for the `logging` module.
    Basic errors are also handled relatively gracefully.

    In order to use it fo your simple console application, you need to:

    0.  Set up `_description`, `_prog` and `_version` (optional)
    1.  Provide a body for ``add_arguments`` (optional).
        Several default arguments, like `--logfile` and `--debug` are added automatically.
    2.  Provide a body for `override_configuration`.
        More
        (for instance more complex argument checking that is not possible to do with `argparse`).
    3.  Provide a body for `initialize` (optional).
        Internal attributes (like processing the config and CLI arguments) should be done in this step.
        For instance, converting `datetime` objects to `astropy.Time`.
    4.  Provide a body for `main` (this one is required).
        The main body of your program should go there.
    5.  Provide a body for `finalize` (optional).
        Cleanup and output of a summary report should go there.
    """
    # Verbose description of the application
    _description = "Simple Configurable Application with Logging and Argparse"
    # Prog, a short name of the program that is shown in --help
    _prog = "Scala"
    # Program version, also shown in --help
    _version = "undefined"

    def __init__(self, **kwargs):
        """
        Optionally override the application name and description.

        prog:
            override the short application name
        description:
            override the short application description
        success_message:
            override the final success message
        abort_message:
            override the program crash message
        """
        self._ok = False
        self._started = datetime.datetime.now(datetime.UTC)
        self._description = kwargs.get('description', self._description)
        self._prog = kwargs.get('prog', self._prog)
        self._success_message = kwargs.get('success_message', f"{c.script(self._prog)} finished successfully")
        self._abort_message = kwargs.get('error_message', f"{c.script(self._prog)} aborted during runtime")

        self._argparser = argparse.ArgumentParser(
            prog=self._prog,
            description=self._description
        )

    def _initialize(self):
        log.info(f"{c.script(self._prog)} (version {self._version}) starting")
        self._add_default_arguments()
        self.add_arguments()
        self.args = self._argparser.parse_args()

        self._configure()
        self._override_configuration()
        self.initialize()

    def add_argument(self, *args, **kwargs):
        """
        Just a public wrapper so that we do not have to access _argparser directly.
        All arguments *args and **kwargs are directly passed to internal argparse.ArgumentParser.
        """
        self._argparser.add_argument(*args, **kwargs)

    def add_arguments(self):
        """ Override this in your Scala derivative to add custom arguments """

    def _add_default_arguments(self):
        """
        Add default arguments that are present in every instance of Scala.
        """
        self.add_argument('-l', '--logfile', type=argparse.FileType('w'), help="Write log to file")
        self.add_argument('-d', '--debug', action='store_true', help="Turn on verbose logging")

    def initialize(self):
        """ Custom initialization routines. Might remain empty. """

    def _configure(self):
        pass

    @abc.abstractmethod
    def main(self):
        """
        The main entry point of the program.
        Provide an implementation in your derivative of Scala.
        """

    def finalize(self):
        """ Override this in you Scala derivative to add custom finalization """

    def _override_configuration(self):
        self.override_configuration()
        log.setLevel(logging.DEBUG if self.args.debug else logging.INFO)
        log.debug(f"{c.script(self._prog)} debug mode on")

        if self.args.logfile:
            log.addHandler(logging.FileHandler(self.args.logfile.name))
            log.debug(f"Added log output {c.path(self.args.logfile.name)}")

    def override_configuration(self):
        """ Custom override hook for overriding the configuration """

    def run(self):
        try:
            self._initialize()
            self.main()
            self._ok = True
        except exceptions.PrerequisiteError as e:
            log.error(f"Terminating due to missing prerequisites: {e}")
            self._ok = False
        except exceptions.ConfigurationError as e:
            log.error(f"Terminating due to a configuration error: {e}")
            self._ok = False
        except KeyboardInterrupt:
            log.error(f"Interrupted by user")
            self._ok = False
        finally:
            self._finalize()
            run_time = datetime.datetime.now(datetime.UTC) - self._started
            if self._ok:
                log.info(f"{self._success_message} in {run_time}")
            else:
                log.critical(f"{self._abort_message} after {run_time}")

    def _finalize(self):
        self.finalize()
