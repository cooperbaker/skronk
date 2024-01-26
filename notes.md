### sudo without password
---
edit the sudoers file <code>sudo pico /etc/sudoers</code>\
add this line at the end: <code>pi    ALL=(ALL) NOPASSWD: ALL</code>

### update raspberry pi os
---
<code>$ sudo apt upgrade</code>\
<code>$ sudo apt update</code>


### cpu and memory monitor
---
<code>$ htop</code>
