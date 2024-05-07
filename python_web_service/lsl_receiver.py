import argparse
import threading
from pylsl import StreamInlet, resolve_stream, local_clock
from heartbeat_response import response, print_log
from multiprocessing import shared_memory
import time


def main_receive(shared, device, stdout, log=False):
    DEVICE_NAME = device
    FILE_STREAM_LOG = DEVICE_NAME + '_lsl.log'
    SENSORS = ['Sensor1', 'Sensor2']
    print(DEVICE_NAME, FILE_STREAM_LOG)

    def receive_data(inlet, name, shared, stdout=False, log=False):
        count = 0
        latency = 0
        start_time = local_clock()
        end_time = local_clock()
        if stdout:
            print(f"{name}: LSL Thread Receiving data...")
        if log:
            print_log(FILE_STREAM_LOG, f"{name}: LSL Thread Receiving data...")
        while True:
            if count % 100 == 0 and count != 0:
                rate = count / (end_time - start_time)
                latency = latency / (end_time - start_time)
                # count = 0
                # start_time = local_clock()
                if stdout:
                    print(f"Stream: {name}, Latency: {latency}s, Rate: {rate}s")
                if log:
                    print_log(FILE_STREAM_LOG, f"Stream: {name}, Latency: {latency}s, Rate: {rate}s")
            count += 1
            # Get a new sample from the inlet
            sample, timestamp = inlet.pull_sample()
            if '1' in name:
                for i in range(len(sample)):
                    shared.buf[i] = int(sample[i])
            else:
                for i in range(len(sample)):
                    shared.buf[4 + i] = int(sample[i])

            if stdout:
                print(f"Stream: {name}, Sample: {sample}, Timestamp: {timestamp}")
            if log:
                print_log(FILE_STREAM_LOG, f"Stream: {name}, Sample: {sample}, Timestamp: {timestamp}")
            # Get current local time
            end_time = local_clock()
            # Calculate latency
            latency += end_time - timestamp
            # print(f"Stream {idx} - Latency: {latency:.3f}s, Current Time: {end_time:.3f}s, "
            #       f"Timestamp: {timestamp:.3f}s")

    def find_sensor(name, shared, stdout=False, log=False):
        streams = resolve_stream('name', name)
        if len(streams) == 0:
            if stdout:
                print(f"Stream {name} not found")
            if log:
                print_log(FILE_STREAM_LOG, f"Stream {name} not found")
            return None
        if stdout:
            print(f"Found streams for {name}: ", streams[0].source_id())
        if log:
            print_log(FILE_STREAM_LOG, f"Found streams for {name}: {streams[0].source_id()}")
        inlet = StreamInlet(streams[0])
        receive_data(inlet, name, shared, stdout, log)

    def main(sensors, shared, stdout, log=False):
        print("Heartbeat Thread Starting ...")
        heartbeat_thread = threading.Thread(target=response, args=(DEVICE_NAME, stdout[1], log))
        heartbeat_thread.start()

        print("LSL Stream Consumption threads Starting ...")
        threads = []
        for sensor in sensors:
            thread = threading.Thread(target=find_sensor, args=(sensor, shared, stdout[0], log))
            threads.append(thread)

        if stdout[0]:
            print("LSL Stream Consumption threads Starting ...")
        if log:
            print_log(DEVICE_NAME + "_" + FILE_STREAM_LOG, "LSL Stream Consumption threads Starting ...")

        for thread in threads:
            thread.start()
        # for thread in threads:
        #     thread.join()

        if stdout[0]:
            print("LSL Stream Consumption threads finished")
        if log:
            print_log(DEVICE_NAME + "_" + FILE_STREAM_LOG, "LSL Stream Consumption threads finished")

        # heartbeat_thread.join()

    return main(SENSORS, shared, stdout, log)


# import time
# import numpy as np

# def make_lsl_loop(shared_mem):
#     # shared_array = np.ndarray((5,), dtype=np.int32, buffer=shared_mem.buf)
        
#     def lsl_loop():
#         x = [0 for _ in range(10)]
#         _x = 0
#         while True:
#             time.sleep(1)
#             _x += 1
#             _x = _x % 256
#             x = x[1:] + [_x]
#             for i in range(len(x)):
#                 shared_mem.buf[i] = x[i]

#     return lsl_loop

