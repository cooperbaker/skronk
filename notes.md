# skronk notes

&nbsp;
### copy skronk library
---
- run the upload script\
  ```$ ./upload.command```

&nbsp;
### sudo without password
---
- edit the sudoers file\
  ```$ sudo visudo```

- add this line at the end\
  ```pi    ALL=(ALL) NOPASSWD: ALL```

&nbsp;
### update raspberry pi os
---
- upgrade to latest packages\
  ```$ sudo apt update && sudo apt upgrade```

&nbsp;
### enable spi & i2c
---
- run raspberry pi config\
  ```$ sudo raspi-config```

- change settings
  - Interface Options &rarr; SPI &rarr; Yes
  - Interface Options &rarr; I2C &rarr; Yes

&nbsp;
### add python smbus api
---
- install smbus package for i2c support\
  ```$ sudo apt install python3-smbus```

&nbsp;
### add pure data
---
- install with apt\
  ```$ sudo apt install puredata```

&nbsp;
### create system skronk service
---
  - link skronk.service file\
    ```$ sudo ln -s /home/pi/skronk/skronk/skronk.service /etc/systemd/system/skronk.service```

  - enable the service at boot\
    ```$ sudo systemctl enable skronk.service```

  - relevant commands:
    - enable and always run at boot\
      ```$ sudo systemctl enable skronk.service```

    - start now\
      ```$ sudo systemctl start skronk.service```

    - restart now\
      ```$ sudo systemctl restart skronk.service```

    - stop now\
      ```$ sudo systemctl stop skronk.service```

    - display status\
      ```$ sudo systemctl status skronk.service```

&nbsp;
### command-line skronk
---
- run skronk from the command line\
  ```$ cd /home/pi/skronk```

  ```$ sudo python3 skronk.py```
    - note: must stop skronk.service first

&nbsp;
### cpu and memory monitor
---
- terminal-based process manager\
  ```$ sudo htop```

&nbsp;
### alsa audio system
---
- list all devices\
  ```$ aplay -l```

- list device names only\
  ```$ aplay -l | awk -F \: '/,/{print $2}' | awk '{print $1}' | uniq```

- termainal-based mixer\
  ```$ alsamixer```


&nbsp;
### rnbo control ?
---
- start now\
  ```$ sudo systemctl start rnbooscquery.service```

- stop now\
  ```$ sudo systemctl stop rnbooscquery.service```

- display status\
  ```$ sudo systemctl status rnbooscquery.service```
