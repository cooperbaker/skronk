# skronk notes

&nbsp;
### sudo without password
---
- edit the sudoers file\
  ```$ sudo pico /etc/sudoers```

- add this line at the end\
  ```pi    ALL=(ALL) NOPASSWD: ALL```

&nbsp;
### update raspberry pi os
---
- upgrade to latest packages\
  ```$ sudo apt update```\
  ```$ sudo apt upgrade```

&nbsp;
### enable spi & i2c
---
- run raspberry pi config\
  ```$ sudo raspi-config```

- change settings
  - Interface Options &rarr; SPI &rarr; Yes
  - Interface Options &rarr; I2C &rarr; Yes

&nbsp;
### add python smbus api for i2c support
---
- install smbus package\
  ```$ sudo apt install python3-smbus```

&nbsp;
### create system skronk service
---
  - link skronk.service file\
    ```$ sudo ln -s /home/pi/skronk/skronk/skronk.service /etc/systemd/system/skronk.service```

  - enable the service at boot\
    ```$ sudo systemctl enable skronk.service```

  - commands:
    - display service status\
      ```$ sudo systemctl status skronk.service```

    - start now and always run at boot\
      ```$ sudo systemctl start skronk.service```

    - restart now and always run at boot\
      ```$ sudo systemctl restart skronk.service```

    - stop now and do not run again\
      ```$ sudo systemctl stop skronk.service```

&nbsp;
### cpu and memory monitor
---
- terminal-based process manager\
  ```$ sudo htop```
