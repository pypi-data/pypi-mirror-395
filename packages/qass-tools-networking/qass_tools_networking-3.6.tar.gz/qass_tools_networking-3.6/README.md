# Networking package for Qass Tools

Networking package to remotely control the Analyzer4D software.

## Install as developer

Install the newest version of the pip package by:

```sh
pip install qass-tools-networking --user -e .[developers]
```

## How to import networking package

```py
from qass.tools import networking
```

or to directly address analyzer_socket:

```py
from qass.tools.networking.analyzer_socket import AnalyzerRemote, ExactSamplerates16Bit
```

or address analyzer_ssh as:

```py
from qass.tools.networking.analyzer_ssh import SSHConnector 
```

## How to use networking package

```py
""" Simple example how to intialize a socket connection to the optimizer and have access to analyzer functions."""
from qass.tools.networking.analyzer_socket import AnalyzerRemote, Channels, Amplitudes

with AnalyzerRemote(ip="your_optimizer_ip") as opti:
    opti.set_multiplexer(channel=Channels.CHANNEL_1)
    info = opti.get_project_info()
    print(info)
    opti.set_multiplexer(gain=800)

    proc = opti.get_process_number()

    opti.set_process_comment(proc, "Hello World")

    opti.start_measuring()
    opti.start_sineGenerator(frequency=500, amplitude=Amplitudes.AMP_191_mV)
    time.sleep(2)
    opti.stop_sineGenerator()
    opti.stop_measuring()
```