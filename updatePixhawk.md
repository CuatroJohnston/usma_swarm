# Updating Pixhawk Firmware on SASC Vehicles
The first section describes how to flash Pixhawk 2 firmware for the TAROT 650 implementation.  The 2nd section is older and pertains to the original SASC implementation.

### Flashing New Pixhawk 2 (Cube) for Tarot 650 Quad Implementation (TODO: clean this up)
1. Detailed instructions from NPS available at `/ACS/ardupilot/build.md`

2. Make sure you have `px4-v3` firmware build

  * `cd ~/ACS/ardupilot/build` and ensure `px-v3` is there.  
  * If not get it from NPS Gitlab (TODO: update to DI2E): `git clone --recursive git@gitlab.nps.edu:sasc/ardupilot.git` 

3. Ensure `test.py` file will not cause problems

  * `cd ~/scrimmage/usma/plugins/autonomy/python`   
  * `gedit test.py`, ensure all lines are commented, save (TODO: fix this)
  
4. Build the firmware (v3 is for the Pixhawk 2)

  * `./waf configure --board px4-v3`   
  * `./waf copter`

5. Load the Firmware using Q-Ground Control

  * Ensure you have QGC version v3.5.3 or later
  * Plug in the Pixhawk into the computer using micro USB
  * Open QGC, click on the Gears Icon (top left), then select "Firmware"
  * Unplug then replug in the Pixhawk into the computer (per QGC instruction)
  * Click "Ardupilot Flight Stack", "Advanced Settings", "Custom Firmware", select file from `/ACS/ardupilot/built/px4-v3/bin/arducopterv3.hex`
  * In Parameters set "serial2_baud" to "1,500,000"
  
### Ensuring PixHawk 2 Cube connects to QGC on initial setup
1. Detailed instructions from NPS available at `http://ardupilot.org/plane/docs/common-loading-firmware-onto-pixhawk.html`
  
### Updating the Pixhawk on the SASC Zephyr II UASs

1.	Note the “tail” number of the UAS: ____(A)____ (e.g. 10)
2.	Open up the “hatch” of the Zephyr and gently lift the Pixhawk out of the 3D printed carriage so that the micro B USB port is accessible.
3.	Start up and log onto the Linux computer.  Ensure the computer is connected to the Internet via an Ethernet connection.  Ensure you have a USB A to USB micro B cable that can reach between the laptop and the Pixhawk.
4.	On the Linux computer, open a terminal (`Ctrl-Alt-T`).
5.	In the terminal, enter `setupPixhawkPlane.sh` (only for fixed wing Zephyrs!)
6.	Build the firmware image: At the application menu, enter `B` (can skip if it has already been done for this release of ArduPlane).
7.	Update the Pixhawk:  At the application menu, enter `U`.  If the application asks for an aircraft ID, enter the “tail” number identified in line 1 (e.g. 10).
8.	Follow all the instructions for connecting and disconnecting the Pixhawk when prompted.
9.	If an ‘Update Successful!” is displayed, enter Q to quit the application.
10. From the terminal window, make note of the “hash” code whcih appears after the version string (e.g. `ArduPlane V3.8.0beta1 (cf848147)`.
11. Gently seat the Pixhawk back in the carriage.  Make sure no cables are pinched.
