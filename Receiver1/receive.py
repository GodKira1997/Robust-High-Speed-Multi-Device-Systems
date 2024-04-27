"""Example program to show how to read a multi-channel time series from LSL."""

import threading
from pylsl import StreamInlet, resolve_stream, local_clock


def receive_data(inlet, name):
    count = 0
    latency = 0
    start_time = local_clock()
    end_time = local_clock()
    print("Receiving data...")
    while True:
        if count % 100 == 0 and count != 0:
            rate = count / (end_time - start_time)
            latency = latency / (end_time - start_time)
            # count = 0
            # start_time = local_clock()
            print(f"Stream: {name}, Latency: {latency}s, Rate: {rate}s")
        count += 1
        # Get a new sample from the inlet
        sample, timestamp = inlet.pull_sample()
        print(f"Stream: {name}, Sample: {sample}, Timestamp: {timestamp}")
        # Get current local time
        end_time = local_clock()
        # Calculate latency
        latency += end_time - timestamp
        # print(f"Stream {idx} - Latency: {latency:.3f}s, Current Time: {end_time:.3f}s, "
        #       f"Timestamp: {timestamp:.3f}s")


def find_sensor(name):
    streams = resolve_stream('name', name)
    if len(streams) == 0:
        print(f"Stream {name} not found")
        return None
    print(f"Found streams for {name}: ", streams[0].source_id())
    inlet = StreamInlet(streams[0])
    receive_data(inlet, name)


def main():
    threads = []
    thread1 = threading.Thread(target=find_sensor, args=('Sensor1',))
    threads.append(thread1)
    thread2 = threading.Thread(target=find_sensor, args=('Sensor2',))
    threads.append(thread2)

    print("LSL Stream Consumption threads Starting ...")
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("LSL Stream Consumption threads finished")


if __name__ == '__main__':
    main()