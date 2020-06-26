import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('package', [
    ('apt-transport-https'),
    ('unattended-upgrades')
])
def test_default_packages(host, package):
    p = host.package(package)
    assert p.is_installed


def test_default_apt_config(host):
    f = host.file('/etc/apt/apt.conf.d/10recommends')

    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644

    assert f.contains('APT::Install-Recommends "1";')
    assert f.contains('APT:Install-Suggests "1";')


def test_default_periodic_config(host):
    f = host.file('/etc/apt/apt.conf.d/20auto_upgrades')

    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644

    assert f.contains('APT::Periodic::Update-Package-Lists "1";')
    assert f.contains('APT::Periodic::Download-Upgradeable-Packages "1";')
    assert f.contains('APT::Periodic::AutocleanInterval "7";')
    assert f.contains('APT::Periodic::Unattended-Upgrade "1";')


def test_default_unattended_upgrades_config(host):
    f = host.file('/etc/apt/apt.conf.d/50unattended-upgrades')

    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644

    origins = """
Unattended-Upgrade::Package-Blacklist {
  "${distro_id} ${distro_codename}-security";
  "${distro_id} ${distro_codename}-updates";
};
"""
    assert f.contains(origins)

    blacklist = """
Unattended-Upgrade::Package-Blacklist {
};
"""
    assert f.contains(blacklist)

    assert f.contains('Unattended-Upgrade::AutoFixInterruptedDpkg "false"')
    assert f.contains('Unattended-Upgrade::MinimalSteps "true"')
    assert f.contains('Unattended-Upgrade::InstallOnShutdown "false"')
    assert f.contains('Unattended-Upgrade::Remove-Unused-Dependencies "true"')
    assert f.contains(
        'Unattended-Upgrade::Remove-Unused-Kernel-Packages "true"'
    )
    assert f.contains('Unattended-Upgrade::Automatic-Reboot "true"')
    assert f.contains('Unattended-Upgrade::Automatic-Reboot-WithUsers "false"')
    assert f.contains('Unattended-Upgrade::Automatic-Reboot-Time "now"')
    assert f.contains('Unattended-Upgrade::SyslogEnable "false"')
    assert f.contains('Unattended-Upgrade::SyslogFacility "daemon"')
