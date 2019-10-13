import usocket as socket
import uasyncio as asyncio
import ujson
# from uasyncio.queues import Queue
# q = Queue()

server = '192.168.4.1'
port = 8123

async def run():
    sock = socket.socket()
    def close():
        sock.close()
        print('Server disconnect.')
    try:
        serv = socket.getaddrinfo(server, port)[0][-1]
        sock.connect(serv)
    except OSError as e:
        print('Cannot connect to {} on port {}, {}'.format(server, port, e))
        sock.close()
        return
    while True:
        sreader = asyncio.StreamReader(sock)
        swriter = asyncio.StreamWriter(sock, {})
        data = ['value', 1]
        while True:
            try:
                await swriter.awrite('{}\n'.format(ujson.dumps(data)))
                res = await sreader.readline()
            except OSError:
                close()
                return
            try:
                master_state = ujson.loads(res)
                print('Received', master_state)
                # q.put(master_state)
            except ValueError:
                close()
                return
            # await asyncio.sleep(2)
            # data[1] += 1
