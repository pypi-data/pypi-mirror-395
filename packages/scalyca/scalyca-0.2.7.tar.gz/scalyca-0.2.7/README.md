This package aims to provide a simple common framework for console jobs in Python.
There is nothing really new about the whole approach and everything can be done
using existing tools and packages. SCALYCA just wraps it all together into a reusable
class that should be easy to extend for use in batch jobs or simple pipeline stages.

It is supposed to be very lightweight and easily integrable.
More complex tasks are probably better suited for custom solutions using the same modules.
The programs are not supposed to be interactive, everything has to be initialized
either from the command line or, in case of SCALYCA, also from a selectable configuration file.

## SCALA -- Simple Console Application with Logging and Argparse
The main class is called Scala. It has two main components:

-   Logging, primarily to `stdout` during the execution of the program.
    This is implemented with the `logging` module, using just a single logger.
-   Parsing and processing command line arguments, that configure the initial state of the application
    and tell it what and where should exactly be done. The tool for the job is `argparse`.

### SCALYCA -- Simple Console Application with Logging, YAML Configuration and Argparse
Scalyca is a subclass of Scala that adds persistent configuration
to the program, which is read from a `YAML` file during the initialization process,
then stored as a static `DotMap` from module `dotmap`.
This is similar to a Python dictionary except that it allows for dot access, which is much more legible.

All of the properties can be overridden from the command line.
The resulting object is accessible through the `config` variable of the class.

## Usage
Just extend the `Scala` class:

- Static attribute `app_name` sets the name of the application that will be displayed by `argparse`.
- Static attribute `description` sets the long description for `argparse`.
- In `add_arguments` you are supposed to add all arguments to the built-in `ArgumentParser`.
