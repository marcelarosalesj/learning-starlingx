# Build System Troubleshooting

## Replacing efiboot.img
```
# If you get this error when executing build-iso
15:10:01 Cleaning repos: TisCentos7Distro local-installer local-rt local-std
15:10:01 Cleaning up everything
15:10:01 Maybe you want: rm -rf /var/tmp/yum-workstation-0MUXvi, to also free up space taken by orphaned data from
disabled or removed repos
15:10:01   Replacing the efiboot.img grub.cfg file with the Titanium Cloud one
15:10:01 losetup: /localdisk/loadbuild/workstation/starlingx/export/efiboot.img: failed to set up loop device: No such
file or directory
15:10:01   Error: failed sudo losetup command.
15:10:01 *** Error: update-efiboot-image script returned failure 1 ***

# Solve it by running this command
rm -rf /var/tmp/yum-workstation-0MUXvi
```

## Could not resolve build-info
```
# If you get
15:58:45 STR=OVMF OVMF-20150414-2.gitc9e5618.el7.noarch.rpm noarch/OVMF-20150414-2.gitc9e5618.el7.noarch.rpm
15:58:45 Installing PKG=OVMF PKG_FILE=OVMF-20150414-2.gitc9e5618.el7.noarch.rpm
PKG_REL_PATH=noarch/OVMF-20150414-2.gitc9e5618.el7.noarch.rpm
PKG_PATH=/localdisk/designer/workstation/starlingx/cgcs-root/cgcs-centos-repo/Binary/noarch/OVMF-20150414-2.gitc9e5618.el7.noarch.rpm
from repo TisCentos7Distro
15:58:45 Debug: Packages still unresolved:  
15:58:45 
15:58:48 Could not resolve packages: build-info
15:58:48 Error -- could not install all explicitly listed packages
15:58:48 Could not install dependencies

# You are missing build-info package
# Probably you did use the --no-build-info flag, so run build-pkgs again without it
```
