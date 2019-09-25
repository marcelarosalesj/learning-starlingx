# MultiOS Maintenance Roadmap

## Current tasks
* [wip] specfiles metal
* [wip] spec files integration with OBS
* [wip] StarlingX configuration on openSUSE
* [on hold] systemd metal
* [on hold] document openSUSE enabling

### specfiles metal
Clean up:
* mtce-common - _Requires is not good enough_
* mtce-storage - _Requires is not good enough_
* platform-kickstarts - _BuildRequires is not good enough_
* python-inventoryclient - _some python files set executable._

Blocked:
* pxe-network-installer - [depends on vmlinuz](https://opendev.org/starlingx/metal/src/branch/master/installer/pxe-network-installer/centos/pxe-network-installer.spec#L12)

Completed:
* opensuse specs merged:
    * mtce
    * inventory
    * mtce-common
    * mtce-control
    * mtce-compute
    * mtce-storage
    * platform-kickstarts
    * python-inventoryclient

### spec files integration with OBS
Work on the integration of metal spec files with OBS. Use sysinv as an example: [spec file](https://opendev.org/starlingx/config/src/branch/master/sysinv/sysinv/opensuse/sysinv.spec) and [service file](https://build.opensuse.org/package/view_file/Cloud:StarlingX:2.0/sysinv/_service?expand=1).

Metal integration with OBS:
* mtce
* inventory
* mtce-common
* mtce-control
* mtce-compute
* mtce-storage
* platform-kickstarts
* python-inventoryclient

Completed:
* TBD

### StarlingX configuration on openSUSE
Identify what ansible and puppet dependencies for configuring StarlingX are met on openSUSE and which ones are not.

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

## Completed tasks
* Document systemd convertion knowhow [here](https://github.com/marcelarosalesj/learning-starlingx/blob/master/systemd.md) and experimentation with pmon.
* Initial openSUSE spec files for metal in opendev - [Gerrit 681146](https://review.opendev.org/#/c/681146/), [Gerrit 680816](https://review.opendev.org/#/c/680816/), [Gerrit 680814](https://review.opendev.org/#/c/680814/)
