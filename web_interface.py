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
        client_id = 1  # For user feedback
        while True:
            res = poller.poll(1)  # 1ms block
            if res:  # Only s_sock is polled
                cl, addr = s.accept()
                loop.create_task(self.run_client(cl, addr))
                client_id += 1
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
                    regex1 = re.compile('(programm[a-z,=,0-9]+)')
                    new_programm_number = regex1.search(res)
                    if new_programm_number is not None:
                        global_vars.PROGRAMM_NUMBER = int(new_programm_number.group(0).decode('UTF-8').split('=')[1])
                        print(global_vars.PROGRAMM_NUMBER)
                if not res or res == b'\r\n':
                   break        
            response = html
            await swriter.awrite(response)  # Echo back
            print('Client {} disconnect.'.format(cid))
            sock.close()
            self.socks.remove(sock)
        except OSError:
            pass
    def close(self):
        print('Closing {} sockets.'.format(len(self.socks)))
        for sock in self.socks:
            sock.close()
