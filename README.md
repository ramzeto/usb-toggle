# USB-Toggle

USB-Toggle is a Python script that allows to **software unplug** and **software plug** any USB device (including hubs).

According to [linux-usb.org](http://www.linux-usb.org/FAQ.html), the sysfs structures for USB are in **/sys/bus/usb/devices/**. The contents of this directory look something like this:

    1-0:1.0  2-0:1.0  3-0:1.0   3-3      3-4      4-0:1.0  usb3 
    1-1      2-1      3-10      3-3:1.0  3-4:1.0  usb1     usb4
    1-1:1.0  2-1:1.0  3-10:1.0  3-3:1.1  3-4:1.1  usb2

The directories that begin with **usb** refer to USB controllers (root hubs). All the other directories refer to USB devices and their interfaces.

Inside the directories that refer to an actual USB device, is a file named **product**. This file contains the description of the connected device.

For example, the directory **3-10** represents **bus-port**. So this USB device is connected to the bus **3** at the port **10**. To **software unplug** this **3-10** device, this directory name should be pushed to **/usb/drivers/usb/unbind**. To **software plug** it again, it has to be pushed to **/usb/drivers/usb/bind**.

**USB-Toggle** scans the **/sys/bus/usb/devices/** directory and shows the available devices, getting their names from the **product** file. The device status is gotten from the **bConfigurationValue** that is inside of the device directory. Plugs and unplugs the devices by pushing the device directory name to **/usb/drivers/usb/bind** and **/usb/drivers/usb/unbind**.

**USB-Toggle** uses GTK 3 as GUI. It does not use any custom styles, the appearance relies on the system theme. 

![USB-Toggle](https://www.dropbox.com/s/6gu4kc68ytqnleu/usb-toggle.png?raw=1)

Requires the proper permissions to be used.
