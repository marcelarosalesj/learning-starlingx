# MultiOS Maintenance Roadmap

## Current Tasks
* specfiles metal
* systemd metal

### specfiles metal

[Gerrit 681146](https://review.opendev.org/#/c/681146/)
* mtce-common - _Requires is not good enough_
* mtce-control
* mtce-compute
* mtce-storage - _Requires is not good enough_
* platform-kickstarts - _BuildRequires is not good enough_
* python-inventoryclient 

[Gerrit 680816](https://review.opendev.org/#/c/680816/)
* mtce

[Gerrit 680814](https://review.opendev.org/#/c/680814/)
* inventory

Blocked:
* pxe-network-installer - [depends on
  vmlinuz](https://opendev.org/starlingx/metal/src/branch/master/installer/pxe-network-installer/centos/pxe-network-installer.spec#L12)


To-do:
* Clean up openSUSE spec files `mtce-common`, `mtce-storage` and `platform-kickstarts`.
* Use this knowledge to clean CentOS spec files.

### systemd metal
Work in progress:
* mtce
    * hostw.service
    * lmon.service
    * hwclock.service
    * mtclog.service
    * mtcClient.service
    * config.service
    * hbsClient.service
    * goenabled.service
    * runservices.service
    * pmon.service
    * fsmon.service
    * hwmon.service
    * mtcalarm.service
* mtce-common
* mtce-control
    * hbsAgent.service
* mtce-compute
    * goenabled-worker.service
* mtce-storage
    * goenabled-storage.service
* kickstart
* inventory
    * Inventory-agent.service
    * Inventory-conductor.service
    * inventory-api.service
* python-inventory
* pxe-network-installer

To-do:
* Identify what services can be started, stopped and restarted after systemd changes ([these ones](https://github.com/marcelarosalesj/learning-starlingx/blob/master/systemd.md)) using Service Manager.


## New tasks
* document openSUSE enabling

### document openSUSE enabling
Previously some experiments were performed trying to enable Maintenance service on an openSUSE VM.

To-do:
* Document the experiments, findings and blocks.