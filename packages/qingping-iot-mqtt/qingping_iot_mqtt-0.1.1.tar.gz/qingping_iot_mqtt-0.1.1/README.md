# Qingping IoT MQTT

Python library and utilities for working with Qingping IoT MQTT protocols - JSON and binary ("HEX"). 

## Background

Qingping IoT devices working over Wi-Fi (and some home Qingping+ devices) can either push data to Qingping IoT Cloud (see [qingping-iot-cloud](https://github.com/danielskowronski/qingping-iot-cloud) library for details) or be "privatized", i.e. change MQTT endpoint to your own MQTT broker. Each model of Qingping IoT Wi-Fi device use either JSON or binary ("HEX") protocol and this cannot be changed. 

References:

- [MQTT JSON](https://developer.qingping.co/private/communication-protocols/public-mqtt-json)
- [MQTT HEX](https://qingping.feishu.cn/docx/BlYOdJVRQobV0ox6SNZcV8V6nZT)

## Scope

This library and set of utilities are designed for both protocols. Ultimately, a Home Assistant integration will be created, but main goal for this repository is to have encoder/decoder of both protocols working with CLI inputs and connected to MQTT broker (including automatic acks, required by some devices). Additionaly, there will be some simple ways of storing all data from devices (SQL or Time-Series DBs to store data coming from historical reports, as HA and Prometheus do not support pushing).

MQTT broker configuration is not part of this project.

Currently, I only have CO2 sensor (HEX protocol) and Air Monitor Lite (JSON protocol), so coverage may be limited.

```
#TODO: usage docs
```
