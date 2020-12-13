# bluetooth-runner
Monitor Bluetooth events and run custom scripts

Code for this [answer][1].

Originally from [here][2] by Douglas6 written for Raspberry Pi.

[1]:http://askubuntu.com/a/644719/36556
[2]:https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=85101

Modified by [danmackinlay](https://github.com/danmackinlay) to adapt to the updated dbus APIs.
This script is now run too often (on *every* bluetooth state change not just mouse connection) but I can't be bothered trying to work out the updated flags so we'll call it done.
