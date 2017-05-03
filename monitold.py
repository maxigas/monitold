#!/usr/bin/python3

import paramiko
from functools import reduce
import yamlrepo, linedump, config

def isip(ip):
    octets = ip.split(".")
    return reduce(lambda x, y: x and int(y) < 256, octets) and len(octets) is 4

def cleanip(ip):
    return ip[0].split(" ")[0] if isinstance(ip, list) else ip.split(" ")[0]

def hosthealth(ip):
    """Checks host health with nmap and dumps the result to linedump."""

    def banner(ip):
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

    def judge(release):
        if isinstance(release, int):
            return release >= config.minimum_debian
        else:
            return release

    assert isip(ip)
    print("Checking", ip)
    dump(judge(release(banner(ip))))

def getips():
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
        hosthealth(ip)
