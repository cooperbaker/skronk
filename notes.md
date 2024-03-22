### sudo without password
---
- edit the sudoers file\
<code>$ sudo pico /etc/sudoers</code>
- add this line at the end:\
<code>pi    ALL=(ALL) NOPASSWD: ALL</code>


### update raspberry pi os
---
<code>$ sudo apt upgrade</code>\
<code>$ sudo apt update</code>


### cpu and memory monitor
---
<code>$ htop</code>


### enable spi & i2c
---
<code>$ sudo raspi-config</code>
- Interface Options => SPI => Yes
- Interface Options => I2C => Yes


### add python smbus api for RPLCD
---
<code>$ sudo apt-get install python-smbus</code>


<!-- ### python virtual environment
---

- make\
<code>$ python3 -m venv skronk</code>
- activate\
<code>$ source skronk/bin/activate</code>
- deactivate\
<code>$ deactivate</code> -->