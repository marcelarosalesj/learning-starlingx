# StarlingX SimpleX Deployment

## Network and VM Creation

To deploy a virtual StarlingX Simplex host follow these steps. First, get StarlingX Tools.
```
git clone https://opendev.org/starlingx/tools.git
cd tools/deployment/libvirt
```

Somes files need to change so the script can work on Fedora:
1. On both `controller.xml` and `controller_allinone.xml`
```
@@ -7,7 +7,7 @@
     <partition>/machine</partition>
   </resource>
   <os>
-    <type arch='x86_64' machine='pc-q35-xenial'>hvm</type>
+    <type arch='x86_64' machine='pc'>hvm</type>
   </os>
   <features>
     <acpi/>
@@ -95,9 +95,5 @@
       <alias name='balloon0'/>
     </memballoon>
   </devices>
-  <seclabel type='dynamic' model='apparmor' relabel='yes'>
-    <label>libvirt-6afab2ba-0ed0-45cb-b1bd-985e211a48de</label>
-    <imagelabel>libvirt-6afab2ba-0ed0-45cb-b1bd-985e211a48de</imagelabel>
-  </seclabel>
```
2. Also, on `functions.sh` it may be useful to change all references to `/var/lib/libvirt/images` to a path in home.
```
@@ -94,20 +94,20 @@ create_controller() {
         fi
         sed -i -e "
             s,NAME,${CONTROLLER_NODE},
-            s,DISK0,/var/lib/libvirt/images/${CONTROLLER_NODE}-0.img,
-            s,DISK1,/var/lib/libvirt/images/${CONTROLLER_NODE}-1.img,
+            s,DISK0,/home/workstation/tools/deployment/libvirt/images/${CONTROLLER_NODE}-0.img,
+            s,DISK1,/home/workstation/tools/deployment/libvirt/images/${CONTROLLER_NODE}-1.img,
             s,%BR1%,${BRIDGE_INTERFACE}1,
```
3. From `setup_configuration.sh` remove 
```
-sudo virt-manager
```
Other problems I had at this point were related to qemu permissions, that was solve modifying `/etc/libvirt/qemu.conf`.

Well, then.
```
# Setup for StarlingX VM. This uses controller.xml to create an specific machine for starlingx, with 4 NIC, memory, etc.
./setup_configuration.sh -i bootimage.iso -c simplex
```
To configure the NAT for the VM:
```
# Remove stxbr1 interface
sudo brctl delif stxbr1 vnet0
sudo brctl delbr stxbr1
```
Create a `nat.xml` file with this content
```
<network>
	<name>default</name>
	<bridge name="stxbr1" stp="off"/>
	<forward mode="nat"/>
	<ip address="10.10.10.1" netmask="255.255.255.0">
	</ip>
</network>
```
^ This will configure stxbr1 as nat with that IP address.
```
# Use that configuration xml to create the NAT
sudo virsh net-define nat.xml
sudo virsh net-start default
# Add again the interface with the bridge
sudo brctl addif stxbr1 vnet0
# Ensure bridge and network interface is up.
sudo ip link set stxbr1 up
sudo ip link set vnet0 up
```

On the StarlingX host:
- Controller All in One
- Graphic
- Standard

The configure the StarlingX IP

```
# Give an IP to the Host
sudo ip addr add 10.10.10.3/24 dev ens3
sudo ip link set ens3 up
sudo ip route add default via 10.10.10.1
```

Finally, verify the NAT is working
```
ping 10.10.10.1
ping <another_pc_ip>
```

## Now, configure using ansible

https://wiki.openstack.org/wiki/StarlingX/Containers/Installation#Method_2:_Run_Ansible_bootstrap_playbook

