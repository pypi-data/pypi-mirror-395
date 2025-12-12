# tess-publisher

Software to publish TESS-W / TESS-W-4C readings when no WiFi connection is available.

## Introduction

The TESS-W was designed for the common situation in which a permanent place with Internet acess through a home gateway that includes an WiFi access point. After the initial configuration step, the photometer connects to the WiFi router and sends its readings to the STARS4ALL Photometer Network via MQTT using the WiFi router as the default gateway to Internet.

![description](images/yebes.jpg) 
(Yebes Observatory, OAN, Spain)

However there are some sitiuations where this deployment assumption is not valid:
1. Radielectric silent sites such as radiotelescope observatories.
2. Sites that for one reason or another there is not a WiFi router and the only connection to Internet is through a computer with Ethernet.

In the first case, not only the WiFi Access Point (AP) is unavaliable but also the TESS-W must disable its radio transmissor and enable a serial port, which requires a custom modification from factory.

The second case requires some discussion. The good news allows is that there is no need for a photometer custom modification. The computer may install a WiFi dongle and be configured as a WiFi router. This solution would fall in the general use case. Depending on the actual circunstances, this alternative may be dicarded.

The photometer is configured by default to serve as a WiFi AP. However, the photometer cannot publish the readings by itself, since it is not the gateway to Internet and cannot configure the computer as the gateway. So it is the computer that must be connected to the WiFi AP set by the photometer.

For both cases explained above, we need a gateway program that reads measurements from the photometer and publish them to the STARS4ALL MQTT photometer network. This program can conveniently run in a RaspberryPi computer with Internet access via Ethernet.

This program *can handle several photometers* at the same time (i.e one TESS-W and one TESS4C) by configuring them in the `config.toml` configuration file.

The photometer emits measurements in JSON format that are captured by this program, then timestamped and sent to the MQTT broker.
Although the photometer emits these strings every 1-2 seconds, it is ***highly recommended*** to set the transmission rate of one reading per 60 seconds in order not to flood the MQTT broker. This is set in the `config.toml` configuration file described below.

## Installation

This utility is published in PyPI, so it can be installed with your favourite Python package manager. This document uses [UV](https://docs.astral.sh/uv/), an extremely fast Python package manager. It is ***highly recommended*** to create a Python virtual environment. 

The example commands assumes:
* a Raspberry Pi computer running Linux with the default `pi` user.
* Python 3.12
* `uv` installed.

### Virtual environment creation

```bash
~$ pwd
/home/pi
 ~$ mkdir tess
 ~$ cd tess
 tess$ uv venv --python 3.12
Using CPython 3.12.3 interpreter at: /usr/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

### Package installation

```bash
$ tess$ uv pip install tess-publisher
```

## Configuration

### Configure Linux groups

If using the serial port method, it is necessary to add the user `pi` to the `dialout` group in order to have permissions to open the serial port.

```bash
 tess$ sudo usermod -a -G dialout pi
```
It is necessary to open a new login session to take effect. Verify it with the following command:


```bash
 tess$ groups pi
```

### Create an `.env` environment file

Some configuration values are read at runtime via enviroment variables (mostly credentials). In your `/home/pi/tess` directory, create a `.env` file with the following contents:

```bash
# These are needed for the systemd service
PATH=/home/pi/tess/.venv/bin:/usr/local/bin:/usr/bin:/bin
PYTHONIOENCODING=utf-8
VIRTUAL_ENV=/home/pi/tess/.venv

# MQTT stuff
MQTT_TRANSPORT=tcp
MQTT_HOST=test.mosquitto.org
MQTT_PORT=1883
MQTT_USERNAME=""
MQTT_PASSWORD=""
MQTT_CLIENT_ID=""
MQTT_TOPIC=foo/bar

# Administration API
ADMIN_HTTP_LISTEN_ADDR=localhost
ADMIN_HTTP_PORT=8080
```

The following contents will publish readings on a public MQTT broker and is valid for testing purposes only, not for production. ***Contact the STARS4ALL team to get the proper values for the MQTT_XXXX variables***

### Create/Edit a `config.toml` file

The remaining configuration values are stored in a `config.toml` file


```toml
[http]

# HTTP management interface section

# Connection is made by env variables ADMIN_HTTP_LISTEN_ADDR, ADMIN_HTTP_PORT

# http task log level (debug, info, warn, error, critical, none)
log_level = "info"

#------------------------------------------------------------------------#
[mqtt]

# MQTT Client config

# The broker host, username, password and client_id
# are configured by environment variables
# MQTT_BROKER, MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID
# respectively

# MQTT keepalive connection (in seconds)
keepalive = 60

# inactivity timeout (in seconds)
# Program dies after this timeout has expired 
# after the last reading was published to the MQTT broker
timeout = 1800

# namespace log level (debug, info, warn, error, critical, none)
log_level = "info"

# MQTT PDUs log level. 
# See all PDU exchanges with 'debug' level. Otherwise, leave it to 'info'
protocol_log_level = "info"

#------------------------------------------------------------------------#

[tess]

# namespace log level (debug, info, warn, error, critical)
log_level = "info"

# Serial to MQTT queue size
qsize = 1000

# Photometers config data
[tess.stars111]
endpoint = "serial:/dev/ttyACM0:9600"
period = 60 # MQTT TX period in seconds. Recommended value: 60
log_level = "info"
model = "TESS-W"
mac_address = "AA:BB:CC:DD:EE:FF"
zp1 = 20.5
offset1 = 0 # Frequency offset (dark current frequency)
filter1 = "UVIR750"


[tess.stars478]
endpoint = "tcp:192.168.4.1:23" # IP when photometer becomes an Acess Point
period = 60 # MQTT TX period in seconds. Recommended value: 60
log_level = "debug"
model = "TESS4C"
mac_address = "FF:AA:BB:CC:DD:EE"
zp1 = 20.5
offset1 = 0 # Frequency offset (dark current frequency)
filter1 = "UVIR750"
zp2 = 20.5
offset2 = 0 # Frequency offset (dark current frequency)
filter2 = "UVIR650"
zp3 = 20.5
offset3 = 0 # Frequency offset (dark current frequency)
filter3 = "RGB-R"
zp4 = 20.5
offset4 = 0 # Frequency offset (dark current frequency)
filter4 = "RGB-B"
firmware = "Mar  4 2024"
```

You need to configure the photometer-specific data. Other values are good as is. In the case of a single channel TESS-W photometer, we have:
* `endpoint`. This is where we specify if reading by serial or TCP port. The endpoint string has three fields separated by `:`. The first one specifies the communication method, the second one is the serial device or IP address and the third one is the baud rate in case of serial port (9600 is fine) or the TCP port to open. The TESS-W IP address as an access point is always `192.18.4.1`. The default TCP port is `23`.
* `period`. Send a message every *period* seconds. Leave it at 60.
* `model` is either `TESS-W` or `TESS4C` strings.
* `mac_address`: See your photometer label in the cable to get this important value.
* `zp1`: Photometer's zero point as calibrated by STARS4ALL.
* `offset1`: frequency offset when completely dark. Leave it a t zero.
* `filter1`: string identifying a mounted filter. All TESS-W models use an UV/IR cut of filter that cuts IR at 750nm. Leave it at "UVIR750" anless your photometer was delivered with a custom filter.

In the case of a 4-channel TESS-W, the `zp1`, `filter1` and `offset1` values must also be configured to channels 2, 3 & 4. You must also specify a `firmware` value. All these values can be looked up by connecting the photometer when it is configured as an [Access Point](http://192.168.4.1/config)


### Testing

After configuration, launch the program in the project directory:

```bash
cd $HOME/tess
uv run tess-publisher --console --trace --config config.toml
``` 

Ouput should be similar to this:

```bash
2025-12-03 14:48:56,654 [INFO    ] [root] ============== tesspublisher.client 0.1.dev43+gd95d6553a.d20251203 ==============
2025-12-03 14:48:56,655 [INFO    ] [stars111] Using SerialProtocol
2025-12-03 14:48:56,681 [INFO    ] [stars111] {'name': 'stars111', 'rev': 2, 'mac': 'AA:BB:CC:DD:EE:FF', 'chan': 'pruebas', 'calib': 20.5, 'wdBm': 0}
2025-12-03 14:48:56,681 [INFO    ] [stars111] Waiting 5 secs. before sending register message again
2025-12-03 14:49:01,682 [INFO    ] [stars111] Opening Serial connection to /dev/ttyACM0 @ 9600
2025-12-03 14:49:01,684 [INFO    ] [stars111] Serial connection to /dev/ttyACM0 @ 9600 open
2025-12-03 14:49:56,682 [INFO    ] [stars111] {'udp': 13861, 'rev': 2, 'name': 'stars111', 'freq': 2688.17, 'mag': 11.93, 'tamb': 21.27, 'tsky': 21.05, 'wdBm': 0, 'hash': '988', 'ain': 384, 'ZP': 20.5, 'tstamp': '2025-12-03T13:49:56Z', 'seq': 0}
2025-12-03 14:50:56,683 [INFO    ] [stars111] {'udp': 13913, 'rev': 2, 'name': 'stars111', 'freq': 2604.17, 'mag': 11.96, 'tamb': 21.21, 'tsky': 21.11, 'wdBm': 0, 'hash': '988', 'ain': 386, 'ZP': 20.5, 'tstamp': '2025-12-03T13:50:56Z', 'seq': 1}
```

### Linux service and log rotation

For convenience, it is *highly recommended* to install this software as a Linux service and its logfile managed by logrotate.

Sample `tesspub.service` file to be placed under `/etc/systemd/system/`

```
[Unit]
Description=TESS Quality Sky Meter MQTT publisher service
Documentation=https://github.com/STARS4ALL/tess-publisher

[Service]
Type=simple
User=root
KillMode=process
ExecStart=/home/pi/tess/.venv/bin/tess-publisher --config /home/pi/tess/config.toml --log-file /home/pi/tess/log/tess-publisher.log
EnvironmentFile=/home/pi/tess/.env
WorkingDirectory=/home/pi/tess/

[Install]
WantedBy=multi-user.target
```

Do not forget to reload systemd and enable this service at startup

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl start tesspub.service
$ sudo systemctl enable tesspub.service
```

If you configured the service to write a logfile like the example below, it is recommended to manage its logfile with logrotate.

Sample `tesspub` logrotate spec below rotates dayly and keeps a history of 30 logfiles. It must be be placed under `/etc/logrotate.d`

```
/home/pi/tess/log/tess-publisher.log {
	su pi pi
	daily
	dateext
	rotate 30
	missingok
	notifempty
	copytruncate
}
```
