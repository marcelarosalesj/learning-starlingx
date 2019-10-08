# Maintenace enabling in openSUSE

## Identified work and updates

```
project: inventory
    package: inventory-1.0-lp151.7.1.x86_64.rpm [SUCCESSFUL INSTALLATION]
        service: inventory-agent.service - This is not in the RPM (neither CentOS or openSUSE), I don't know why.
        service: inventory-conductor.service - files in /usr/lib64/ocf/resource.d/platform, /lib/heartbeat/ocf-shellfuncs: No such file or directory
        service: inventory-api.service - files in /usr/lib64/ocf/resource.d/platform, /lib/heartbeat/ocf-shellfuncs: No such file or directory
project: mtce
    package: libamon1-1.0-lp151.10.2.x86_64.rpm / this is pmon [SUCCESSFUL INSTALLATION]
        service: pmon.service - Missing /etc/platform/platform.conf
    package: mtce-1.0-lp151.10.2.x86_64.rpm [SUCCESSFUL INSTALLATION]
        service: fsmon.service - Missing /etc/platform/platform.conf
        service: goenabled.service - failed to write state file /var/run/.goenabled, but returns an exit status 0 if it runs with sudo
        service: hbsClient.service - Missing /etc/platform/platform.conf
        service: hwclock.service - exit status 0, but it has errors about /usr/lib/locale/en_US.UTF-8/ not existing, in openSUSE is /usr/lib/locale/en_US.utf8/
        service: mtcClient.service - Missing /etc/platform/platform.conf
        service: mtcalarm.service - Missing /etc/platform/platform.conf
        service: mtclog.service - Missing /etc/platform/platform.conf
        service: runservices.service - [pid  4831] read(0, "/etc/init.d/runservices: line 53: run-parts: command not found\n", 4096) = 63
    package: mtce-devel-1.0-lp151.10.2.x86_64.rpm [SUCCESSFUL INSTALLATION]
        service: N/A
    package: mtce-hostw-1.0-lp151.10.2.x86_64.rpm [SUCCESSFUL INSTALLATION]
        service: hostw.service - Missing /etc/platform/platform.conf
    package: mtce-hwmon-1.0-lp151.10.2.x86_64.rpm [SUCCESSFUL INSTALLATION]
        service: hwmon.service - Missing /etc/platform/platform.conf
    package: mtce-lmon-1.0-lp151.10.2.x86_64.rpm - [SUCCESSFUL INSTALLATION]
        service: lmon.service - Missing /etc/platform/platform.conf
project: mtce-common
    package: mtce-common-devel-1.0-lp151.9.4.x86_64.rpm [SUCCESSFUL INSTALLATION]
        service: N/A
project: mtce-compute
    package: mtce-compute-1.0-lp151.7.1.noarch.rpm [SUCCESSFUL INSTALLATION]
        service: goenabled-worker.service - failed to write /var/run/.goenabled_subf, but returns an exit status 0 if it runs with sudo
project: mtce-control
    package: mtce-control-1.0-lp151.7.1.noarch.rpm [SUCCESSFUL INSTALLATION]
        service: hbsAgent.service - Missing /etc/platform/platform.conf
project: mtce-storage
    package: mtce-storage-1.0-lp151.6.1.noarch.rpm [SUCCESSFUL INSTALLATION]
        service: goenabled-storage.service - return 0
project: python-inventoryclient
    package: python-inventoryclient-1.0-lp151.7.1.x86_64.rpm [SUCCESSFUL INSTALLATION]
        service: N/A
```

## Questions
* Who provides /etc/platform/platform.conf? ansible, stx-puppet and sysinv

## Learning
* StarlingX provisioning before maintenance can run

## References
* [[Starlingx-discuss] [MultiOS] Maintenance enabling on openSUSE first steps and errors](http://lists.starlingx.io/pipermail/starlingx-discuss/2019-October/006436.html)
