import abc

from fabric import api as fabric_api


HOST_TYPE_CMC = 'cmc'
HOST_TYPE_SLAVE = 'slave'


class Host(object):
    """Abstract base class for hosts."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, hostname, type, ports):
        self._hostname = hostname
        self._type = type
        self._ports = {port.network.name: port for port in ports}

    @property
    def hostname(self):
        return self._hostname

    @property
    def type(self):
        return self._type

    @property
    def ports(self):
        return self._ports.copy()

    @property
    def networks(self):
        return {net_name: port.network for net_name, port in self._ports.items()}

    @abc.abstractmethod
    def execute(self, task, *args, **kwargs):
        pass

    @abc.abstractmethod
    def run(self, cmd, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def put(self, *args, **kwargs):
        pass


class FabricHost(Host):
    """Abstract base class for hosts for use with Fabric."""

    __metaclass__ = abc.ABCMeta

    def execute(self, task, *args, **kwargs):
        return fabric_api.execute(task, hosts=self.hostname, *args, **kwargs)

    def run(self, cmd, *args, **kwargs):
        return fabric_api.run(cmd, hosts=self.hostname, *args, **kwargs)

    def get(self, *args, **kwargs):
        return fabric_api.get(*args, hosts=self.hostname, **kwargs)

    def put(self, *args, **kwargs):
        return fabric_api.put(*args, hosts=self.hostname, **kwargs)

    @abc.abstractmethod
    def ssh_host_string(self):
        pass

    @abc.abstractmethod
    def ssh_key(self):
        pass


class Network(object):
    """Base class for networks."""

    def __init__(self, name, cidr):
        self._name = name
        self._cidr = cidr

    @property
    def name(self):
        return self._name

    @property
    def cidr(self):
        return self._cidr


class Port(object):

    def __init__(self, network, ip):
        self._network = network
        self._ip = ip

    @property
    def network(self):
        return self._network

    @property
    def ip(self):
        return self._ip


class Infra(object):
    """A set of ANT test infrastructure."""

    def __init__(self, hosts, networks):
        self._hosts = {host.hostname: host for host in hosts}
        self._networks = {network.name: network for network in networks}

    def get_hosts(self):
        return self._hosts.copy()

    def get_host(self, hostname):
        return self._hosts[hostname]

    def get_cmcs(self):
        return {name: host
                for name, host in self._hosts.items()
                if host.type == 'cmc'}

    def get_cmc(self, hostname=None):
        cmcs = self.get_cmcs()
        if hostname:
            return cmcs[hostname]
        return cmcs.values()[0]

    def get_slaves(self):
        return {name: host
                for name, host in self._hosts.items()
                if host.type == 'slave'}

    def get_slave(self, hostname=None):
        slaves = self.get_slaves()
        if hostname:
            return slaves[hostname]
        return slaves.values()[0]

    def get_networks(self):
        return self._networks.copy()

    def get_network(self, name):
        return self._networks[name]
