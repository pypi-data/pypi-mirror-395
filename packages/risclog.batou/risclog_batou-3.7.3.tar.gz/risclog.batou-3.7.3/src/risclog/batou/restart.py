import batou


class Restart(batou.component.Component):

    service = batou.component.Attribute()
    namevar = 'service'

    def verify(self):
        for name in ('testing', 'automotive', 'future'):
            if name in self.environment.name:
                raise batou.UpdateNeeded()

    def update(self):
        self.cmd(f'sudo systemctl restart {self.service}.service')
