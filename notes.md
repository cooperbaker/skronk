### sudo without password
---
- edit the sudoers file\
<code>$ sudo pico /etc/sudoers</code>
- add this line at the end:\
<code>pi    ALL=(ALL) NOPASSWD: ALL</code>


### update raspberry pi os
---
<code>$ sudo apt update</code>\
<code>$ sudo apt upgrade</code>


### cpu and memory monitor
---
<code>$ sudo htop</code>


### enable spi & i2c
---
<code>$ sudo raspi-config</code>
- Interface Options => SPI => Yes
- Interface Options => I2C => Yes


### add python smbus api for i2c support
---
<code>$ sudo apt install python3-smbus</code>


### start skronk on boot
---
<code>$ sudo ln -s /home/pi/skronk/skronk/skronk.service /etc/systemd/system/skronk.service</code>\
<code>$ sudo systemctl enable skronk.service</code>