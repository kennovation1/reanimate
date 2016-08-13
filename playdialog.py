import subprocess
import time

delay = 0.395
# 0.1 light behind music
# 0.2 light behind music
# 0.3 light behind music - close
# 0.35 light behind music - really close
# 0.38 light behind music - almost perfect
# 0.395 seems synched - perfect I think
'''
This weird configuration is because I don't know how to get aseqdump to
see the midi commands from timidity. Therefore I play the same file at about
the same time from aplaymidi. Since there is a lag on processing the seqdump
and then displaying it to the panel, I've stuffing in an artificial delay.
Of course this is brittle, but until I get get the commands out of timidity,
then this will have to do.
'''

'''
This doesn't work. ps looks okay, but no light activity is observed.
cmd = 'aseqdump -p 14:0 | python -u displaymidi.py'
p1 = subprocess.Popen(cmd, shell=True)
print 'aseqdump and displaymidi pid =', str(p1.pid)
time.sleep(1)
'''

p2 = subprocess.Popen(['/usr/bin/aplaymidi', '-p', '128:0', 'dialog.mid'])

time.sleep(delay)

p3 = subprocess.Popen(['/usr/bin/timidity', 'dialog.mid'])

print 'aplaymidi pid =', str(p2.pid)
print 'Timidity pid =', str(p3.pid)
