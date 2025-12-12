## python-can-damiao

This module is a plugin that lets you use Damiao USB-CAN adapters with python-can.

**Disclaimer:** This project is not affiliated with, endorsed by, or associated with Shenzhen Damiao Technology Co., Ltd. in any way. It is an independent community-developed plugin.

### Documentation

For detailed information about Damiao USB-CAN adapters, please refer to the official documentation:
[Damiao USB-CAN Documentation](https://gitee.com/kit-miao/dm-tools/tree/master/USB%E8%BD%ACCAN)

### Installation

Install using pip:

    $ pip install python-can-damiao

### Usage

Overall, using this plugin is quite similar to the main Python-CAN library, with the interface named `damiao`. 

Create python-can bus with the Damiao USB-CAN interface:

    import can

    bus = can.Bus(interface="damiao", channel=0, bitrate=1000000)