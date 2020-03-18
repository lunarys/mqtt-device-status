#!/bin/bash
systemctl disable mqtt-status.service
rm /etc/mqtt-integration/mqtt-status.conf
rm /usr/local/bin/mqtt-status.py
rm /etc/systemd/system/mqtt-status.service
