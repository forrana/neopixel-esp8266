import machine
import usocket as socket
import uasyncio as asyncio
import uselect as select
import ujson
import socket
import re
from index_html import html
import global_vars

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
                loop.create_task(self.run_client(cl, addr))
            await asyncio.sleep_ms(200)

    async def run_client(self, sock, cid):
        self.socks.append(sock)
        sreader = asyncio.StreamReader(sock)
        swriter = asyncio.StreamWriter(sock, {})
        print('Got connection from client', cid)
        try:
            while True:
                res = await sreader.readline()
                if res == b'':
                    raise OSError
                print('Received {} from client {}'.format(res, cid))
                if 'GET /?' in res:
                    utf8Res = res.decode('UTF-8')
                    program_regex = re.compile('(programm[a-z,=,0-9]+)')
                    color_regex = re.compile('(color[a-z,=,0-9,%]+)')
                    new_programm_number = program_regex.search(utf8Res)
                    new_color = color_regex.search(utf8Res)
                    if new_programm_number is not None:
                        global_vars.PROGRAMM_NUMBER = int(new_programm_number.group(0).split('=')[1])
                        print(global_vars.PROGRAMM_NUMBER)
                    if new_color is not None:
                        new_color = new_color.group(0).split('=')[1]
                        new_color = new_color.replace("%23", "")
                        color_array_hex = [new_color[i:i+2] for i in range(0, len(new_color), 2)]
                        color_array_hex.append('00')
                        color_array_decimal = map(lambda  x:int(x,16), color_array_hex)
                        global_vars.LED_COLOR = tuple(color_array_decimal)
                if not res or res == b'\r\n':
                   break        
            response = html
            await swriter.awrite(response)
            print('Client {} disconnect.'.format(cid))
            sock.close()
            self.socks.remove(sock)
        except OSError:
            pass
    def close(self):
        print('Closing {} sockets.'.format(len(self.socks)))
        for sock in self.socks:
            sock.close()
