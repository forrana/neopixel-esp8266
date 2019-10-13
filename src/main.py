import uasyncio as asyncio
import machine
import neopixel_programs
import web_interface
from global_vars import manager
import sync_client
import sync_server

def conntect_to_master():
    import network
    print(manager.master_ap_id)
    print(manager.master_ap_password)
    print("conntect_to_master")
    if not manager.master_ap_id or not manager.master_ap_password:
        return

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(manager.master_ap_id, manager.master_ap_password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

loop = asyncio.get_event_loop()
loop.create_task(neopixel_programs.start())
server = web_interface.Server()
loop.create_task(server.run(loop))

if manager.is_sync_mode:
    conntect_to_master()
    loop.create_task(sync_client.run())
else:
    s_server = sync_server.Server()
    loop.create_task(s_server.run(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print('Interrupted')  # This mechanism doesn't work on Unix build.
except MemoryError:
    machine.reset()
finally:
    server.close()
