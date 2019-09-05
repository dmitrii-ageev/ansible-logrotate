import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_os_type(host):
    assert host.system_info.type == 'linux', 'Only the Linux operating system is supported!'


def test_logrotate_configuration(host):
    package_name = 'logrotate'
    assert not host.package(package_name).is_installed, 'The %s package should be removed.' % package_name

    # Logratate configuration file must be deleted
    configuration = host.file('/etc/logrotate.conf')
    assert not configuration.exists, 'The logrotate.conf file should not exists.'

    # This directory should be removed
    settings = host.file('/etc/logrotate.d')
    assert not settings.exists
