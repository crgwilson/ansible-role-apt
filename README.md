# Ansible role: Apt

![Molecule Test](https://github.com/crgwilson/ansible-role-apt/workflows/Molecule%20Test/badge.svg)

Configure Apt & unattended-upgrades on Debian hosts

* Conditionally install apt-transport packages (only https for now)
* Configure Apt
* Install and configure unattended-upgrades


## Variables

Most variables map pretty closely to apt configs for more info on these refer to [the appropriate documentation](https://wiki.debian.org/AptConfiguration)

### `apt_preferences` - list(dict)

Configure apt preferences

Example:
```yaml
apt_preferences:
  - package: some-package
    pin: some.repo.url
    pin-priority: 500
```


### `apt_install_https_transport` - bool

Install `apt-transport-https` to support using https apt sources


### `apt_install_unattended_upgrades` - bool

Install and configure apt unattended upgrades


### `apt_packages` - list

Misc packages to install


## Testing

Testing for this project is setup using [Molecule](https://molecule.readthedocs.io/en/stable/) & [Docker](https://www.docker.com/).
Unit tests can be run using the below command:

```console
foo@bar:~$ molecule test --all
```
