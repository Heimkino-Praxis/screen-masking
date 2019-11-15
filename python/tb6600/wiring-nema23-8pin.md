## Motor: NEMA 23 With 8 Wires

Connect motor to TB6600 stepper driver:

- **B-** yellow
- **B+** red
- **A-** orange
- **A+** black

Connect unused wires:

- blue + violet
- white + brown

## Stepper Driver: TB6600

Connect stepper driver to power adapter:

- **GND** power minus
- **VCC** power plus

Connect stepper driver to Raspberry Pi:

- **ENA-(ENA)** PIN 39 (GND)
- **ENA+(+5V)** PIN 37 (BCM 26)
- **DIR-(DIR)** PIN 34 (GND)
- **DIR+(+5V)** PIN 33 (BCM 13)
- **PUL-(PUL)** PIN 30 (GND)
- **PUL+(+5V)** PIN 35 (BCM 19)

Switches 1–6 settings for half steps and maximum current of 4.0 A:

- on-off-on-off-off-off
