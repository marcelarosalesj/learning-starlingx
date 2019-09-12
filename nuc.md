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
--- a/sysinv/sysinv/sysinv/sysinv/api/controllers/v1/interface.py
+++ b/sysinv/sysinv/sysinv/sysinv/api/controllers/v1/interface.py
@@ -93,7 +93,7 @@ DATA_NETWORK_TYPES = [constants.NETWORK_TYPE_DATA]

 # Kernel allows max 15 chars. For Ethernet/AE, leave 5 for VLAN id.
 # For VLAN interfaces, support the full 15 char limit
-MAX_IFNAME_LEN = 10
+MAX_IFNAME_LEN = 15
 MAX_VLAN_ID_LEN = 5

 # Maximum number of characters in data network list
@@ -390,6 +390,7 @@ class InterfaceController(rest.RestController):
     @wsme_pecan.wsexpose(Interface, body=Interface)
     def post(self, interface):
         """Create a new interface."""
+        LOG.debug('Create a new interface')
         if self._from_ihosts:
             raise exception.OperationNotPermitted

@@ -698,6 +699,7 @@ def _check_interface_name(op, interface, ihost, from_profile=False):
     ifname = interface['ifname']
     iftype = interface['iftype']

+    LOG.debug('Begin interface name check')
     # Check for ifname that has only spaces
     if ifname and not ifname.strip():
         raise wsme.exc.ClientSideError(_("Interface name cannot be "
@@ -741,6 +743,7 @@ def _check_interface_name(op, interface, ihost, from_profile=False):
             continue
         if i.ifname == ifname:
             raise wsme.exc.ClientSideError(_("Interface Name {} must be unique.".format(ifname)))
+    LOG.debug('Pass interface name check')
     return interface

--- a/sysinv/sysinv/sysinv/sysinv/common/utils.py
+++ b/sysinv/sysinv/sysinv/sysinv/common/utils.py
@@ -508,9 +508,11 @@ def is_system_usable_block_device(pydev_device):
      o non permanent devices: USB stick
     :return bool: True if device can be used else False
     """
+    """
     if pydev_device.get("ID_BUS") == "usb":
         # Skip USB devices
         return False
+    """
     if pydev_device.get("DM_VG_NAME") or pydev_device.get("DM_LV_NAME"):
         # Skip LVM devices
         return False

--- a/sysinv/sysinv/sysinv/sysinv/conductor/manager.py
+++ b/sysinv/sysinv/sysinv/sysinv/conductor/manager.py
@@ -1742,7 +1742,7 @@ class ConductorManager(service.PeriodicService):
         :returns: pass or fail
         """

-        LOG.debug("Entering iport_update_by_ihost %s %s" %
+        LOG.info("Entering iport_update_by_ihost %s %s" %
                   (ihost_uuid, inic_dict_array))
         ihost_uuid.strip()
         try:
@@ -1772,8 +1772,9 @@ class ConductorManager(service.PeriodicService):
                 break

         cloning = False
+        add_usb_eth = 0
         for inic in inic_dict_array:
-            LOG.debug("Processing inic %s" % inic)
+            LOG.info("Processing inic %s" % inic)
             interface_exists = False
             networktype = None
             ifclass = None
@@ -1820,7 +1821,7 @@ class ConductorManager(service.PeriodicService):

                         # interface already exists so don't create another
                         interface_exists = True
-                        LOG.debug("interface mac match inic mac %s, inic_dict "
+                        LOG.info("interface mac match inic mac %s, inic_dict "
                                   "%s, interface_exists %s" %
                                   (interface['imac'], inic_dict,
                                    interface_exists))
@@ -1921,7 +1922,7 @@ class ConductorManager(service.PeriodicService):
                         }

                         try:
-                            LOG.debug("Attempting to create new interface %s" %
+                            LOG.info("Attempting to create new interface %s" %
                                       interface_dict)
                             new_interface = self.dbapi.iinterface_create(
                                 ihost['id'], interface_dict

@@ -1949,7 +1950,7 @@ class ConductorManager(service.PeriodicService):
                             pass  # at least create the port

                 try:
-                    LOG.debug("Attempting to create new port %s on host %s" %
+                    LOG.info("Attempting to create new port %s on host %s" %
                               (inic_dict, ihost['id']))

                     port = self.dbapi.ethernet_port_get_by_mac(inic['mac'])
@@ -1989,8 +1990,43 @@ class ConductorManager(service.PeriodicService):
                                                              None)

                     LOG.info("Attempting to create new port %s "
-                             "on host %s" % (inic_dict, ihost.uuid))
+                             "on host %s" % (port_dict, ihost.uuid))
                     port = self.dbapi.ethernet_port_create(ihost.uuid, port_dict)
+                    # if port_dict['iftype'] == 'ethernet' and add_usb_eth == 0:
+                    # if True:
+                    LOG.info("Add usb ethernet")
+                    add_usb_eth = 1
+                    interface_dict = {'forihostid': ihost['id'],
+                                      'ifname': 'enp0s20f0u3', # put the interface name
+                                      'imac': '00:24:9b:16:77:ce', # put the mac of your usb-ethernet
+                                      'imtu': 1500,
+                                      'iftype': 'ethernet',
+                                      'networktype': networktype
+                                      }
+                    LOG.info("interface: ")
+                    new_interface = self.dbapi.iinterface_create(
+                                         ihost['id'], interface_dict)
+                    LOG.info("Create interface success")
+                    # append to port attributes as well
+                    inic_dict.update(
+                            {'interface_id': new_interface['id'],
+                             'bootp': bootp
+                             })
+                    port_dict = inic_dict.copy()
+                    port_dict['mac'] = '00:24:9b:16:77:ce' # mac of usb-ethernet
+                    port_dict['pname'] = 'enp0s20f0u3' # interface name
+                    port_dict['pciaddr'] = '0000:00:0b.0'
+                    # port_dict['driver'] = 'aisx'
+                    # port_dict['uuid'] = 'f6cdbe3e-53ff-4886-b34c-13d01f704143'
+                    port_dict['name'] = port_dict.pop('pname', None)
+                    port_dict['namedisplay'] = port_dict.pop('pnamedisplay',
+                                                         None)
+                    LOG.info("Attempting to create usb port %s "
+                           "on host %s" % (port_dict, ihost.uuid))
+                    self.dbapi.ethernet_port_create(ihost.uuid, port_dict)
+                    LOG.info("Finish Add usb ethernet")
+                    LOG.info("Attempting to create new usb port %s "
+                             "on host %s" % (port_dict, ihost.uuid))


--- a/sysinv/sysinv/sysinv/sysinv/db/sqlalchemy/api.py
+++ b/sysinv/sysinv/sysinv/sysinv/db/sqlalchemy/api.py
@@ -1945,6 +1945,7 @@ class Connection(api.Connection):

     @objects.objectify(objects.ethernet_port)
     def ethernet_port_create(self, hostid, values):
+        LOG.info("ethernet_port_create is called")
         if utils.is_int_like(hostid):
             host = self.ihost_get(int(hostid))
         elif utils.is_uuid_like(hostid):
@@ -1958,13 +1959,18 @@ class Connection(api.Connection):

         if not values.get('uuid'):
             values['uuid'] = uuidutils.generate_uuid()
-
+        LOG.info("call EthernetPorts()")
         ethernet_port = models.EthernetPorts()
+        LOG.info("call ethernet update port")
         ethernet_port.update(values)
+        LOG.info("try _session_for_write")
         with _session_for_write() as session:
             try:
+                LOG.info("add ethernet port")
                 session.add(ethernet_port)
+                LOG.info("ethernet flush")
                 session.flush()
+                LOG.info("finish ethernet flush")
             except db_exc.DBDuplicateEntry:
                 LOG.error("Failed to add port %s (uuid: %s), port with MAC "
                           "address %s on host %s already exists" %
@@ -1974,7 +1980,8 @@ class Connection(api.Connection):
                            values['host_id']))
                 raise exception.MACAlreadyExists(mac=values['mac'],
                                                  host=values['host_id'])
-
+            except Exception as e:
+                LOG.exception('Error:%s', str(e))
             return self._ethernet_port_get(values['uuid'])
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
system host-disk-list controller-0 | awk '/\/dev\/sdb/{print $2}' | xargs -i system host-stor-add controller-0 {}
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

### Add internet access to StarlingX System
* Add DNS in `/etc/resolv.conf`
* Add `proxy=http://*****` in `/etc/yum.conf`
