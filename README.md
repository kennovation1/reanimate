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
