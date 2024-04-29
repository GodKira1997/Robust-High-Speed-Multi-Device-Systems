import time

def make_lsl_loop(shared_mem):
    def lsl_loop():
        x = [0 for _ in range(10)]
        _x = 0
        while True:
            time.sleep(1)
            _x += 1
            _x = _x % 256
            x = x[1:] + [_x]
            for i in range(len(x)):
                shared_mem.buf[i] = x[i]

    return lsl_loop

