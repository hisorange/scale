from os import system as run_shell_cmd

from scale.logger import create_logger

'''
Check for the required binaries and install the associated packages if they are not found.
'''


class DependencyManager:
    def __init__(self) -> None:
        self.logger = create_logger(self.__class__.__name__)
        self.aptUpdated = False

    # Check for missing packages and install them

    def prepare_necessities(self) -> None:
        self.logger.info('Verifying the required binaries')
        dependencies: dict = {
            "wg": ["wireguard-tools", "wireguard-dkms"],
        }

        for [bin, dep] in dependencies.items():
            self.logger.debug('Checking for [{}]'.format(bin))

            if not self.is_available(bin):
                self.install(dep)
            else:
                self.logger.warn('WHAT? {}'.format(self.is_available(bin)))

    # Check if the requested binary exists in the current environment
    def is_available(self, binary) -> bool:
        return run_shell_cmd('command -v {} > /dev/null'.format(binary)) == 0

    # Install the given packages
    def install(self, packages: list) -> None:
        self.logger.info('Installing packages [{}]'.format(packages))

        if self.aptUpdated == False:
            self.logger.info('Updating the package manager')
            run_shell_cmd('apt update')
            self.aptUpdated = True

        installed = run_shell_cmd(
            'apt install -y {}'.format(' '.join(packages))) == 0

        if not installed:
            raise EnvironmentError('Package installation failed!')
