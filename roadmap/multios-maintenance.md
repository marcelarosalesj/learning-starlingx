# MultiOS Maintenance Roadmap

## Current tasks
* specfiles metal
* systemd metal
* document openSUSE enabling

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
* Wait for specs to be merged as they are.
* Then, start working on cleaning up openSUSE spec files `mtce-common`, `mtce-storage` and `platform-kickstarts`.

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
* Document pmon interaction dependencies with SM.

### document openSUSE enabling
Previously some experiments were performed trying to enable Maintenance service on an openSUSE VM.

To-do:
* Open bugs for enabling issues of each metal service. Start with pmon.

## New tasks
* TBD

### TBD

## Completed tasks
* Document systemd convertion knowhow [here](https://github.com/marcelarosalesj/learning-starlingx/blob/master/systemd.md) and experimentation with pmon.
