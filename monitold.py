#!/usr/bin/python3
# monitold.py

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
