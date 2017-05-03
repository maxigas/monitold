#!/usr/bin/python3

import os, yaml
import config

# TODO: Check if config repo is clean, quit if not

# print(sh.grep(sh.git.status(), "clean"))

def loaddir(name=config.server_info_dir):
    servers = []
    xdir = os.path.join(name, "servers")
    for x in os.listdir(xdir):
        ydir = os.path.join(xdir, x, "vms")
        for y in os.listdir(ydir):
            # DEBUG:
            # print(os.path.join(ydir, y))
            # DEBUG:
            # print(loadfile(os.path.join(ydir, y)))
            # print(loadfile(os.path.join(ydir, y))['details']['ip'])
            servers.append(loadfile(os.path.join(ydir, y)))
    return servers


def loadfile(name):
    # TODO: There is probably an os.path. function for extracting the file name:
    return {"name": name.split("/")[-1].split(".")[0], "details": yaml.safe_load(open(name, 'r'))}
