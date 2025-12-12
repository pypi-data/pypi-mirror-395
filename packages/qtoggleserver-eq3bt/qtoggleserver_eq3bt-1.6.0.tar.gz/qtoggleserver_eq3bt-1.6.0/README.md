## About

This is an addon for [qToggleServer](https://github.com/qtoggle/qtoggleserver).

It provides Eqiva eQ-3 bluetooth thermostat support for qToggleServer.


## Install

Install using pip:

    pip install qtoggleserver-eq3bt


## Usage

##### `qtoggleserver.conf:`
``` ini
...
peripherals = [
    ...
    {
        driver = "qtoggleserver.eq3bt.EQ3BTThermostat"
        name = "livingradiator"         # a name of your choice
        address = "00:1A:22:AA:BB:CC"   # bluetooth address of the device
    }
    ...
]
...
```
