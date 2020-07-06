import sys
import select
import os
import termios
import tty
import asyncio

import websockets

STDIN_CHANNEL = 0
STDOUT_CHANNEL = 1
STDERR_CHANNEL = 2
ERROR_CHANNEL = 3
RESIZE_CHANNEL = 4


def readchar(quit_pipe):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        (readable, _, _) = select.select([sys.stdin, quit_pipe], [], [])
        if quit_pipe in readable:
            return None
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


async def output_tunnel(ws: websockets.WebSocketClientProtocol, quit_pipe):
    while True:
        data = await ws.recv()
        if len(data) < 1:
            continue
        channel = data[0]
        data = data[1:].decode() if len(data) > 1 else ''
        if channel == STDOUT_CHANNEL:
            print(data, end='', flush=True)
        elif channel == STDERR_CHANNEL:
            print(data, end='', file=sys.stderr, flush=True)
        elif channel == ERROR_CHANNEL:
            print(data, end='\r\n', file=sys.stderr)
            os.write(quit_pipe, b'.')
            break


async def input_tunnel(ws: websockets.WebSocketClientProtocol, quit_pipe):
    loop = asyncio.get_running_loop()
    while True:
        c = await loop.run_in_executor(None, readchar, quit_pipe)
        if c is None:
            break
        data = bytes([STDIN_CHANNEL]) + c.encode()
        await ws.send(data)


async def websocket_connect(url):
    (pipe_read, pipe_write) = os.pipe()
    try:
        async with websockets.connect(url) as ws:
            t1 = asyncio.create_task(output_tunnel(ws, pipe_write))
            t2 = asyncio.create_task(input_tunnel(ws, pipe_read))
            await asyncio.gather(t1, t2)
    except websockets.exceptions.ConnectionClosed:
        print('\r\nConnection closed by server', end='\r\n', file=sys.stderr)
        os.write(pipe_write, b'.')
    except OSError:
        print(f'Connection call to server {url} failed: host not found')
    except Exception:
        os.write(pipe_write, b'.')
        raise


async def websocket_write(url, file):
    try:
        async with websockets.connect(url) as ws:
            while True:
                content = file.read(32768)
                if not content:
                    break
                await ws.send(bytes([STDIN_CHANNEL]) + content)
    except websockets.exceptions.ConnectionClosed:
        print('\r\nConnection closed by server', end='\r\n', file=sys.stderr)
    except OSError:
        print(f'Connection call to server {url} failed: host not found')


async def websocket_read(url, file):
    try:
        async with websockets.connect(url) as ws:
            async for data in ws:
                if len(data) < 1:
                    continue
                channel = data[0]
                data = data[1:].decode() if len(data) > 1 else ''
                if channel == STDOUT_CHANNEL:
                    file.write(data.encode())
                elif channel == STDERR_CHANNEL:
                    print(data, end='', file=sys.stderr, flush=True)
                elif channel == ERROR_CHANNEL:
                    print(data, end='\r\n', file=sys.stderr)
                    break
    except websockets.exceptions.ConnectionClosed:
        print('\r\nConnection closed by server', end='\r\n', file=sys.stderr)
    except OSError:
        print(f'Connection call to server {url} failed: host not found')
