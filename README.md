# Ansible modules to control statuscake.com tests

Currently, this module just pauses and unpauses the given test

## Installation

Right now, it needs to be installed by hand. At some point in the future,
I'll package this up properly into an ansible galaxy role, but for now
you'll have to roll (ha!) this into your ansible setup by hand, mostly
because we're stuck with ansible 1.9.3 and I don't want to do any packaging
work before we upgrade to 2.0.

For now, if your ansible top-level `.yaml` file is in `./ansible`, symlink the
`statuscake` directory here to `./ansible/roles/statuscake`.

## Usage

The following example pauses the given `{{test_name}}`.

    ---
    - hosts: localhost
      roles:
        - {role: statuscake}  # Load the statuscake module from the role
      tasks:
        - statuscake:
            username: {{statuscake_username}}
            api_key: {{statuscake_api_key}}
            name: {{test_name}}
            pause: true # Either true to pause, or false to unpause

Note that `{{test_name}}` is the full name in status cake, and *not* the url used by the test.

## Versions

- __0.1__: Module to turn on/off test, need to package as a galaxy role for 1.0
