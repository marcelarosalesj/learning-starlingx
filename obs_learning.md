# OBS learning  

## osc commands
```
# Checkout content from upstream creating a local copy
osc co home:marcelarosalesj
# Modify repositories metadata
osc meta -e prj home:marcelarosalesj
# Build for ubuntu target
osc build xUbuntu_16.04 x86_64 fm-mgr_0.0-1.dsc
#

```

## Download on Demand (DoD) Feature  
* https://openbuildservice.org/2016/07/05/download-on-demand-feature/
  "Please note that you need admin privileges in order to add DoD repositories to a buildservice instance."
* https://openbuildservice.org/help/manuals/obs-reference-guide/cha.obs.concepts.html#concept_dod
* How to add DoD: https://openbuildservice.org/help/manuals/obs-best-practices/cha.obs.best-practices.webuiusage.html#idm140458366672880
* OBS Admin guide https://openbuildservice.org/help/manuals/obs-admin-guide/
* Cengn starlingx repository
```
  <repository name="stx-cengn">
    <download arch="x86_64" url="http://mirror.starlingx.cengn.ca/mirror/starlingx/master/centos/latest_build/inputs/RPMS/" repotype="rpmmd"/>
    <download arch="x86_64" url="http://mirror.starlingx.cengn.ca/mirror/starlingx/master/centos/latest_build/outputs/RPMS/" repotype="rpmmd"/>
    <arch>x86_64</arch>
  </repository>
```
* Kiwi wiki with information about repository configuration https://opensource.suse.com/kiwi/building/build_in_buildservice.html
