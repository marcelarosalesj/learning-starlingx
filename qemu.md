# QEMU commands


## To create a bootable virtual machine
```
qemu-img create -f raw target.img 30G
qemu-system-x86_64 -enable-kvm -m 2048 -boot d -hda target.img -cdrom custom-ubuntu-16.04.6-desktop-amd64.iso
qemu-system-x86_64 -enable-kvm -m 2048 -hda target.img
```
