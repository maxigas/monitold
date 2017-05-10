#!/usr/bin/python3

from functools import reduce
from os import system
from os import path
import paramiko
import yamlrepo, linedump, config

def ping(ip):
    """Ping IP to see if it is reachable: Return True of False."""
    return True if system("ping -q -c 1 " + ip) is 0 else False

def isip(ip):
    """Accepts a string and returns a boolean specifying whether it is a valid IP."""
    octets = ip.split(".")
    return reduce(lambda x, y: x and int(y) < 256, octets) and len(octets) is 4

def cleanip(ip):
    """IPs from YAML can be single values or a list. Assumes we only need one IP."""
    return ip[0].split(" ")[0] if isinstance(ip, list) else ip.split(" ")[0]

def check(ip):
    """Checks host age and dumps the result to linedump."""

    def sniff_ssh_banner(ip):
        """Accepts an IP, returns an OpenSSH banner or None"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=ip,
                        port=22,
                        username="root",
                        password="root",
                        banner_timeout=2,
                        timeout=2)
        except:
            try:
                banner = ssh.get_transport().remote_version
                ssh.close()
                return banner
            except:
                ssh.close()
                return None

    def fingerprint_debian_release(banner):
        """Accepts a banner and tries fingerprinting based on the config file."""
        # DEBUG
        print("Banner:", banner)
        if isinstance(banner, str):
            for x in config.banners:
                # DEBUG: 
                # print("Comparing", banner, x)
                if banner and x['fingerprint'] in banner:
                    # DEBUG:
                    print("Release:", x['release'])
                    return x['release']
            return None
        else:
            return None

    def prepare_diagnosis(release):
        """Accepts a release number or status and returns the age of the host.
           * The age is either True for young; False for old.
           * If the release number is not a number, it pings the host.
           * If the host if up it returns "x", if the host is up None."""
        if isinstance(release, int):
            return release >= config.minimum_debian
        else:
            return None if ping(ip) else "x"

    assert isip(ip)
    print("Checking", ip)
    dump(prepare_diagnosis(fingerprint_debian_release(sniff_ssh_banner(ip))))


def getips():
    """Loads the IPs of hosts from a structured git repo of YAML files."""
    servers = yamlrepo.loaddir()
    ips = (server['details']['ip'] for server in servers)
    return [cleanip(ip) for ip in ips if ip]


def interactive(chars):
    """Accepts and prints a linedump, waits for commands, calls commands and then itself."""
    print()
    print("Type a printable ASCII char to see details or Enter to quit:")
    key = input('> ')
    print()
    if len(key) is 0:
        exit(0)
    else:
        print(yamlrepo.yaml.dump(yamlrepo.loaddir()[linedump.keypos(key)]))
    dump(chars)
    return interactive(chars)


if __name__ == "__main__":
    # INIT
    if path.exists('linedump.cache'):
        with open('linedump.cache') as f:
            chars = f.read()
        linedump.length = linedump.newlength(len(chars))
        dump = linedump.newlinedump()
        for x in chars:
            dump(x)
    else:
        ips = getips()
        linedump.length = linedump.newlength(len(ips))
        dump = linedump.newlinedump()
        for ip in ips:
            check(ip)
    interactive(dump())

