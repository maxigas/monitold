#!/usr/bin/python3
# yamlrepo.py

import os, yaml
import config

# TODO: Check if config repo is clean, quit if not

def loaddir(name=config.server_info_dir):
    """Accepts a path or takes from the config file, returns YAML objects of VMs."""
    servers = []
    xdir = os.path.join(name, "servers")
    for x in os.listdir(xdir):
        ydir = os.path.join(xdir, x, "vms")
        for y in os.listdir(ydir):
            servers.append(loadfile(os.path.join(ydir, y)))
    return servers


def loadfile(name):
    """Accepts a file name string and returns a tuple of basename and YAML."""
    # TODO: There is probably an os.path. function for extracting the file name:
    return {"name": name.split("/")[-1].split(".")[0], "details": yaml.safe_load(open(name, 'r'))}
