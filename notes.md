# skronk notes

&nbsp;
### get git
---
- run the git install command\
  ```$ sudo apt install git```

&nbsp;
### git the skronk library
---
- run the git clone command\
  ```$ git clone --depth 1 https://github.com/cooperbaker/skronk```

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
- stop skronk service\
  ```$ sudo systemctl stop skronk.service```

- run skronk by hand\
  ```$ cd ~/skronk```

  ```$ sudo python3 skronk.py```


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


---

Download the latest Cycling 74 RNBO Raspberry Pi image\
[https://rnbo.cycling74.com/resources#raspberry-pi-images](https://rnbo.cycling74.com/resources#raspberry-pi-images)

Unzip the image

Flash to SD card using Raspberry Pi Imager with the following settings\
[https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)


- Raspberry Pi Device
  - Raspberry Pi 5
- Operating System
  - Use Custom
    - Enable "All Files (*)"
    - Select the .dmg that you just unzipped
- Storage
  - *your SD card*
- [ NEXT ]
- Use OS customisation?
  - [ EDIT SETTINGS ]
- General
  - Set hostname
    - skronk *. . . or whatever you want*
  - Set username and password ( *RNBO requires username 'pi'* )
    - pi
    - *your password*
  - Configure wireless LAN
    - *your wifi name*
    - *your wifi password*
    - *your country*
    - *hidden ssid?*
  - Set locale settings
    - *your time zone*
    - *your keyboard layout*
- Services
  - Enable SSH
    - Use password authentication
- [ SAVE ]
- Would you like to apply OS customisation settings?
  - [ YES ]
  - Warning
    - [ YES ]
- Write and Verify
  - Remove SD card
    - [ CONTINUE ]
    - Quit Raspberry Pi Imager

Boot the Pi with the fresh SD card

Reboot ( the activity light will flash red / green several times )

SSH into the pi

$ ```curl https://raw.githubusercontent.com/cooperbaker/skronk/refs/heads/main/install.sh | bash```