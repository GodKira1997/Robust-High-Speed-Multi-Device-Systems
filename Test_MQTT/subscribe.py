import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
        client.subscribe("test")
    else:
        print("could not connect, return code:", return_code)
        client.failed_connect = True


def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))


broker_hostname = "192.168.0.110"
port = 1883
print(broker_hostname, port)

client = mqtt.Client("Client2")
# client.username_pw_set(username="my_user", password="12345") # uncomment if you use password auth
client.on_connect = on_connect
client.on_message = on_message
client.failed_connect = False

client.connect(broker_hostname, port)
client.loop_start()

# this try-finally block ensures that whenever we terminate the program earlier by hitting ctrl+c, it still gracefully exits
try:
    i = 0
    print("HEY")
    while client.failed_connect == False:
        print(client.is_connected())
        time.sleep(1)
        i = i + 1
    if client.failed_connect == True:
        print('Connection failed, exiting...')

finally:
    client.disconnect()
    client.loop_stop()