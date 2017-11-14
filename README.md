reannz.logrotate
================

This role will install logrotate package, and run it as a service.

The main role purpose is to:
- make sure logrotate is installed and enabled in cron;
- make it easy to configure logrotate - create per-application files in /etc/logrotate.d;
- handle log files for standard installations.


Requirements
------------

Ubuntu 16 or CentOS 7.
This role supports RedHat 7 and Debian 8, 9 as well.

Role Variables
--------------

logrotate__files: A list of logrotate files and the directives to use for the rotation.

name    - The name of the file that goes into /etc/logrotate.d/.
absent  - If defined a file will be deleted from /etc/logrotate.d/ directory.
path    - A list of path patterns for the log rotation.
options - List of directives for logrotate, view the logrotate man page for specifics.
scripts - Dictionary of scripts for logrotate with format section_name: 'executed command'.

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

Dependencies
------------

None.

Example Playbook
----------------

You can invoke this role from the other one, declaring it as a dependency in the meta file: 
```
dependencies:
  - role: reannz.logrotate
    logrotate__files:
      - name: "application"
        path:
          - /var/log/application/*.log
        options:
          - weekly
          - rotate 4
          - compress
        scripts:
          postrotate: systemctl reload application > /dev/null

      - name: "test"
        absent: yes
```

License
-------

GNU General Public License v2.0

Author Information
------------------

Dmitrii Ageev <dmitrii.ageev@reannz.co.nz>

