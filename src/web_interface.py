import usocket as socket
import uasyncio as asyncio
import uselect as select
import gc
import json
import re
from index_html import html
from global_vars import manager

def set_color(hex_color):
    print(hex_color)
    new_color = hex_color.replace("#", "")
    color_array_hex = [new_color[i:i+2] for i in range(0, len(new_color), 2)]
    color_array_hex.append('00')
    color_array_decimal = map(lambda  x:int(x,16), color_array_hex)
    manager.led_color = tuple(color_array_decimal)

def set_program(program_id):
    print(program_id)
    manager.program_number = int(program_id)

switcher={
        'program':set_program,
        'color':set_color,
    }

def set_value(key, value):
    value_setter = switcher.get(key, lambda :'Not implemented')
    print(value_setter)
    value_setter(value)

class Server:
    async def run(self, loop):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        self.socks = [s]

        print('listening on', addr)

        poller = select.poll()
        poller.register(s, select.POLLIN)
        while True:
            res = poller.poll(1)  # 1ms block
            if res:  # Only s_sock is polled
                cl, addr = s.accept()
                loop.create_task(self.run_client(cl, addr, poller))
            await asyncio.sleep_ms(200)
            gc.collect()

    async def run_client(self, sock, cid, poller):
        self.socks.append(sock)
        sreader = asyncio.StreamReader(sock)
        swriter = asyncio.StreamWriter(sock, {})
        print('Got connection from client', cid)
        try:
            is_get_request = True
            content_length = 0
            print('Received from client {}'.format(cid))
            while True:
                res = await sreader.readline()
                if res == b'':
                    raise OSError
                print('{}'.format(res))
                if 'POST' in res: 
                    is_get_request = False
                if 'Content-Length' in res:
                    utf8Res = res.decode('UTF-8')
                    content_length = int(utf8Res.split(':')[1])
                if not res or res == b'\r\n':
                    if not is_get_request:
                        res_body = await sreader.read(content_length)
                        body_dict = json.loads(res_body)
                        for key in body_dict.keys():
                            set_value(key, body_dict.get(key))
                    break
            response = ""
            if is_get_request:
                new_color = "%X%X%X" % (manager.led_color[0], manager.led_color[1], manager.led_color[2])
                isxchecked = ['']*3
                isxchecked[manager.program_number - 1] = 'checked'
                response = html.format(color=new_color,is1checked=isxchecked[0],is2checked=isxchecked[1],is3checked=isxchecked[2])
            else:
                response = "HTTP/1.1 204 No Content\n\r\n"
            await swriter.awrite(response)
            print('Client {} disconnect.'.format(cid))
            sock.close()
            self.socks.remove(sock)
            poller.unregister(sock)
        except OSError:
            pass
        gc.collect()
    def close(self):
        print('Closing {} sockets.'.format(len(self.socks)))
        for sock in self.socks:
            sock.close()
