# Maintenace enabling in openSUSE

## Identified work and updates

```
project: inventory
    package: inventory-1.0-lp151.7.1.x86_64.rpm
        service: Inventory-agent.service
        service: Inventory-conductor.service
        service: inventory-api.service
project: mtce
    package: libamon1-1.0-lp151.10.2.x86_64.rpm (184 KB) / this is pmon [SUCCESSFUL INSTALLATION]
        service: pmon.service - Missing /etc/platform/platform.conf
    package: mtce-1.0-lp151.10.2.x86_64.rpm (902 KB) [SUCCESSFUL INSTALLATION]
        service: fsmon.service - Missing /etc/platform/platform.conf
        service: goenabled.service - failed to write state file /var/run/.goenabled, but returns an exit status 0 if it runs with sudo
        service: hbsClient.service - Missing /etc/platform/platform.conf
        service: hwclock.service - exit status 0, but it has errors about /usr/lib/locale/en_US.UTF-8/ not existing, in openSUSE is /usr/lib/locale/en_US.utf8/
        service: mtcClient.service - Missing /etc/platform/platform.conf
        service: mtcalarm.service - Missing /etc/platform/platform.conf
        service: mtclog.service - Missing /etc/platform/platform.conf
        service: runservices.service - [pid  4831] read(0, "/etc/init.d/runservices: line 53: run-parts: command not found\n", 4096) = 63
    package: mtce-devel-1.0-lp151.10.2.x86_64.rpm (8.85 KB)
        service: N/A
    package: mtce-hostw-1.0-lp151.10.2.x86_64.rpm (108 KB)
        service: hostw.service
    package: mtce-hwmon-1.0-lp151.10.2.x86_64.rpm (342 KB)
        service: hwmon.service
    package: mtce-lmon-1.0-lp151.10.2.x86_64.rpm (170 KB)
        service: lmon.service
project: mtce-common
    package: mtce-common-devel-1.0-lp151.9.4.x86_64.rpm (1.9 MB)
        service: N/A
project: mtce-compute
    package: mtce-compute-1.0-lp151.7.1.noarch.rpm (18.2 KB)
        service: goenabled-worker.service
project: mtce-control
    package: mtce-control-1.0-lp151.7.1.noarch.rpm (18.1 KB)
        service: hbsAgent.service
project: mtce-storage
    package: mtce-storage-1.0-lp151.6.1.noarch.rpm (18.2 KB)
        service: goenabled-storage.service
project: python-inventoryclient
    package: python-inventoryclient-1.0-lp151.7.1.x86_64.rpm (96.7 KB)
        service: N/A
```

## Questions
* Who provides /etc/platform/platform.conf?
