#!/bin/bash
pip3 install -r ./requirements
cp ../image/script/mqtt-status.py /usr/local/bin/mqtt-status.py
cp ./mqtt-status.service /etc/systemd/system
chown root:root /usr/local/bin/mqtt-status.py
chown root:root /etc/systemd/system/mqtt-status.service
mkdir -p /etc/mqtt-integration
cp ./mqtt-status.conf /etc/mqtt-integration
chown root:root /etc/mqtt-integration
chown root:root /etc/mqtt-integration/mqtt-status.conf
chmod 600 /etc/mqtt-integration/mqtt-status.conf
systemctl enable mqtt-status.service
systemctl start mqtt-status.service
