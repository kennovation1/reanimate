# First upload - everything is a TODO
For now, this is just a dump of files.

I need to delete cruft and organize what I've got.

Key files are:
* testaux.py, pacdrive.py - Drives lamps
  * Need to verify all lamps and wire 28V to all
  * Need to replace more bulbs
* readsw.py  - Reads all switches wired to RPi GPIO
  * All switches now work
* spitest.py - Reads ADC for R1-R4, A3, A4, S1, S2, S3
  * All analog inputs now work

# Git notes:
```
git remote add origin https://github.com/kennovation1/reanimate.git
git push -u origin master
```

## TODOs
- [ ] Add a license file (what type?)
- [ ] Delete junk files that are no longer needed
- [ ] Create a sane directory structure and file naming
- [ ] Create proper packages that are separated from application code 
- [ ] *** Something is wrong with board. Passing board 2 for updatePin only updates board 1. Update all works.
- [ ] Add EXPECTED_BOARDS in addition to MAX_BOARDS?
- [ ] Put mapping into a json file

### RPi setup
* Installed NOOBS to 16 GB microSD card
* Installed Raspbian to RPi3
* Set up WiFi UI via menu (top bar)
* Set up preferences (keyboard, timezone, etc.) via UI menu
* ifconfig to find IP
#### STATIC IP
    To set a static IP, I went to the router's advanced setting, IP address distribution and found
    device for RPi and clicked box that said make this static. Therefore the address is statically 
    192.168.1.13 now. No need to do anything else. One router screen now shows static, but another shows
    dynamic. I'm not sure if that's a problem or just a refresh issue.

ssh pi@192.168.1.13
password: raspberry

### General Linux environment set up
```
ssh-keygen -t rsa
cp id_rsa.pub authorized_keys
Copy private file to Mac ~/.ssh/rpi
chmod 400 rpi
From Mac: ssh -i ~/.ssh/rpi pi@192.168.1.13
Add the following to Mac .bash_profile
alias sshrpi='ssh -i ~/.ssh/rpi pi@192.168.1.13'
alias scprpi='scp -i ~/.ssh/rpi'

mkdir ken
cd ken
mkdir pacdrive
cd pacdrive
# Don't do this: mkvirtualenv pacdrive
# Don't do this: workon pacdrive
git init
On Mac, add to .bash_profile:
alias sshrpi='ssh -i ~/.ssh/rpi pi@192.168.1.13'
alias scprpi='scp -i ~/.ssh/rpi'
On RPi added to .bashrc:
# KLR Added
alias l='ls -FC'
alias ll='ls -l'
alias la='ls -la'
alias pu='pushd .'
alias po='popd'
alias s='more'
alias j='jobs'
alias hd='hexdump -C'
alias lp='ls -FC *.py'

Add to ~/.vimrc:
syntax on
filetype indent plugin on
set modeline
:set tabstop=8 expandtab shiftwidth=4 softtabstop=4
```

### Get required packages
```
sudo apt-get update
sudo apt-get install python-dev 
sudo apt-get install vim
```

### Virtualenv
* Use root installs. Don't use virtualenv.
* These are notes, just in case.
```
# sudo pip install virtualenvwrapper
# In ~/.bashrc, add:
# export WORKON_HOME=$HOME/.virtualenvs
# export PROJECT_HOME=$HOME/Devel
# source /usr/local/bin/virtualenvwrapper.sh
```

### USB
* http://walac.github.io/pyusb/
```
sudo pip install pyusb
```

### GPIO
Folling is where the /sys/class/gpio interface manipulations are defined
https://sites.google.com/site/semilleroadt/raspberry-pi-tutorials/gpio
Pointers to how to figure out rpio code:
https://www.raspberrypi.org/forums/viewtopic.php?&t=34746
RPi.GPIO basic doc on sourceforge:
https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
```
sudo pip install rpi.gpio
```

### SPI
```
http://raspberrypi-aa.github.io/session3/spi.html
This doesn't quite work yet since lsmod | grep spi shows nothing...
Well, spitest.py is working fine. Come back and review this.
cd ~/ken
git clone git://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install
```

### PacDrive
```
cd ~/ken/pacdrive
To dump USB information
    python printAllUSBInfo.py
```

From Andy at Ultimarc
    The USB data format is very simple, it appears as a standard HID compliant device and responds to
    a 4 byte data packet. Only the two least significant bytes are used, which are a bitmap of the LEDs.

I ordered 4 Pac-Drives and requested that they be pre-configured to default outputs to off (normally defaults
to on). Andy will also set unique IDs for each since they'll be on the same bus.

The IDs appear in the bcdDevice. All other values are the same.
    bcdDevice              :    0x1 Device 0.01
    bcdDevice              :    0x2 Device 0.02
    bcdDevice              :    0x3 Device 0.03
    bcdDevice              :    0x4 Device 0.04

iSerialNumber looks different from lsusb -v, but the value is really just 0x3. I think that the other stuff
(1-4) is added by lsusb and not part of the data (based on my printing our dev.iSerialNumber).
    iSerialNumber          :    0x3 1
    iSerialNumber          :    0x3 2
    iSerialNumber          :    0x3 3
    iSerialNumber          :    0x3 4
    
To allow (user space) access to the USB device:
```
sudo cp 21-ultimarc.rules /etc/udev/rules.d/
sudo reboot
('sudo udevadm trigger' doesn't seem to work, so a reboot is best)
lsusb
sudo lsusb -v

Example dump for device 0x4:
DEVICE ID d209:1500 on Bus 001 Address 007 =================
 bLength                :   0x12 (18 bytes)
 bDescriptorType        :    0x1 Device
 bcdUSB                 :  0x200 USB 2.0
 bDeviceClass           :    0x0 Specified at interface
 bDeviceSubClass        :    0x0
 bDeviceProtocol        :    0x0
 bMaxPacketSize0        :    0x8 (8 bytes)
 idVendor               : 0xd209
 idProduct              : 0x1500
 bcdDevice              :    0x4 Device 0.04
 iManufacturer          :    0x1 Ultimarc
 iProduct               :    0x2 LED Controller
 iSerialNumber          :    0x3 4
 bNumConfigurations     :    0x1
  CONFIGURATION 1: 500 mA ==================================
   bLength              :    0x9 (9 bytes)
   bDescriptorType      :    0x2 Configuration
   wTotalLength         :   0x22 (34 bytes)
   bNumInterfaces       :    0x1
   bConfigurationValue  :    0x1
   iConfiguration       :    0x0 
   bmAttributes         :   0x80 Bus Powered
   bMaxPower            :   0xfa (500 mA)
    INTERFACE 0: Human Interface Device ====================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x0
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x1
     bInterfaceClass    :    0x3 Human Interface Device
     bInterfaceSubClass :    0x0
     bInterfaceProtocol :    0x0
     iInterface         :    0x0 
      ENDPOINT 0x81: Interrupt IN ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x81 IN
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :    0x8 (8 bytes)
       bInterval        :    0xa
```
