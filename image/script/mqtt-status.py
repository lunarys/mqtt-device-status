#!/usr/bin/python

import paho.mqtt.client as mqtt
import sys
import time
import signal
import os
import psutil

#####################################
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        result = client.publish(topic, up, qos, retain is not None and retain == True)
        client.connected_flag = True
        print("[C] Connected OK")
    else:
        print("[C] Bad connection: Returned code=", rc)
#####################################################
def on_disconnect(client, userdata, rc):
    print("[C] Disconnected: ", rc)
    client.connected_flag = False
#####################################################
def signal_handler(sig, frame):
    print("Interrupt or termination received")
    result = client.publish(topic, down, qos, retain is not None and retain == True)
    client.loop_stop()
    client.disconnect()
    print("Done")
    exit(0)
###################################

# Set default values
broker_address="localhost"
port=1883
qos=1
retain = None
up = "Online"
down = "Offline"
crash = "Crash"

# Get iterator for command line arguments and skip first item (the script call)
arg_it = iter(sys.argv)
next(arg_it)

topic_set = False
user_set = False
password_set = False

topic = os.environ.get('MQTT_TOPIC')
starttime_topic = os.environ.get('MQTT_STARTTIME_TOPIC')
broker_address = os.getenv('MQTT_BROKER', broker_address)
port = int(os.getenv('MQTT_PORT', port))
qos = int(os.getenv('MQTT_QOS', qos))
user = os.environ.get('MQTT_USER')
password = os.environ.get('MQTT_PASSWORD')
up = os.getenv('MQTT_UP_MESSAGE', up)
down = os.getenv('MQTT_DOWN_MESSAGE', down)
crash = os.getenv('MQTT_CRASH_MESSAGE', crash)
disable_starttime = os.getenv('MQTT_DISABLE_STARTTIME')

if topic is not None:
    topic_set = True

if user is not None:
    user_set = True

if password is not None:
    password_set = True

# Parse command line arguments
for arg in arg_it:
    if arg == '-a':
        broker_address=next(arg_it)

    elif arg == '-q':
        qos=next(arg_it)

    elif arg == '-p':
        port = next(arg_it)

    elif arg == '-f':
        import configparser
        configParser = configparser.RawConfigParser()
        configParser.read(next(arg_it))

        if configParser.has_option('messages', 'up'):
            up = configParser.get('messages', 'up')

        if configParser.has_option('messages', 'down'):
            down = configParser.get('messages', 'down')

        if configParser.has_option('messages', 'crash'):
            crash = configParser.get('messages', 'crash')

        if configParser.has_option('settings', 'retain'):
            retain = configParser.getboolean('settings', 'retain')

        if configParser.has_option('settings', 'topic'):
            topic = configParser.get('settings', 'topic')
            topic_set = True

        if configParser.has_option('settings', 'starttime_topic'):
            starttime_topic = configParser.get('settings', 'starttime_topic')

        if configParser.has_option('settings', 'disable_starttime'):
            disable_starttime = configParser.getboolean('settings', 'disable_starttime')

        if configParser.has_option('settings', 'address'):
            broker_address = configParser.get('settings', 'address')

        if configParser.has_option('settings', 'qos'):
            qos = configParser.getint('settings', 'qos')

        if configParser.has_option('settings', 'port'):
            port = configParser.getint('settings', 'port')

        if configParser.has_option('settings', 'user'):
            user = configParser.get('settings', 'user')
            user_set = True

        if configParser.has_option('settings', 'password'):
            password = configParser.get('settings', 'password')
            password_set = True

    elif arg == '--up' or arg == '-U':
        up = next(arg_it)

    elif arg == '--down' or arg == '-D':
        down = next(arg_it)

    elif arg == '-t':
        topic = next(arg_it)
        topic_set = True

    elif arg == '-s' or arg == '--starttime-topic':
        starttime_topic = next(arg_it)

    elif arg == '--crash' or arg == '-C':
        crash = next(arg_it)

    elif arg == '-r':
        retain = True

    elif arg == '--retain':
        retain = next(arg_it) == 'true'

    elif arg == '-u':
        user = next(arg_it)
        user_set = True

    elif arg == '-pw' or arg == '-P':
        password = next(arg_it)
        password_set = True

    elif arg == '--disable-starttime':
        disable_starttime = True

    elif arg == '-h':
        print("Usage:", sys.argv[0], "\n", """-t <topic> ------------- base topic to publish to
 -a <host address> ------ mqtt server host
[-s <starttime-topic> --- topic to publish the starttime to (default: base topic + /starttime)
[-p <port>] ------------- mqtt server port
[-q <qos>] -------------- quality of service
[-u <user>] ------------- user for the mqtt server
[-pw <password>] -------- password for the mqtt server
[-U <up-message>] ------- message on start
[-D <down-message>] ----- message on stop
[-C <crash-message>] ---- message on crash (testament)
[-r(etain flag)] -------- retain all messages
[--retain <true|false>] - set retain policy (default: retain only starttime)
[--disable-starttime] --- do not send the starttime""")
        exit()

    else:
        print("Use \'", sys.argv[0], " -h\' to print available arguments.")
        exit()

# User and password need to be set both or none
if user_set != password_set:
    print("Please set either both username and password or none of those")
    exit()

# Can't assume topic and message
if not topic_set:
    print("Please set the status topic. Help:", sys.argv[0], "-h")
    exit()

if starttime_topic is None:
    starttime_topic = topic + "/starttime"

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Set up MQTT client
client = mqtt.Client()

# Set last will
client.will_set(topic, crash, qos, retain is not None and retain == True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Username and password
if user_set and password_set:
    client.username_pw_set(user, password)

# Connect to broker
client.connect(broker_address, port)

# Set start time
if disable_starttime is None or disable_starttime == False:
    starttime = int(psutil.boot_time())
    client.publish(starttime_topic, str(starttime), qos, retain is None or retain == True)

# Loop until interrupt is received
client.loop_forever()
