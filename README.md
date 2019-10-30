# USB-Toggle

USB-Toggle is a simple Python script that allows binding and unbinding USB devices.

I made it because I have two gamepads connected to my PC, an XBox One controller and an arcade stick. And when I wanted to play a game that uses xinput via Proton or Wine, the arcade stick was always recognized as default. So instead of unplugging the arcade stick every time I played one of those games, I decided to make a script to unbind the device by software.

USB-Toggle uses GTK 3 as GUI and it requires the apropiate permissions to bind/unbind a device.


![USB-Toggle](https://www.dropbox.com/s/6gu4kc68ytqnleu/usb-toggle.png?dl=1)


In Ubuntu and Fedora, USB devices are in /sys/bus/usb/devices/. I do not know if this path is valid for other distros.


