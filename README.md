# Arping Check My LAN
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](LICENSE)

Catch aliens on your LAN easily!

## Introduction

Using this utility you'll be able to look for the existed devices on your lan and hold them into local file so you can quickly and easily check for any new device had been entered your LAN.

Using [Arping](https://en.wikipedia.org/wiki/Arping)  which is implemented using [scapy](https://github.com/secdev/scapy) library it'll probe hosts on the attached network link by sending Link Layer frames using the ARP request method addressed to a host identified by its MAC Address of the network interface.


## Why "Arping Check My LAN" ?

It's not that easy to manually check the existed hosts and devices in our lan, in most cases we ignore that supposing that we've protected our network very well already.

But unfortunately it's not the case, attackers will find their ways to access our network and we won't notice them, here where "Arping Check My LAN" comes.

## Prerequisites

This utility uses only the `scapy` library which is can be installed using `pip` :

```
pip install scapy
```

## How To use ?

Simply run the `main.py` file with root privilages :

```sh
sudo python main.py
```

In the first time you run the utility it'll store a copy of the existed machines into a local `json` file (~/.arping/) with the name of the specified interface that holds each device's MAC address and its IP address at that time.

Later when running the utility again, it'll check for any new device which is not detected earlier, it'll ask you to confirm that you are aware of this device existence before adding it to the whitelist. Also it'll notify you if any device had a different IP address since the last time it run.

## Command line arguments

using the `-i` argument you can tell the utility from which network interface it'll get the network mask that the broadcast message will be send to.

For example, to check for the devices existed in the network same as my device over the `eth0` adapter we can specify :

```
sudo python main.py -i eth0
```

## License

[Apache License 2.0](LICENSE)
