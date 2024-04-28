import argparse
import threading
import time
from pylsl import StreamInfo, StreamOutlet, local_clock
from heartbeat_response import response, print_log

FILE_STREAM_LOG = 'lsl.log'
DEVICE_NAME = "Sensor1"
S_RATE = 1
N_CHANNELS = 2
TYPE = 'EEG'
CHANNEL_FORMAT = 'float32'


def main(name, s_rate, s_type, n_channels, channel_format, stdout, log=False):
    heartbeat_thread = threading.Thread(target=response, args=(DEVICE_NAME, stdout[1], log))
    heartbeat_thread.start()

    # Create a new stream info
    if stdout[0]:
        print("Creating a new stream...")
    if log:
        print_log(FILE_STREAM_LOG, "Creating a new stream...")
    info = StreamInfo(name, s_type, n_channels, s_rate, channel_format, DEVICE_NAME.lower())

    # next make an outlet
    if stdout[0]:
        print("Creating a stream outlet...")
    if log:
        print_log(FILE_STREAM_LOG, "Creating a stream outlet...")
    outlet = StreamOutlet(info)

    if stdout[0]:
        print("Sending data...")
    if log:
        print_log(FILE_STREAM_LOG, "Sending data...")
    start_time = local_clock()
    sent_samples = 0
    count = 0
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(s_rate * elapsed_time) - sent_samples
        for sample_ix in range(required_samples):
            mysample = [count + i for i in range(n_channels)]
            count += n_channels
            # now send it
            outlet.push_sample(mysample)
        sent_samples += required_samples
        # now send it and wait for a bit before trying again.
        time.sleep(0.01)

    heartbeat_thread.join()


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
    main(DEVICE_NAME, S_RATE, TYPE, N_CHANNELS, CHANNEL_FORMAT, (stdout1, stdout2), args.log)
