
def generate_hostnames(dcs, env, node_count, indexes, dev_flavors=None):
    hostnames = []

    for dc in dcs:
        for index in indexes:
            for i in range(1, node_count + 1):
                node = f"{i:02d}{index}"

                if env == "prd":
                    hostname = f"{dc}0-fbofd{node}-prd{dc}.prd.fndlsb.net"
                    hostnames.append(hostname)
                else:
                    for flavor in dev_flavors:
                        hostname = f"{dc}-fbofd{node}-{flavor}.dev.fndlsb.net"
                        hostnames.append(hostname)

    return hostnames