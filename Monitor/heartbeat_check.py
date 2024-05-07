import argparse
import paho.mqtt.client as mqtt
import time
import os
import threading


FILE_HEARTBEAT_LOG = 'heartbeat_checker.log'
broker_hostname = "192.168.73.33"
port = 1883
THREAD1_TOPIC = "heartbeat_check"
THREAD2_TOPIC = "heartbeat_response"
RETRIES = 3
NUM_SENSORS = 2


def print_log(log, msg):
    if log:
        mode = 'a' if os.path.exists(log) else 'w'
        with open(log, mode) as f:
            f.write(msg + '\n')


def monitor(stdout=False, log=False):
    def thread1_heartbeat_request(dv_name="heartbeat_request"):
        def on_connect(client, userdata, flags, return_code):
            if return_code == 0:
                if stdout:
                    print("connected")
                if log:
                    print_log(FILE_HEARTBEAT_LOG, "connected")
            else:
                if stdout:
                    print("could not connect, return code:", return_code)
                if log:
                    print_log(FILE_HEARTBEAT_LOG, "could not connect, return code:" + str(
                        return_code))
        # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, dv_name)
        client = mqtt.Client(dv_name)
        # client.username_pw_set(username="my_user", password="12345") # uncomment if you use password auth
        client.on_connect = on_connect
        client.connect(broker_hostname, port)
        client.loop_start()

        msg_count = 0

        try:
            while msg_count < 200:
                time.sleep(2)
                result = client.publish(THREAD1_TOPIC, msg_count)
                status = result[0]
                if status == 0:
                    if stdout:
                        print("Message " + str(msg_count) + " is published to topic " +
                              THREAD1_TOPIC)
                    if log:
                        print_log(FILE_HEARTBEAT_LOG, "Message " + str(msg_count) + " is "
                                                                                    "published to "
                                                                                    "topic " +
                                  THREAD1_TOPIC)
                else:
                    if stdout:
                        print("Failed to send message to topic " + THREAD1_TOPIC)
                    if log:
                        print_log(FILE_HEARTBEAT_LOG, "Failed to send message to topic " +
                                  THREAD1_TOPIC)
                    if not client.is_connected():
                        if stdout:
                            print("Client not connected, exiting...")
                        if log:
                            print_log(FILE_HEARTBEAT_LOG, "Client not connected, exiting...")
                        break
                msg_count += 1

        finally:
            client.disconnect()
            client.loop_stop()

    def thread2_heartbeat_response(dv_name="heartbeat_response"):
        current_active_sensors = set()
        sensors_list = set([i for i in range(1, NUM_SENSORS + 1)])
        current_count = 0

        def on_connect(client, userdata, flags, return_code):
            if return_code == 0:
                if stdout:
                    print("connected")
                if log:
                    print_log(FILE_HEARTBEAT_LOG, "connected")
                client.subscribe(THREAD2_TOPIC)
                client.subscribe(THREAD1_TOPIC)
            else:
                if stdout:
                    print("could not connect, return code:", return_code)
                if log:
                    print_log(FILE_HEARTBEAT_LOG, "could not connect, return code:" + str(
                        return_code))
                client.failed_connect = True

        def on_message(client, userdata, message):
            nonlocal current_active_sensors, sensors_list, current_count
            msg = str(message.payload.decode("utf-8"))
            if stdout:
                print("Received message: ", msg)
                print(f"Topic: {message.topic}")
            if log:
                print_log(FILE_HEARTBEAT_LOG, "Received message: " + msg)
                print_log(FILE_HEARTBEAT_LOG, f"Topic: {message.topic}")
            if message.topic == THREAD1_TOPIC:
                current_count = int(msg)
                if int(msg) % RETRIES == 0:
                    if len(current_active_sensors) != NUM_SENSORS:
                        dead_sensors = sensors_list - current_active_sensors
                        if stdout:
                            print(f'Dead Sensor list: {dead_sensors}')
                        if log:
                            print_log(FILE_HEARTBEAT_LOG, f'Dead Sensor list: {dead_sensors}')
                        # print(f'Active Sensor list: {current_active_sensors}')
                    current_active_sensors = set()
            else:
                msg = msg.split("_")
                if 'sensor' in msg[1].lower():
                    # if stdout:
                        # print(msg)
                        # print(current_count, current_count % RETRIES, int(msg[0]))
                    if (current_count - (current_count % RETRIES) <= int(msg[0]) <=
                            current_count):
                        current_active_sensors.add(int(msg[1][6:]))

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

    if stdout:
        print("Starting threads...")
    if log:
        print_log(FILE_HEARTBEAT_LOG, "Starting threads...")
    thread_1 = threading.Thread(target=thread1_heartbeat_request)
    thread_1.start()
    thread_2 = threading.Thread(target=thread2_heartbeat_response)
    thread_2.start()

    # Wait for the inner thread to finish
    thread_1.join()
    thread_2.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Stdout Heartbeat")
    parser.add_argument('--sout', action='store_true', default=False, help="Console output")
    parser.add_argument('--log', action='store_true', default=False, help="Log the file")
    args = parser.parse_args()
    monitor(args.sout, args.log)
