# Print all USB info available

import usb.core
import usb.util

devs = usb.core.find(find_all=True)
for dev in devs:
    print dev

