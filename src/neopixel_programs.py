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

async def cycle(np, delay, color):
    n = np.n
    if n % 2 == 0:
        for i in range(n):
            for j in range(n):
                np[j] = (0, 0, 0, 0)
            np[i % n] = color
            np.write()
            await asyncio.sleep_ms(delay)
    else:
        np[n-1] = color
        for i in range(n-1):
            for j in range(n-1):
                np[j] = (0, 0, 0, 0)
            np[i % n] = color
            np.write()
            await asyncio.sleep_ms(delay)

async def bounce(np, delay, color):
    n = np.n
    # bounce
    for i in range(n):
        for j in range(n):
            np[j] = color
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0, 0)
        np.write()
        await asyncio.sleep_ms(delay)

async def fade(np, delay, color):
    def truncate(current_value, max_value):
        if current_value < 0:
            return 0
        elif current_value > max_value:
            return max_value
        else:
            return current_value
    n = np.n
    # fade in/out
    max_color = max(color)
    for i in range(0, 2*max_color, 8):
        for j in range(n):
            result_color = [0, 0, 0, 0]
            for color_position in range(3):
                val = 0
                grow_speed = color[color_position]/max_color
                if (i // max_color) % 2 == 0:
                    val = truncate(color[color_position] - int(i * grow_speed), color[color_position])
                else:
                    val = truncate(int((i % max_color) * grow_speed), color[color_position])
                result_color[color_position] = val
            np[j] = tuple(result_color)
        np.write()
        await asyncio.sleep_ms(int(delay/2))

async def indirect(programm, delay, color):
    switcher={
            0:clear,
            1:cycle,
            2:bounce,
            3:fade,
            }
    func=switcher.get(programm, lambda :'Invalid')
    return await func(np, delay, color)

async def start():
    print("neopixel start")
    while True:
        await indirect(manager.program_number, manager.delay, manager.led_color)
        gc.collect()