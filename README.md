# MQTT device status

## What does this do?
This script sends the current status of the device on a MQTT topic.
It can be run either in a docker container or as a systemd service.
Three different states are detected: `Online`, `Offline` or `Crashed`, the which are also the default messages.
Crashes are 'detected' by setting a last will message.

## Configuration
The script can be configured either via a [configuration file](service/mqtt-status.conf) (recommended when running as a service) 
or via environment variables (for docker containers), a template [.env](.env.template) is provided.
