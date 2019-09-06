# StarlingX Simplex AIO on a NUC

Retrieved from old conversation and updated to StarlingX September, 2019.

## Requirements
* NUC
* [USB 3.0 to Gigabit Ethernet NIC Network Adapter](https://www.startech.com/Networking-IO/usb-network-adapters/USB-3-to-Gigabit-Ethernet-NIC-Network-Adapter~USB31000S)

## Steps
1. Kernel patch
2. Sysinv patch
3. Installing StarlingX

## 1. Kernel patch: Enable USB-Ethernet Driver
First of all, StarlingX Simplex requires two network interfaces, as presented in the [Bare metal All-in-one Simplex installation guide](https://docs.starlingx.io/deploy_install_guides/current/bare_metal_aio_simplex.html). The NUC has only one, so you need to use a USB-Ethernet adapter to get the second one. For it to be recognized by the OS, you need to patch the kernel so it uses the network USB drivers.

Start by having your base build environment working. Check my notes on that [here
](https://github.com/marcelarosalesj/learning-starlingx/blob/master/building/build-system-1.0.md).  

1. Delete kernel-std package
```
build-pkg --clean kernel
```

2. Patch the kernel to enable USB-Ethernet driver.
Normally this process is interactive: you open and edit a file, but in StarlingX build system that is not possible. You need to add your patch here  `starlingx/integ/src/branch/master/kernel/kernel-std/centos/patches`. For this guide, you can add these flags manually in this file `stx-integ/kernel/kernel-std/centos/patches/kernel-3.10.0-x86_64.config.tis_extra`.
```
-CONFIG_USB_USBNET=n
+CONFIG_USB_USBNET=y

-CONFIG_USB_PEGASUS=n
+CONFIG_USB_PEGASUS=y

+# Enable USB Ethernet
+CONFIG_USB_NET_DRIVERS=y
+CONFIG_USB_NET_AX8817X=y
+CONFIG_USB_NET_AX88179_178A=y
+CONFIG_NET_VENDORS_ATHEROS=y
```

3. Rebuild the kernel and installer files.
```
build-pkgs kernel --no-descendants
build-pkgs --installer
update-pxe-network-installer
```
The script `update-pxe-network-installer` will create new installer files (new-squashfs, new-vmlinuz and new-initrd). These will be located in `/localdisk/loadbuild/workstation/starlingx/pxe-network-installer/output/` in the Build System Terminal 2 (inside the container).
In order for them to be considered for the upcoming `build-iso`, you need to move/copy the files into the appropriate place, here `~/starlingx/mirror/CentOS/stx-installer` in the Build System Terminal 3. Then, rename them.
```
cp starlingx/workspace/localdisk/loadbuild/workstation/starlingx/pxe-network-installer/output/new-* ~/starlingx/mirror/CentOS/stx-installer/
cd ~/starlingx/mirror/CentOS/stx-installer
mv new-initrd.img initrd.img                                                                                               
mv new-squashfs.img squashfs.img
mv new-vmlinuz vmlinuz
```

4. Then, you can build the iso
```
build-iso
```

At this point, after an StarlingX installation, the Operating System will be able to see the second interface, but StarlingX System Inventory won't.
