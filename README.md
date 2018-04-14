logrotate
=========

This role will setup logrotate and create additional rotation scripts.

The main role purpose is to:
- make sure logrotate is installed and enabled in cron;
- make it easy to configure logrotate - create per-application files in /etc/logrotate.d;
- handle log files for standard installations.

Requirements
------------

This role requires root access.

Role Variables
--------------

logrotate__files: A list of logrotate files and the directives to use for the rotation.

name    - The name of the file that goes into /etc/logrotate.d/.
absent  - If defined a file will be deleted from /etc/logrotate.d/ directory.
path    - A list of path patterns for the log rotation.
options - List of directives for logrotate, view the logrotate man page for specifics.
scripts - Dictionary of scripts for logrotate with format section_name: 'executed command'.

Dependencies
------------

None.

Example Playbook
----------------

You can invoke this role from a playbook or from an other role, declaring it as a dependency in the meta file. 
```
---
- hosts: all
  become: True
  roles:
    - role: logrotate
      logrotate__files:
        - name: glusterfs
          path:
            - /var/log/glusterfs/samples/*.samp
            - /var/log/glusterfs/bricks/*.log
          options:
            - daily
            - rotate 3
            - sharedscripts
            - missingok
            - compress
            - delaycompress
          scripts: 
            postrotate: systemctl reload glusterfs
...
```

License
-------

GNU General Public License v2.0

Author Information
------------------

Dmitrii Ageev <dageev@gmail.com>

