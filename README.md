# Ansible modules to control statuscake.com tests

Currently, this module just pauses and unpauses the given test

## Installation

Use `ansible-galaxy` to install the `statuscake` role.

## Usage

The following example pauses the given `{{test_name}}`.

    ---
    - hosts: localhost
      roles:
        - {role: statuscake}  # Load the statuscake module from the role
      tasks:
        - statuscake:
            username: "{{statuscake_username}}"
            api_key: "{{statuscake_api_key}}"
            name: "{{test_name}}"
            pause: true # Either true to pause, or false to unpause

Note that `{{test_name}}` is the full name in status cake, and *not* the url used by the test.

## Versions

- __0.1__: Module to turn on/off test, need to package as a galaxy role for 1.0
- __1.0.0__: Have it packaged as an [Ansible Galaxy](https://galaxy.ansible.com) role.
