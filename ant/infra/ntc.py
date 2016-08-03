from ant import infra

import vagrant


class CMC(infra.FabricHost):

    def ssh_host_string(self):
        v = vagrant.Vagrant()
        return v.user_hostname_port(vm_name=self.hostname)

    def ssh_key(self):
        v = vagrant.Vagrant()
        return v.keyfile(vm_name=self.hostname)


class Slave(infra.Host):
    pass


class Infra(infra.Infra):

    def __init__(self):
        networks = [
            infra.Network('site', '10.0.2.0/24'),
            infra.Network('mgmt', '10.142.0.0/24')
        ]
        hosts = [
            CMC('cmc1', infra.HOST_TYPE_CMC, [infra.Port(networks[0], '10.0.2.15'), infra.Port(networks[1], '10.142.0.1')),
            Slave('slave1', infra.HOST_TYPE_SLAVE, infra.Port())
        ]
        super(Infra, self).__init__(hosts, networks)
