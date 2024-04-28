import time

def make_lsl_loop(shared_mem):
    def lsl_loop():
        x = 0
        while True:
            time.sleep(1)
            x += 1
            x = x % 256
            shared_mem.buf[0] = x

    return lsl_loop
