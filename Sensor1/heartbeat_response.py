import paho.mqtt.client as mqtt
import time
import os


FILE_HEARTBEAT_LOG = 'heartbeat.log'
broker_hostname = "192.168.0.110"
port = 1883
THREAD1_TOPIC = "heartbeat_check"
THREAD2_TOPIC = "heartbeat_response"


def print_log(log, msg):
    if log:
        mode = 'a' if os.path.exists(log) else 'w'
        with open(log, mode) as f:
            f.write(msg + '\n')


def response(dv_name="device", stdout=False, log=False):
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        if stdout:
            print("Received message: ", msg)
        if log:
            print_log(FILE_HEARTBEAT_LOG, "Received message: " + msg)
        if message.topic == THREAD1_TOPIC:
            response_msg = msg + "_" + dv_name[6:]
            result = client.publish(THREAD2_TOPIC, response_msg)
            if stdout:
                print("Response sent: ", response_msg)
            if log:
                print_log(FILE_HEARTBEAT_LOG, "Response sent: " + response_msg)
        else:
            pass

    def on_connect(client, userdata, flags, return_code):
        if return_code == 0:
            if stdout:
                print("Connected")
            if log:
                print_log(FILE_HEARTBEAT_LOG, "Connected")
            client.subscribe(THREAD1_TOPIC)
        else:
            if stdout:
                print("could not connect, return code:", return_code)
            if log:
                print_log(FILE_HEARTBEAT_LOG, "could not connect, return code:" + str(return_code))

    # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, dv_name)
    client = mqtt.Client(dv_name)
    # client.username_pw_set(username="my_user", password="12345") # uncomment if you use password auth
    client.on_connect = on_connect
    client.on_message = on_message
    client.failed_connect = False
    client.connect(broker_hostname, port)
    client.loop_start()

    try:
        while not client.failed_connect:
            if not client.is_connected() and stdout:
                print("Client not connected, Trying to connect...")
            if not client.is_connected() and log:
                print_log(FILE_HEARTBEAT_LOG, "Client not connected, Trying to connect...")
            time.sleep(1)
        if client.failed_connect and stdout:
            print('Connection failed, exiting...')
        if client.failed_connect and log:
            print_log(FILE_HEARTBEAT_LOG, 'Connection failed, exiting...')

    finally:
        client.disconnect()
        client.loop_stop()
