# StarlingX Simplex AIO on a NUC

Retrieved from old conversation and updated to StarlingX September, 2019.

## Requirements
* NUC NUC7i7BNH
* [USB 3.0 to Gigabit Ethernet NIC Network Adapter](https://www.startech.com/Networking-IO/usb-network-adapters/USB-3-to-Gigabit-Ethernet-NIC-Network-Adapter~USB31000S)

## Steps
1. Kernel patch
2. Sysinv patch
3. Installing and deploying StarlingX

## 1. Kernel patch: Enable USB-Ethernet Driver
First of all, StarlingX Simplex requires two network interfaces, as presented in the [Bare metal All-in-one Simplex installation guide](https://docs.starlingx.io/deploy_install_guides/current/bare_metal_aio_simplex.html). The NUC has only one, so you need to use a USB-Ethernet adapter to get the second one. For it to be recognized by the OS, you need to patch the kernel so it uses the network USB drivers. Start by having your base build environment working. 

1. Delete kernel-std package

Check my notes on that [here
](https://github.com/marcelarosalesj/learning-starlingx/blob/master/building/build-system-1.0.md). Then delete the kernel-std package.
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

## 2. Sysinv patches
The OS can see the USB-ethernet interface, but StarlingX doesn't. We need to patch Sysinv for specifically identify our adapter and interface.

1. Get the adapter MAC address

Connect the adapter and see with `ifconfig` its MAC address. In this case it is
```
enp0s20f0u11: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether 00:24:9b:16:77:ce  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

2. Modify sysinv to identify the USB/Ethernet adapter.
Add your adapter's interface name and MAC.
```
# TO-DO
```
Then, rebuild sysinv and the iso.
```
build-pkgs sysinv --clean
build-pkgs sysinv
build-iso
```
This ISO now has the kernel and sysinv patches.

## 3. Installing and deploying StarlingX
1. First, create the bootable USB.
```
sudo dd if=bootimage.iso of=/dev/sdc bs=1M status=progress
```
2. Install Simplex AIO in your NUC
```
- UEFI All-in-one Controller Configuration
- Graphical Console
```
After installing, the OS should be able to see the USB-Ethernet interface. You can check this by using `ip a`.

3. Run Ansible playbook.
You may need to configure `/home/sysadmin/localhost.yml` to have your proxies, dns and override the bootstrap playbook.
```
ansible-playbook /usr/share/ansible/stx-ansible/playbooks/bootstrap/bootstrap.yml
```
After this step, StarlingX should be able to see the USB-Ethernet interface. You can check this by using
```
source /etc/platform/openrc
system host-port-list controller-0
system host-if-list -a controller-0
```
Ansible playbook runs the system inventory, so if in the sysinv patch you logged messages, they should be here `/var/log/sysinv.log`.

4. Continue the configuration

Follow the steps from the [StarlingX/Containers/Installation
guide](https://wiki.openstack.org/w/index.php?title=StarlingX/Containers/Installation&oldid=170746#Configure_the_OAM_interface).

- Configure the OAM interface.  
In my case this is eno1
- Configure data interfaces.  
For this guide, we will only configure one data interface, it is the one enabled using the USB/Ethernet adapter: enp0s20f0u3
- Prepare the host for running the containerized services
- Setup partitions for Controller-0.  
This partitioning is needed for nova
- Configure Ceph for Controller-0.  
In this step, make sure you're not adding to Ceph the bootable USB you used for StarlingX installation. 
```
echo ">>> Add OSDs to primary tier"

system host-disk-list controller-0
system host-stor-add controller-0 </dev/sda uuid>
system host-stor-list controller-0
```
- Unlock the controller.  
After you unlock, the system will reboot. Then wait for 10 min for the system to complete provisioning.

**=== Guide incomplete ===**  
The system cannot be completly provisioned right now due to missing hardware requirements.
Check [here](https://docs.starlingx.io/deploy_install_guides/current/bare_metal_aio_simplex.html#hardware-requirements) that starlingx needs one SSD additional disk for Ceph OSD. Right now I don't have one, so I cannot complete the provision in my NUC.  
:(  
**========================**

## Network learning and debug

### Interface without IP
If your interface does not receive an IP by the DHCP, you can request it by creating this file `/etc/sysconfig/network-scripts/ifcfg-eth0` with
```
DEVICE=eth0
TYPE=Ethernet
ONBOOT=yes
BOOTPROTO=dhcp
```
content and restarting the service `sudo systemctl restart network`.


