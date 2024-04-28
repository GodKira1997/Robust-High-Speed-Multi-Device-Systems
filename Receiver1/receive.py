import argparse
import threading
from pylsl import StreamInlet, resolve_stream, local_clock
from heartbeat_response import response, print_log


FILE_STREAM_LOG = 'lsl.log'
DEVICE_NAME = "Receiver1"
SENSORS = ['Sensor1', 'Sensor2']


def receive_data(inlet, name, stdout=False, log=False):
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


def find_sensor(name, stdout=False, log=False):
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
    receive_data(inlet, name, stdout, log)


def main(sensors, stdout, log=False):
    # print("Heartbeat Thread Starting ...")
    # heartbeat_thread = threading.Thread(target=response, args=(DEVICE_NAME, stdout[0], log))
    # heartbeat_thread.start()

    print("LSL Stream Consumption threads Starting ...")
    threads = []
    for sensor in sensors:
        thread = threading.Thread(target=find_sensor, args=(sensor, stdout[0], log))
        threads.append(thread)

    if stdout[0]:
        print("LSL Stream Consumption threads Starting ...")
    if log:
        print_log(FILE_STREAM_LOG, "LSL Stream Consumption threads Starting ...")

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    if stdout[0]:
        print("LSL Stream Consumption threads finished")
    if log:
        print_log(FILE_STREAM_LOG, "LSL Stream Consumption threads finished")

    # heartbeat_thread.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Stdout LSL Stream data or Heartbeat")
    parser.add_argument('--sout', choices=['streams', 'heartbeat'], default='streams',
                        help="Type of console output")
    parser.add_argument('--log', action='store_true', default=False, help="Log the file")
    # parser.add_argument('--sensors', nargs='+', help="List of sensors to receive data from")
    args = parser.parse_args()
    stdout1 = False
    stdout2 = False
    if args.sout == 'streams':
        stdout1 = True
    elif args.sout == 'heartbeat':
        stdout2 = True
    main(SENSORS, (stdout1, stdout2), args.log)
