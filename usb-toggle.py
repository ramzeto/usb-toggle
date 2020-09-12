import re
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):

    USB_DEVICES_PATH = "/sys/bus/usb/devices/"
    USB_BIND_PATH = "/sys/bus/usb/drivers/usb/bind"
    USB_UNBIND_PATH = "/sys/bus/usb/drivers/usb/unbind"

    def __init__(self):
        Gtk.Window.__init__(self, title = "USB-Toggle")

        grid = Gtk.Grid()
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        self.add(grid)

        # Headers
        column = 0
        headers = ["Unlock", "Device", "Toggle"]        
        for header in headers:
            header_label = Gtk.Label()
            header_label.set_markup("<b>" + header + "</b>")
            header_label.set_hexpand(True)
            header_label.set_justify(Gtk.Justification.CENTER)
            header_label.set_margin_bottom(10)
            grid.attach(header_label, column, 0, 1, 1)
            column = column + 1

        self.scan_devices(path = self.USB_DEVICES_PATH)

        # Devices
        row = 1
        for device in self.devices:
            unlock_check_button = Gtk.CheckButton()
            grid.attach(self.make_column(widget = unlock_check_button), 0, row, 1, 1)

            name_label = Gtk.Label()
            grid.attach(self.make_column(widget = name_label), 1, row, 1, 1)

            on_switch = Gtk.Switch()
            grid.attach(self.make_column(widget = on_switch), 2, row, 1, 1)

            DeviceGuiController(window = self, device = device, unlock_check_button = unlock_check_button, name_label = name_label, on_switch = on_switch)
            row = row + 1
        
        # Error
        self.error_label = Gtk.Label()
        self.error_label.set_hexpand(True)
        self.error_label.set_justify(Gtk.Justification.CENTER)
        self.error_label.set_label("")
        grid.attach(self.make_column(widget = self.error_label), 0, row, 3, 1)

    def make_column(self, widget):
        column_box = Gtk.Box()
        column_box.set_margin_start(10)
        column_box.set_margin_end(10)
        column_box.set_margin_top(10)
        column_box.set_margin_bottom(10)

        left_box = Gtk.Box()
        left_box.set_hexpand(True)
        column_box.pack_start(left_box, True, True, 0)

        column_box.pack_start(widget, False, False, 0)
        widget.set_hexpand(False)

        right_box = Gtk.Box()
        right_box.set_hexpand(True)
        column_box.pack_start(right_box, True, True, 0)

        return column_box



    def scan_devices(self, path):
        self.devices = []
        for entry in os.listdir(path):                
            entry_file_name = os.path.join(path, entry)
            if os.path.isdir(entry_file_name):
                product_file_name = os.path.join(entry_file_name, "product")
                if os.path.isfile(product_file_name):
                    self.devices.append(Device(path = entry_file_name))


    def show_error(self, error):
        self.error_label.set_label(error)



class DeviceGuiController:

    def __init__(self, window, device, unlock_check_button, name_label, on_switch):
        self.window = window
        self.device = device

        self.unlock_check_button = unlock_check_button
        self.unlock_check_button.connect("toggled", self.on_toggled_lock)

        self.name_label = name_label
        self.name_label.set_label(self.device.name)
        self.name_label.set_sensitive(False)

        self.on_switch = on_switch
        self.on_switch.set_sensitive(False)
        self.on_switch.set_active(self.device.on)
        self.on_switch.connect("state-set", self.on_activate)



    def on_toggled_lock(self, unlock_check_button):
        self.name_label.set_sensitive(unlock_check_button.get_active())
        self.on_switch.set_sensitive(unlock_check_button.get_active())



    def on_activate(self, on_switch, state):
        print(self.device.path)
        regex = re.compile(r'[\w\W]+/([\w\W]*)/product')
        matches = regex.match(os.path.join(self.device.path, "product"))
        if matches:
            device_mount_point = matches.group(1);
            status = 1000
            if state:
                status = os.system("echo '" + device_mount_point + "' | tee " + USB_BIND_PATH)
            else:
                status = os.system("echo '" + device_mount_point + "' | tee " + USB_UNBIND_PATH)

            if status != 0:
                self.window.show_error(error = "Failed to change the state of '" + self.device.name + "' (" + self.device.path + ").\nMake sure you have the required permissions.\nError " + str(status))
            else:
                self.window.show_error(error = "")

        return True




class Device:

    def __init__(self, path):
        self.path = path
        self.unlocked = False

        product_file_name = os.path.join(self.path, "product")
        fp = open(product_file_name, "r")
        self.name = fp.read().replace("\n", "")
        fp.close()

        configuration_value_file_name = os.path.join(self.path, "bConfigurationValue")
        fp = open(configuration_value_file_name, "r")
        configuration_value = fp.read()
        fp.close()

        if len(configuration_value) > 0 and int(configuration_value) > 0:
            self.on = True
        else:
            self.on = False

        



main_window = MainWindow()
main_window.connect("destroy", Gtk.main_quit)
main_window.set_position(Gtk.WindowPosition.CENTER)
main_window.show_all()
Gtk.main()
