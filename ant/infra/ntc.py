from ant import infra

import vagrant


class NTCCMC(infra.Host):

    def run(self, cmd, *args, **kwargs):
        pass


class NTCSlave(infra.Host):
    pass


class Infra(infra.Infra):
    pass
