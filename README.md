# Betaflight Logo Replacer

This is a helper library written in Python3 for replacing the default logo with a custom one in an OSD font.

## Example usage

```python
from bflogoreplacer import replace_logo

with open("my-custom-font.mcm") as f:
    f.write(replace_logo("digital.mcm", "my-logo.png"))
```

See [`samples/`](samples/) directory for example input/output.

## Notes on the source files

* image has to be exactly 288px×72px
* background must be full green (#00ff00)
* must use white and black colors only
* it's better to use RGB mode than RGBA (alpha is ignored anyway)
* green areas will be transparent on the OSD
* default Betaflight fonts can be obtained from the configurator's repo:  
  https://github.com/betaflight/betaflight-configurator/tree/master/resources/osd

## Legal

This module is released under the GPLv3 license. Some code were taken and modified from here:  
https://github.com/Knifa/MAX7456-Font-Tools
