# screen-masking

Controlling a stepper motor used for screen masking in a home cinema via http protocol.

## Involved Components

- Nema 17 stepper motor, like the ones used for 3D-printing
- TB6600 stepper driver
- power adapter with 24–36 V / 4 A output
- Raspberry Pi 3 or higher with Raspbian installed

How to build screen masking mechanics and how to pull the mask with a stepper motor
and a screw drive is totally up to you.
[Have a look at this article.](https://translate.google.de/translate?sl=de&tl=en&u=https%3A%2F%2Fwww.heimkino-praxis.com%2Fleinwand-maskierung-antriebsmechaniken%2F)

## Hardware Setup

As described in [python/tb6600/wiring-nema17-4pin.md](python/tb6600/wiring-nema17-4pin.md),

1. connect the stepper motor with the TB6600 driver
2. connect the TB6600 driver with the Raspberry Pi
3. connect power adapter to the driver
4. set switches at the driver to whatever applies to your motor

## Software Setup

This repository contains the software part of the project, including Python scripts to control the stepper motor
and a Node.js application running as web service. This is your interface to any home cinema control mechanisms
such as universal remote controls. 

### 1. Install Raspbian

There are thousands of tutorials out there on how to do this. SSH mode preferred!

### 2. Install Node.js

[Here is a tutorial](https://www.instructables.com/id/Install-Nodejs-and-Npm-on-Raspberry-Pi/) on how to do this.

### 3. Setup This Repository

Clone this repository to `~/screen-masking` or wherever you like it to run.

### 4. Install Node Modules

`cd` into the `screen-masking` directory and install all required node_modules by typing

```
npm install
```

This may take a while.

### 5. Make a Test Run

Start the app by typing

```
node index.js
```

The app should start over and tell you on which port it is listening for requests.

`curl` or type the following URL into a web browser located in the same local network as your Raspberry Pi:

```
http://<raspberry-pi-ip>:<port>/force-by/500
```

**Warning!** Always test the motor while it is not connected to your screen masking. Driving the motor too far into
one direction will very likely damage the mechanics. Do not underestimate the strength of a stepper motor.

### 6. Setup the App to Run at System Startup

You may want to [autoload the Node-app at system startup](https://weworkweplay.com/play/raspberry-pi-nodejs/).

```
sudo vi /etc/rc.local
```

Add the following line:

```
su pi -c 'cd /home/pi/screen-masking; node index.js < /dev/null &'
```

After a reboot the app should run in the background. You should still be able to call the above mentioned URL.

### 7. Adjust Configuration

The Node app is just a HTTP wrapper for the Python scripts. There is no configuration to take care of
(unless you like to change out well-chosen port number).

However, configuring the stepper behavior is done in `python/tb6600/stepper.py`.

- You can change the Raspberry Pi pin numbers for `DIR`, `PUL` and `ENA` output.
- The `STEP_ANGLE` is preconfigured for half steps of 0.9 degree.
- There is a `RAMP_LENGTH` of 600 steps configured for speeding up and slowing down the motor nicely.
- `MIN_RPM` and `MAX_RPM` defines the slowest and fastest speed of the motor.
  Set these as low/high as possible, but where the motor turns without producing too much noise.
- `MAX_STEPS` is the most important value for you. This is how many steps the motor may turn before it reaches the
  upper security boundary.

A few more words on `MAX_STEPS`. The stepper script ensures that the motor can only move between `0` and `MAX_STEPS`.
It can not move below or above these boundaries (it will simply stop). This is to make sure that the motor can not push
or pull your screen masking over its mechanical limits.

Before using the script in production, you have to determine how many steps your motor must move to run your
screen masking over its full mechanical range. Using the motor to turn a screw drive which pulls the mask, the carriage
on the screw will most likely have to move the same distance as the mask. Let's say this is 20 cm (7,874 inches).
Depending on the pitch of the thread this may need e.g. 10000 steps for the motor to perform. Use a ruler to measure
how far the carriage goes by a given amount of steps. Then set `MAX_STEPS` to this value.

## API

You can call the following paths to interact with the service.
Use HTTP *GET* to request values und *PUT* to perform actions.
Return values are in JSON format.

**GET /position**\
Returns the current position of the motor as steps, a value between `0` and `MAX_STEPS`.

**GET /power**\
Returns the power state of a relay module connected at pin 11. `1` or `0`.
(This is some kind of bonus feature. Use a relay module to turn *on* or *off* power of the driver via the API.)

**PUT /move-to/1000**\
Moves the motor absolute to the given step. Takes a value between `0` and `MAX_STEPS`.
Movement as fast as possible, using a ramp.

**PUT /move-by/250**\
Moves the motor relative by the given steps. Takes any positive or negative number.
Example: motor is currently at position 4350, `/move-by/-350`, new position is 4000.
Movement as fast as possible, using a ramp.

**PUT /force-by/250**\
Moves the motor relative by the given steps. Takes any positive or negative number.
Movement as slow as possible, no ramp. **Ignores min and max boundaries!**
Use this very carefully! The motor will run out of your masking's mechanical bounds without apologizing.
Instead you can simply turn the motor or screw by hand.

**PUT /calibrate**\
Sets the internally saved position to `0`. Call this after you manually set the motor to its lower bound position.

**PUT /power/1**\
Sets the power state of a relay module connected at pin 11. `1` or `0`.
This is always called automatically before you perform any other action that needs power for the motor.
You don't have to set the power state explicitly. The relay module is always powered on (if off) before moving.
If you have no relay module, power is *always on* anyway.
