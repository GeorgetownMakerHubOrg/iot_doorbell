
### Code and Scripts for Georgetown MakerHub's IOT Doorbell.

Georgetown’s MakerHub needs music.   And a working doorbell. The most practical and simple approach is to build a Spotify streaming service that can be interrupted by an IoT doorbell.   Tools for building this solution include:

* A Raspberry Pi 3 or 4
* Amplified speaker and cable
* Librespot & PulseAudio
* IoT doorbell based upon the ESP8266 MCU
* MQTT protocol using TCP on the MakerHub’s private network

The following instructions will help anyone with basic familiarity with Raspberry Pis, Linux, and hacking to debug or build from scratch the solution we’ve cobbled.  It involves the following steps:

1. Create a minimal Raspian OS on a MicroSD
2. Put the RPi on the MakerHub private network
3. Install packages to compile and install librespot
4. Install PulseAudio and Sox
5. Install packages to install MQTT
6. Clone the Doorbell Git repository and configure the default settings in config.py
7. Enable Librespot, PulseAudio, MQTT-listen to load on boot up

### Installation

1. Create a Raspian LITE distribution (no desktop) following [these instructions](https://www.raspberrypi.com/documentation/computers/getting-started.html).

2. Using `sudo raspi-config`, enable `sshd()` and configure wpa_supplicant to find the hidden private network called PILGRIMAGE_25.   Access the ASUS router at 192.168.1.1 and add the MAC address of the RPi.  Be sure to change to default `pi` password from `raspberry` to the MakerHub assigned password.
	
The `/etc/wpa_supplicant/wpa_supplicant` file should include the following, as a minimum:
    
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US

    network={
        scan_ssid=1
        ssid="PILGRIMAGE_25"
        key_mgmt=NONE
    }

3. Fetch packages for compiling and install librespot
    Install `git` via:

    `pi@raspberrypi:~/iot_doorbell $ sudo apt install git`

Install `rust` & C compilers to install `librespot` following instructions on this [page](https://github.com/librespot-org/librespot/blob/master/COMPILING.md).  Compile using the pulseaudio-backend and not the default ALSA: 

    pi@raspberrypi:~ $ sudo apt-get install libpulse-dev
    pi@raspberrypi:~ $ git clone https://github.com/librespot-org/librespot.git
    pi@raspberrypi:~ $ cargo build --no-default-features --features "pulseaudio-backend"</code>
    
4. Install pulseaudio & sox for audio playback via:

    ```
    pi@raspberrypi:home/pi/iot_doorbell $ sudo apt-get install pulseaudio
    pi@raspberrypi:~/iot_doorbell $ sudo apt-get install sox libsox-fmt-mp3</code>
    ```
5. Install pip3 and paho-mqtt via:

    ```
    pi@raspberrypi:~/iot_doorbell $ sudo apt-get install python3-pip
    pi@raspberrypi:~/iot_doorbell $ pip3 install paho-mqtt
    ```

6. Install MakerHub bits from git:

    ```
    pi@raspberrypi:~/iot_doorbell $ git clone https://github.com/GeorgetownMakerHubOrg/iot_doorbell.git
    ```
You will also need to copy the config.py.sample to config.py and replace the dummy values for USER, X_AIO_KEY, MQTT_PASSWORD, and MQTT_SUB_TOPIC with real values.

7. Since librespot and mqtt-listen will run as a user process, configure both librespot and mqtt-listen to start as a ‘pi’ process on bootup:   
    * Using the `raspi-config` tool, select “`1 System Options-> S5 Boot / Auto Login->B2 Console Autologin Text console` to have the RPi automatically log in as ‘pi’ user on bootup.
    * Copy the librespot.service file from the iot_doorbell distribution to the user system control directory.  Enable this service and start this service:

        ```
        pi@raspberrypi:~/iot_doorbell $ sudo cp librespot.service /lib/systemd/user
        pi@raspberrypi:~/iot_doorbell $ sudo cp mqtt-listen.service /lib/systemd/user
    
        pi@raspberrypi:~/iot_doorbell $ systemctl --user enable librespot.service
        pi@raspberrypi:~/iot_doorbell $ systemctl --user enable mqtt-listen.service
        ```

### Actual Doorbell

The doorbell uses the following components:
  * D1 Mini Wemos ESP8266 
  * Single Neopixel for Status
  * Simple push button

[Circuitry for this project.](./Doorbell_bb.jpg)

[3D Printed a very nice case from Thingiverse.](https://www.thingiverse.com/thing:2847539)
[It looks like this.](./Doorbell.jpeg) 
