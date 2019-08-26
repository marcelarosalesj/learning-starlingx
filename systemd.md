# StarlingX Systemd

This notes are related to the story: [Systemd usage standardization of flock services](https://storyboard.openstack.org/#!/story/2006192)

## SysV Init Scripts to Systemd Quickstart
At least for StarlingX Maintenance, most services seem to be systemd standardized by doing this:

```
# Pmon example

# Modify service file
vi mtce/src/pmon/scripts/pmon.service

[Service]
-Type=forking
+Type=simple
-ExecStart=/etc/rc.d/init.d/pmon start
-ExecStop=/etc/rc.d/init.d/pmon stop
-ExecReload=/etc/rc.d/init.d/pmon reload
-PIDFile=/var/run/pmond.pid
+ExecStart=/usr/local/bin/pmond
KillMode=process

# Remove the init script
rm mtce/src/pmon/scripts/pmon

# Modify spec file to not install init script
vi mtce/centos/mtce.spec

+++ b/mtce/centos/mtce.spec
@@ -338,7 +338,6 @@ install -m 755 -p -D %{_buildsubdir}/scripts/hbsClient %{buildroot}%{_sysconfdir
 install -m 755 -p -D %{_buildsubdir}/hwmon/scripts/lsb/hwmon %{buildroot}%{_sysconfdir}/init.d/hwmon
 install -m 755 -p -D %{_buildsubdir}/fsmon/scripts/fsmon %{buildroot}%{_sysconfdir}/init.d/fsmon
 install -m 755 -p -D %{_buildsubdir}/scripts/mtclog %{buildroot}%{_sysconfdir}/init.d/mtclog
-install -m 755 -p -D %{_buildsubdir}/pmon/scripts/pmon %{buildroot}%{_sysconfdir}/init.d/pmon
 install -m 755 -p -D %{_buildsubdir}/lmon/scripts/lmon %{buildroot}%{_sysconfdir}/init.d/lmon
 install -m 755 -p -D %{_buildsubdir}/hostw/scripts/hostw %{buildroot}%{_sysconfdir}/init.d/hostw
 install -m 755 -p -D %{_buildsubdir}/alarm/scripts/mtcalarm.init %{buildroot}%{_sysconfdir}/init.d/mtcalarm
@@ -530,7 +529,6 @@ install -m 755 -d %{buildroot}/var/run
 %{_libdir}/libamon.so.1
 %{_libdir}/libamon.so
 
-%{_sysconfdir}/init.d/pmon
 %{local_bindir}/pmond
```
Note: as this pmon is the main program and doesn't fork, it's service `Type=` is `simple`.
* [systemd.service man page](https://manpages.debian.org/jessie/systemd/systemd.service.5.en.html)

## How to test this change?
You would need to rebuild the package you modified, and then rebuild the ISO. You can look 
[here
](https://github.com/marcelarosalesj/learning-starlingx/blob/master/building/build-system-1.0.md) to see my notes.

Then, you can use the automated-robot-suite that is in [starlingx test](https://opendev.org/starlingx/test.git) to install a Simplex configuration and run a Sanity test.
```
python runner.py --run-suite Setup --configuration 1 --environment virtual
sleep 600
python runner.py --run-suite Provision
sleep 600
python runner.py --run-suite Sanity-Test
```
Note: You need to have `bootimage.iso` and `stx-openstack.tgz` in automation-robot-suite directory for installation and
provision steps. Then, you need `cirros-0.4.0-x86_64-disk.qcow2` and `CentOS-7-x86_64-GenericCloud.qcow2` for sanity
test. All of that is explained in automated-robot-suite README.md.

## References
* [Converting sysvinit scripts to
  systemd](https://serverfault.com/questions/690155/whats-the-easiest-way-to-make-my-old-init-script-work-in-systemd)

* [systemd forking vs simple](https://superuser.com/questions/1274901/systemd-forking-vs-simple/1274913)
