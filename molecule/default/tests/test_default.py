import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_os_type(host):
    assert host.system_info.type == 'linux', 'Only the Linux operating system is supported!'


def test_cron_daemon(host):
    # Get the scheduler daemon name
    distribution = host.system_info.distribution
    if distribution == 'debian' or distribution == 'ubuntu':
        package_name = 'cron'
    elif distribution == 'centos' or distribution == 'redhat':
        package_name = 'cronie'
    else:
        raise ValueError('Unsupported distribution:', distribution)
    service_name = "crond"

    # Check if the system has cron daemon installed, enabled, up and running
    assert host.package(package_name).is_installed, 'The %s package should be installed.' % package_name
    assert host.service(service_name).is_running, 'The %s daemon should be running.' % service_name
    assert host.service(service_name).is_enabled, 'The %s service should be enabled.' % service_name


def test_logrotate_configuration(host):
    package_name = 'logrotate'
    assert host.package(package_name).is_installed, 'The %s package should be installed.' % package_name

    # Logratate configuration file must be in place
    configuration = host.file('/etc/logrotate.conf')
    assert configuration.exists, 'The logrotate.conf should exists'

    # Logrotate configuration file must load everything from logrotate.d
    assert configuration.contains('include /etc/logrotate.d'), 'Logrotate should read settings from logrotate.d!'

    # This file should present in the system
    application = host.file('/etc/logrotate.d/application')
    assert application.exists
    assert application.user == 'root'
    assert application.group == 'root'
    assert application.mode == 0o644

    # This file should be removed
    syslog = host.file('/etc/logrotate.d/syslog')
    assert not syslog.exists
