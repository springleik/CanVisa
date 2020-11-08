# CanVisa
This Python 3 script for Raspberry Pi exposes an SDO interface on CAN bus for Visa-enabled bench instruments.  This allows CANOpen measurement systems to incorporate Visa instuments into their measurement and control functions.  The example given here is a [Keithley](https://www.tek.com/tektronix-and-keithley-dc-power-supplies/keithley-2220-2230-2231-series) 2230 three-output power supply, connected to the RasPi via USB.  The CAN bus is similarly connected through a [Lawicel](https://www.can232.com/?m=201710) CANUSB dongle.  The CAN object dictionary is quite limited, including just enough SDOs to set and get voltage and current for the three outputs.  There is no need for a full-featured CANOpen library in this case, and all messages fit within a single CAN packet.  Access to the USB peripherals does require permission if you are running in Linux, so I created a simple udev rule for the Keithley like this:

```
SUBSYSTEM=="usb", ATTRS{idVendor}=="05e6", ATTRS{idProduct}=="2230", MODE:="0660", GROUP:="visa"
```

No permission needed if running on Windows but a different syntax is used to open the CAN bus, as shown in comments near the top of the script file.  Multiple instances of this script can run simultaneously on the RasPi, all using the same CAN interface, so long as each copy has a different CAN node number.  In this way several Visa instruments could be connected to CAN at the same time.
