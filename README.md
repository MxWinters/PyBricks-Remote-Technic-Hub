# PyBricks Remote Controlled Technic Hub
Pybricks software for using the PoweredUp Remote with the Technic hub. This has been written for use with my motorised 42110 Land Rover set but can be used on any model that has 2 drive motors and 1 steer motor such as the 42099 4X4 X-treme Off-Roader set.

The code allows for 2 different control modes, Precision Mode and Bang Bang Mode.
Precision Mode is basically a speed controller for the drive motors and increments the motor speed by 10%. It also increments the steering motor by 10°.
Bang Bang Mode acts as a simple on/off controller for the drive motors and turns the steering motor all the way to the endstop.

# Install
Simply download to your device, open <Version 1.0/main.py> with the PyBricks app or PyBricks website with Chrome, configure it as per below and then flash the code to the Technic Hub in the normal way.

# Configuration
1. Set which Controller Mode you want the hub to start with in the Set Startup Controller Mode section.
2. Set the user definable settings in the "User Definable Variables" section.
3. Set the motor settings in the "Initialize The Motors" section.
(detailed info on each setting is included in the comments next to each setting in the main.py file)

# Bugs / Issues
Should you have any issue with it, send me a message on WhatsApp/Facebook/Eurobricks or submit an issue on the Issues tab on GitHub and Ill look into it.

# Contributions
Being an open source project, if you have any changes/bug fixes/improvements, feel free to fork this repo and submit a pull request. I welcome any contributions to the project.

# Copyright / Licence
The project has been published under the MIT licence, you are free to download, run, edit and publish derivatives of this software but the top copyright notice MUST remain. See LICENCE file for more information.
