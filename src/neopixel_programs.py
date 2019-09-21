# This is script that run when device boot up or wake from sleep.
import uasyncio as asyncio
import machine, neopixel
import gc
from global_vars import manager

np = neopixel.NeoPixel(machine.Pin(4), 7, bpp=4)

def clear(np):
    n = np.n
    # clear
    for i in range(n):
        np[i] = (0, 0, 0, 0)
    np.write()

async def cycle(np, delay):
    n = np.n
    for i in range(n):
        for j in range(n):
            np[j] = (0, 0, 0, 0)
        np[i % n] = manager.led_color
        np.write()
        await asyncio.sleep_ms(delay)
    return 1

async def bounce(np, delay):
    n = np.n
    # bounce
    for i in range(n):
        for j in range(n):
            np[j] = manager.led_color
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0, 0)
        np.write()
        await asyncio.sleep_ms(delay)
    return 1

async def fade(np, delay):
    n = np.n
    # fade in/out
    for i in range(0, 2*256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0, 0)
        np.write()
        await asyncio.sleep_ms(int(delay/2))
    return 1

async def indirect(programm, delay):
    switcher={
            0:clear,
            1:cycle,
            2:bounce,
            3:fade,
            }
    func=switcher.get(programm, lambda :'Invalid')
    return await func(np, delay)

async def start(programm, delay):
    print("neopixel start")
    while True:
        await indirect(manager.program_number, delay)
        gc.collect()