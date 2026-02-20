#!/bin/bash

docker run -d \
  --name mosquitto \
  -p 1883:1883 \
  -v /home/fernando/tests/mqtt/config/mosquitto.conf:/mosquitto/config/mosquitto.conf \
  eclipse-mosquitto