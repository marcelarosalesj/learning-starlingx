# Open Build Service learning

## OBS account
First you need to create an account in [openSUSE Build Service](https://build.opensuse.org/). Notice that if you want to use `osc` tool it will require this username and password, and that information will be stored in plain text in `~/.config/osc/oscrc`.

## osc commands
osc is the openSUSE build service command-line tool [here](https://en.opensuse.org/openSUSE:OSC). For Installing and Configuring, look [here](https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.osc.html)
```
# Checkout project creating a local copy
osc co home:marcelarosalesj

# Modify repositories metadata
osc meta -e prj home:marcelarosalesj

# Build for Ubuntu target
osc build xUbuntu_16.04 x86_64 fm-mgr_0.0-1.dsc

# Build for SUSE
osc build SLE_12_SP4 x86_64 fm-api.spec

# Useful parameters
osc build -p /tmp/foo -k /tmp/foo --no-verify SLE_12_SP4 x86_64 fm-api.spec
```

## Download on Demand (DoD) Feature  
"Please note that you need admin privileges in order to add DoD repositories to a buildservice instance." - [here](https://openbuildservice.org/2016/07/05/download-on-demand-feature/)  
How to add DoD [here](https://openbuildservice.org/help/manuals/obs-best-practices/cha.obs.best-practices.webuiusage.html#idm140458366672880)  
OBS Admin guide [here](https://openbuildservice.org/help/manuals/obs-admin-guide/)  
Kiwi wiki with information about repository configuration [here](https://opensource.suse.com/kiwi/building/build_in_buildservice.html)  
```
  <repository name="stx-cengn">
    <download arch="x86_64" url="http://mirror.starlingx.cengn.ca/mirror/starlingx/master/centos/latest_build/inputs/RPMS/" repotype="rpmmd"/>
    <download arch="x86_64" url="http://mirror.starlingx.cengn.ca/mirror/starlingx/master/centos/latest_build/outputs/RPMS/" repotype="rpmmd"/>
    <arch>x86_64</arch>
  </repository>
```


## openSUSE checks
openSUSE requires specfiles and code to follow standards, that's why OBS executes a set of [Packaging checks](https://en.opensuse.org/openSUSE:Packaging_checks). The github repository of those scripts is [here](https://github.com/openSUSE/brp-check-suse)

* init scripts should follow [LSB](https://wiki.debian.org/LSBInitScripts).
* more about [openSUSE Specfile guidelines](https://en.opensuse.org/openSUSE:Specfile_guidelines)


## OBS interface
You can add repositories to your OBS project by going to your project > Repositories > "Add Repository Path" > search and select the project.

## Local OBS
* [Setting up](https://openbuildservice.org/help/manuals/obs-best-practices/cha.obs.best-practices.localsetup.html)

## Spec files
A package may use the same spec file for CentOS, Red Hat and SUSE. If there are special cases for each, it can use this kind of logic:
```
%if 0%{?centos_version}
BuildRequires : librbd1-devel
%else

%if ! 0%{?rhel_version}
BuildRequires : librbd-devel
%endif

%endif

%if 0%{?suse_version}
BuildRequires : libnuma-devel
%else
BuildRequires : numactl-devel
%endif
```

## References
* [OBS Beginners Guide](https://openbuildservice.org/help/manuals/obs-beginners-guide/)
* [OBS Reference](https://openbuildservice.org/files/manuals/obs-reference-guide.pdf)
* [OBS Concepts](https://openbuildservice.org/help/manuals/obs-reference-guide/cha.obs.concepts.html)
* [Notes from OBS for StarlingX mail](http://lists.starlingx.io/pipermail/starlingx-discuss/2019-May/004435.html)
* [Docker Image with osc](https://hub.docker.com/r/jaltek/docker-opensuse-osc-client/)
* [spec-cleaner](https://github.com/openSUSE/spec-cleaner)
* [Tips and Tricks](https://en.opensuse.org/openSUSE:Build_Service_Tips_and_Tricks#link_and_aggregate)