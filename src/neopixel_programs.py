# This is script that run when device boot up or wake from sleep.
import uasyncio as asyncio
import machine, neopixel
import gc
from global_vars import manager
import urandom
from utime import time

np = neopixel.NeoPixel(machine.Pin(2), manager.led_amount, bpp=manager.led_bits)
# button = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

led_bits = manager.led_bits

async def wait_pin_change(pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    cur_value = pin.value()
    active = 0
    while active < 500:
        if pin.value() != cur_value:
            active += 1
        else:
            active = 0
        await asyncio.sleep_ms(1)

def get_n_bits_color_tuple(red, green, blue, white, n):
    if(n == 3):
        return (red, green, blue)
    elif(n == 4):
        return (red, green, blue, white)

async def clear(np, delay, color, background_color):
    n = np.n
    for i in range(n):
        np[i] = get_n_bits_color_tuple(0,0,0,0,led_bits)
    np.write()
    await asyncio.sleep_ms(1)

async def crazy_rainbow(np, delay, color, background_color):
    n = np.n
    for i in range(n):
        np[i] = get_n_bits_color_tuple(urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8), led_bits)
    np.write()
    await asyncio.sleep_ms(delay)

async def gradient(np, delay, color, background_color):
    n = np.n
    start_red = min(color[0], background_color[0])
    start_green = min(color[1], background_color[1])
    start_blue = min(color[2], background_color[2])

    delta_red = int((max(color[0], background_color[0]) - start_red)/n)
    delta_green = int((max(color[1], background_color[1]) - start_green)/n)
    delta_blue = int((max(color[2], background_color[2]) - start_blue)/n)

    for color_counter in range(n):
        np[color_counter] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
        start_red += delta_red
        start_green += delta_green
        start_blue += delta_blue
        np.write()
        await asyncio.sleep_ms(int(delay))

    for color_counter in range(n):
        np[color_counter] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
        start_red -= delta_red
        start_green -= delta_green
        start_blue -= delta_blue
        np.write()
        await asyncio.sleep_ms(int(delay))


async def rainbow(np, delay, color, background_color):
    n = np.n
    start_red = 240
    start_green = 0
    start_blue = 0
    for color_counter in range(n):
        np[color_counter] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
        start_green += int(255/n)
        np.write()
        await asyncio.sleep_ms(int(delay))
    for color_counter in range(n):
        np[color_counter] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
        start_red -= int(255/n)
        np.write()
        await asyncio.sleep_ms(int(delay))
    for color_counter in range(n):
        np[color_counter] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
        start_blue += int(255/n)
        np.write()
        await asyncio.sleep_ms(int(delay))
    for color_counter in range(n):
        np[color_counter] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
        start_green -= int(255/n)
        np.write()
        await asyncio.sleep_ms(int(delay))
    for color_counter in range(n):
        np[color_counter] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
        start_red += int(255/n)
        np.write()
        await asyncio.sleep_ms(int(delay))
    for color_counter in range(n):
        np[color_counter] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
        start_blue -= int(255/n)
        np.write()
        await asyncio.sleep_ms(int(delay))

async def cycle(np, delay, color, background_color):
    n = np.n
    if n % 2 == 0:
        for i in range(n):
            for j in range(n):
                np[j] = get_n_bits_color_tuple(background_color[0],background_color[1],background_color[2],0,led_bits)
            np[i % n] = get_n_bits_color_tuple(color[0],color[1],color[2],0,led_bits)
            np.write()
            await asyncio.sleep_ms(delay)
    else:
        np[n-1] = get_n_bits_color_tuple(color[0],color[1],color[2],0,led_bits)
        for i in range(n-1):
            for j in range(n-1):
                np[j] = get_n_bits_color_tuple(background_color[0],background_color[1],background_color[2],0,led_bits)
            np[i % n] = get_n_bits_color_tuple(color[0],color[1],color[2],0,led_bits)
            np.write()
            await asyncio.sleep_ms(delay)

async def bounce(np, delay, color, background_color):
    n = np.n
    for i in range(n):
        for j in range(n):
            np[j] = get_n_bits_color_tuple(color[0],color[1],color[2],0,led_bits)
        if (i // n) % 2 == 0:
            np[i % n] = get_n_bits_color_tuple(background_color[0],background_color[1],background_color[2],0,led_bits)
        else:
            np[n - 1 - (i % n)] = get_n_bits_color_tuple(background_color[0],background_color[1],background_color[2],0,led_bits)
        np.write()
        await asyncio.sleep_ms(delay)

async def fade(np, delay, color, background_color):
    def truncate(current_value, max_value):
        if current_value < 0:
            return 0
        elif current_value > max_value:
            return max_value
        else:
            return current_value
    n = np.n

    max_color = max(color)
    for i in range(0, 2*max_color, 8):
        for j in range(n):
            result_color = [0, 0, 0]
            for color_position in range(3):
                val = 0
                grow_speed = color[color_position]/max_color
                if (i // max_color) % 2 == 0:
                    val = truncate(color[color_position] - int(i * grow_speed), color[color_position])
                else:
                    val = truncate(int((i % max_color) * grow_speed), color[color_position])
                result_color[color_position] = val
            np[j] = get_n_bits_color_tuple(result_color[0],result_color[1],result_color[2],0,led_bits)
        np.write()
        await asyncio.sleep_ms(int(delay/2))

async def indirect(programm):
    switcher={
            0:clear,
            1:cycle,
            2:bounce,
            3:fade,
            4:rainbow,
            5:crazy_rainbow,
            6:gradient
            }
    func=switcher.get(programm, lambda :'Invalid')
    return await func(np, manager.delay, manager.led_color, manager.background_color)

async def start():
    await indirect(0)
    # await wait_pin_change(button)
    print("neopixel start")
    start = time()
    while True:
        now = time()
        time_diff = now - start + manager.delta_time
        if time_diff < 30:
            await indirect(3)
            print(time_diff)
        elif time_diff >= 30 and time_diff < 75:
            print(time_diff)
            await indirect(2)
        elif time_diff >= 75 and time_diff < 150:
            print(time_diff)
            await indirect(1)
        elif time_diff >= 150 and time_diff < 240:
            print(time_diff)
            await indirect(6)
        elif time_diff >= 240 and time_diff < 300:
            print(time_diff)
            await indirect(2)
        elif time_diff >= 300 and time_diff < 405:
            print(time_diff)
            await indirect(5)
        elif time_diff >= 405 and time_diff < 510:
            print(time_diff)
            await indirect(4)
        elif time_diff >= 510:
            print(time_diff)
            await indirect(3)
        await asyncio.sleep_ms(50)
