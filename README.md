# Raw notes for now

## Key files
* Operating the panel
  * auxcontrol.py - Main application to operate Auxiliary Control panel. Usage: python auxcontrol.py
    * panel_config.py - Describes the specifics of the Auxiliary Control Panel and the actions used by auxcontrol.py
    * digit_in.py - Used by auxcontrol.py. Run by itself tests all switch inputs
    * analog_in.py - Used by auxcontrol.py. Run by itself tests all analog inputs (pots and switches using ADC)
    * pacdrive.py - Driver layer for PacDrives to control lamps. Contains higher level functions to manage the state and mappings for the panel. Ideally these higher level functions should be factored out to their own module, but I've run out of time on this project and this is good enough for a weekend hack for now. If I ever use PacDrives in another project, then I should refactor appropriately (which will require changes to auxcontrol.py, testaux.py, displaymidi.py).

* Playing the Close Encounters of the Third Kind dialog
  * displaymidi.py - Reads MIDI events from aseqdump and drives lamps on panel in response. See header for usage.
    * Usage: aseqdump -p 14:0 | python -u displaymidi.py (in a separate window)
  * playdialog.py - Starts playing dialog.mid audio and MIDI stream and tries to keep sync between the two.
    * Usage: python playdialog.py (after displaymidi.py has been started)

* testaux.py - Debug utiity to manipulate lamps on the panel. Usage: python testaux.py

* Other files
  * colors.py - utility ASCII color codes
  * printAllUSBInfo.py - utility to print info about all connected USB devices
  * spitest.py - Originally used to debug the SPI interface and the ADC. Replaced by analog_in.py
  * readsw.py - Originally used to debug reading the RPi GPIO and reading switch states. Replaced by digitial_in.py

# Git notes:
```
git remote add origin https://github.com/kennovation1/reanimate.git
Since I didn't set up with ssh initially:
git remote set-url origin git@github.com:kennovation1/reanimate.git
git push -u origin master

See below for ssh key set up
```

## TODOs
- [ ] Use pots to control flash or chase rate on some lamps or warning lamps in auxcontrol.py
- [ ] Add a license file (what type?)
- [ ] Get linear power supply for about 4 amps or gang my current power supplies in parallel
- [ ] Better sync midi to lamps. If I had more time, I'd like to have a less kludgy way of playing midi audio and driving displaymidi.py so that the audio and lamps are properly synched.
- [ ] Clean up some of the lamp and pacdrive code factoring
- [ ] Add action handler type to execute a subprocess.popen() so that I can execute arbitrary code?
- [ ] Make video and stills (and put in album) and share with Mark C, Bobby E, etc.
- [ ] Share videos with Mark, Bobby, work
- [ ] Make limit cable for legs
- [ ] Add feet to legs

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
On Mac:
ssh-keygen -t rsa
cp id_rsa.pub authorized_keys
Copy private file to Mac ~/.ssh/rpi
chmod 400 rpi
From Mac: ssh -i ~/.ssh/rpi pi@192.168.1.13
Add the following to Mac .bash_profile
alias sshrpi='ssh -i ~/.ssh/rpi pi@192.168.1.13'
alias scprpi='scp -i ~/.ssh/rpi'

On RPi:
ssh-keygen -t rsa -b 4096 -C "kenrobbins@ieee.org for GitHub"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
Add public key to github account

mkdir reanimate
cd reanimate
git init
On Mac, add to .bash_profile:
alias sshrpi='ssh -i ~/.ssh/rpi pi@192.168.1.13'
alias scprpi='scp -i ~/.ssh/rpi'

On RPi added to .bashrc:
alias l='ls -FC'
alias ll='ls -l'
alias la='ls -la'
alias pu='pushd .'
alias po='popd'
alias s='more'
alias j='jobs'
alias hd='hexdump -C'
alias lp='ls -FC *.py'
alias gs='git status'

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
cd ~/reanimate
git clone git://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install
```

### PacDrive
```
cd ~/reanimate
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

### Midi
I did install things, but ended up only needing preinstalled software. See CloseEncounters for various notes.

