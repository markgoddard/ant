import abc

from fabric import api as fabric_api


class Host(object):
    """Abstract base class for hosts."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, hostname, type, networks):
        self._hostname = hostname
        self._type = type
        self._networks = networks

    @property
    def hostname(self):
        return self._hostname

    @property
    def type(self):
        return self._type

    @property
    def networks(self):
        return self._networks.copy()

    @abc.abstractmethod
    def execute(self, task, *args, **kwargs):
        pass

    @abc.abstractmethod
    def run(self, cmd, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        pass


class FabricHost(Host):

    def execute(self, task, *args, **kwargs):
        return fabric_api.execute(task, hosts=self.hostname, *args, **kwargs)

    def run(self, cmd, *args, **kwargs):
        return fabric_api.run(cmd, hosts=self.hostname, *args, **kwargs)

    def get(self, *args, **kwargs):
        return fabric_api.get(*args, hosts=self.hostname, **kwargs)

    def put(self, *args, **kwargs):
        return fabric_api.put(*args, hosts=self.hostname, **kwargs)


class Network(object):
    """Base class for networks."""

    def __init__(self, cidr):
        self._cidr = cidr

    @property
    def cidr(self):
        return self._cidr


class Infra(object):
    """A set of ANT test infrastructure."""

    def __init__(self):
        self.hosts = {}

    def get_hosts(self):
        return self.hosts.copy()

    def get_cmcs(self):
        return {name: host
                for name, host in self.hosts.items()
                if host.type == 'cmc'}

    def get_slaves(self):
        return {name: host
                for name, host in self.hosts.items()
                if host.type == 'slave'}

    def get_networks(self):
        return self.networks.copy()
