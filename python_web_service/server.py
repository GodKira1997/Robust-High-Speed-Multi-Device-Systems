from aiohttp import web
from threading import Thread
import argparse
import numpy as np

import socketio

from multiprocessing import shared_memory
shm_a = shared_memory.SharedMemory(create=True, size=10)

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

### Thread
from lsl_receiver import main_receive
parser = argparse.ArgumentParser(description="Stdout LSL Stream data or Heartbeat")
parser.add_argument('name', type=str, help="Name to server")
# parser.add_argument('--sout', choices=['streams', 'heartbeat'], default='streams',
#                     help="Type of console output")
parser.add_argument('--log', action='store_true', default=False, help="Log the file")
# parser.add_argument('--sensors', nargs='+', help="List of sensors to receive data from")
args = parser.parse_args()
stdout1 = True
stdout2 = False
t = Thread(target=main_receive(shm_a, args.name, (stdout1, stdout2), args.log))
# t = Thread(target=make_lsl_loop(shm_a))
t.start()




# async def background_task():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         await sio.sleep(10)
#         count += 1
#         await sio.emit('my_response', {'data': 'Server generated event'})


async def index(request):
    with open('app.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.event
async def get_latest_values(sid):
    data = [str(int(shm_a.buf[x])) for x in range(10)]
    await sio.emit('my_response', {'data': ", ".join(data)})



app.router.add_static('/static', 'static')
app.router.add_get('/', index)


async def init_app():
    # sio.start_background_task(background_task)
    return app


if __name__ == '__main__':
    web.run_app(init_app())
