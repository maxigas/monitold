#!/usr/bin/python3

from functools import reduce
import paramiko
import yamlrepo, linedump, config

def isip(ip):
    """Accepts a string and returns a boolean specifying whether it is a valid IP."""
    octets = ip.split(".")
    return reduce(lambda x, y: x and int(y) < 256, octets) and len(octets) is 4

def cleanip(ip):
    """IPs from YAML can be single values or a list. Assumes we only need one IP."""
    return ip[0].split(" ")[0] if isinstance(ip, list) else ip.split(" ")[0]

def check(ip):
    """Checks host age and dumps the result to linedump."""

    def banner(ip):
        """Accepts an IP and tries to return an OpenSSH banner."""
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
                banner = None
                ssh.close()
                return banner
            
    def release(banner):
        """Accepts a banner and tries fingerprinting based on the config file."""
        if isinstance(banner, str):
            for x in config.banners:
                # DEBUG: 
                # print("Comparing", banner, x)
                if banner and x['fingerprint'] in banner:
                    # DEBUG:
                    print("Release:", x['release'])
                    return x['release']
        else:
            return banner

    def diagnosis(release):
        """Accepts a release number or status and returns the age of the host.
           The age is either True for young; False for old; and None for unknown."""
        if isinstance(release, int):
            return release >= config.minimum_debian
        else:
            return release

    assert isip(ip)
    print("Checking", ip)
    dump(diagnosis(release(banner(ip))))

def getips():
     """Loads the IPs of hosts from a structured git repo of YAML files."""
    servers = yamlrepo.loaddir()
    ips = (server['details']['ip'] for server in servers)
    return [cleanip(ip) for ip in ips if ip]


if __name__ == "__main__":
    # INIT
    ips = getips()
    linedump.length = linedump.newlength(len(ips))
    dump = linedump.newlinedump()
    # ACTION
    for ip in ips:
        check(ip)
