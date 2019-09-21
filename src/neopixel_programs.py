# This is script that run when device boot up or wake from sleep.
import uasyncio as asyncio
import machine, neopixel
import gc
from global_vars import manager

np = neopixel.NeoPixel(machine.Pin(4), 7, bpp=4)

def clear(np):
    n = np.n
    for i in range(n):
        np[i] = (0, 0, 0, 0)
    np.write()

async def cycle(np, delay, color, background_color):
    n = np.n
    if n % 2 == 0:
        for i in range(n):
            for j in range(n):
                np[j] = background_color
            np[i % n] = color
            np.write()
            await asyncio.sleep_ms(delay)
    else:
        np[n-1] = color
        for i in range(n-1):
            for j in range(n-1):
                np[j] = background_color
            np[i % n] = color
            np.write()
            await asyncio.sleep_ms(delay)

async def bounce(np, delay, color, background_color):
    n = np.n
    for i in range(n):
        for j in range(n):
            np[j] = color
        if (i // n) % 2 == 0:
            np[i % n] = background_color
        else:
            np[n - 1 - (i % n)] = background_color
        np.write()
        await asyncio.sleep_ms(delay)

async def fade(np, delay, color, background_color):
    def truncate(current_value, max_value):
        if current_value < 1:
            return 1
        elif current_value > max_value:
            return max_value
        else:
            return current_value
    n = np.n

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

async def indirect(programm):
    switcher={
            0:clear,
            1:cycle,
            2:bounce,
            3:fade,
            }
    func=switcher.get(programm, lambda :'Invalid')
    return await func(np, manager.delay, manager.led_color, manager.background_color)

async def start():
    print("neopixel start")
    while True:
        await indirect(manager.program_number)
        gc.collect()