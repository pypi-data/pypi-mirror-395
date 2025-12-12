##########################################################################
# Copyright (c) 2023-2024 Reinhard Caspary                               #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This module provides the function load_config() to read the default
# configuration parameters
#
# Parameter           | key
# --------------------+--------
# author name         | author
# author email        | email
# author ORCiD        | orcid
# author organization | organization
# server URL          | server
# server key          | key
#
# The values of these parameters are taken either from environment
# variables or a config file. Both options are optional. Data from the
# config file overides the environment variables.
#
# The name of the environment variable of key foo is DC_FOO.
#
# The name of the config file is "$HOME\scidata.cfg" (Windows) or
# "~/.scidata" (other OS). It is expected to be a text file. Leading and
# trailing white space is ignored. Lines starting with "#" are ignored.
# The parameters are taken from lines in the form "<key> = <value>".
# Optional white space before and after the equal sign is ignored. The
# keywords are case-insensitive.
#
##########################################################################

import os
import platform


def load_config(config_path: str = None, **kwargs) -> dict:
    """Get author identity and server configuration.

    This function uses kwargs, the scidata config file and environmental
    variables as sources for each parameter. The former sources
    overriding the latter ones.

    Users may use the result of this function to inject the author
    identity when building a new container:

    config = load_config(author="John Doe", email="john@doe.com")
    dc = Container(config=config)

    Args:
        str: Path of the config file. If this is None, the default file will
             be used. This filename is only required for testing.

        kwargs: Parameter values as keyword arguments.

    Returns:
        dict: A dictionary containing information strings with keys "author",\
              "email", "orcid", "organization", "server", "key".
    """

    # Initialize config dictionary
    config = {
        "author": "",
        "email": "",
        "orcid": "",
        "organization": "",
        "server": "",
        "key": "",
    }

    # Get default values from environment variables
    for key in config:
        name = "DC_%s" % key.upper()
        if name in os.environ:
            config[key] = os.environ[name].strip()

    # Path to scidata config file
    if not config_path:
        if platform.system() == "Windows":
            config_path = os.path.join(os.path.expanduser("~"), "scidata.cfg")
        else:
            config_path = os.path.join(os.path.expanduser("~"), ".scidata")

    # Get default values from config file
    if os.path.exists(config_path):
        with open(config_path, "r") as fp:
            for line in fp.readlines():
                line = line.strip()
                if line[:1] == "#":
                    continue
                line = line.split("=", 1)
                if len(line) < 2:
                    continue
                key = line[0].strip().lower()
                if key in config:
                    config[key] = line[1].strip()

    # Use keyword arguments
    for key in config:
        if key in kwargs:
            config[key] = kwargs[key].strip()

    # Return config dictionary
    return config
