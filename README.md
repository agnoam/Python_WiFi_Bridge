# Python_WiFi_Bridge

Python_WiFi_Bridge created to handle WiFi manipulation by Command line (cmd / terminal)
# Tested On
  - Windows (10)
  - Linux (raspbian)

# How to run this library ?

  Just put download this repository and run in cmd / terminal
  `` python Bridge.py <command> ``
# Commands

## -scan
-scan command return all available WiFi networks array. after him another array with the encryption type key

#### Example
    python Bridge.py -scan
    ['AndroidAP', 'Home Network', 'Mall', 'Free WiFi']
    ['WPA2_PSK', 'WPA2_PSK', 'WPA2_PSK', None]

## -connect
-connect has 2 parameters, one of them is necessary, and one dependent on the first.

- SSID of the wanted WiFi network
- Password of the WiFi network (if needed)

connect function based on scan function results

#### Example

    python Bridge.py -connect <SSID> <Password>
    
## -status
-status has no parameters, it gives you your Wireless Lan antena status. 
Which can be:
- DISCONNECTED
- SCANNING
- INACTIVE
- CONNECTING
- CONNECTED

#### Example
    python Brdige.py -status
    CONNECTED

### Installation
There is no installation that need to be before you use it.
JUST PLUG AND PLAY

**Building for production**

#### Based On

This project based on @awkman/pywifi repository
See more info here: [pywifi repository](https://github.com/awkman/pywifi)

**Free Software**
